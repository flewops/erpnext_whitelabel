"""Writes the branding into the settings Frappe itself reads.

The login page, the desk's title and loading screen, the website's favicon and footer, the help
menu and outgoing emails all read System, Website and Navbar Settings, so that is where the
branding goes. Those settings live in each site's database, so every client site on a bench keeps
its own brand.
"""

import frappe
from frappe.utils import cint

# Apps whose tiles take the client's logo when "Use logo for Frappe and ERPNext tiles" is on.
FRAMEWORK_APPS = ("frappe", "erpnext")


def get_settings():
	return frappe.get_cached_doc("Whitelabel Settings")


def apply(settings=None, previous=None):
	"""Write the branding into Frappe's settings.

	Called on every save of Whitelabel Settings (with the values from before the save) and after
	every migrate (without them).
	"""
	settings = settings or frappe.get_single("Whitelabel Settings")
	write_settings(settings, previous)
	sync_help_menu(settings, previous)
	sync_text_replacements(settings, previous)
	frappe.clear_cache()


def _branding_values(settings) -> dict[tuple[str, str], str | None]:
	logo = settings.app_logo
	return {
		("System Settings", "app_name"): settings.app_name,
		("Website Settings", "app_name"): settings.app_name,
		("Website Settings", "app_logo"): logo,
		("Navbar Settings", "app_logo"): logo,
		("Website Settings", "favicon"): settings.favicon or logo,
		("Website Settings", "splash_image"): settings.splash_image or logo,
		("Website Settings", "footer_powered"): settings.footer_powered,
		("System Settings", "email_footer_address"): settings.email_footer_address,
	}


def _flag_values(settings) -> dict[tuple[str, str], int]:
	updates = cint(settings.disable_update_notifications)
	email_footer = cint(settings.disable_standard_email_footer)
	return {
		("System Settings", "enable_onboarding"): 0 if cint(settings.disable_onboarding) else 1,
		("System Settings", "disable_system_update_notification"): updates,
		("System Settings", "disable_change_log_notification"): updates,
		("System Settings", "disable_standard_email_footer"): email_footer,
		("System Settings", "hide_footer_in_auto_email_reports"): email_footer,
	}


def write_settings(settings, previous=None):
	"""A blank branding field leaves Frappe's value alone, so whatever the site already had stays.
	Blanking a field that was set clears it in Frappe too, back to Frappe's default."""
	before = _branding_values(previous) if previous else {}
	updates = {
		key: value or None for key, value in _branding_values(settings).items() if value or before.get(key)
	}
	updates.update(_flag_values(settings))

	by_doctype: dict[str, dict] = {}
	for (doctype, fieldname), value in updates.items():
		current = frappe.db.get_single_value(doctype, fieldname)
		if (current or None) != (value or None):
			by_doctype.setdefault(doctype, {})[fieldname] = value

	# set_single_value rather than saving the documents: System and Website Settings validate
	# much more than branding on save, and an unrelated problem there must not block this.
	for doctype, values in by_doctype.items():
		frappe.db.set_single_value(doctype, values)


def _is_external(route: str | None) -> bool:
	return bool(route) and route.startswith(("http://", "https://"))


def sync_help_menu(settings, previous=None):
	"""Hide the standard help rows that lead off the site (Frappe Support and the like, from any
	app's standard_help_items), and keep the optional support row in step with the settings."""
	navbar = frappe.get_single("Navbar Settings")
	changed = False

	hidden = cint(settings.hide_vendor_help)
	for item in navbar.help_dropdown:
		if item.is_standard and _is_external(item.route) and cint(item.hidden) != hidden:
			item.hidden = hidden
			changed = True

	# Our row is the non-standard route row under the support label, now or before this save.
	labels = {settings.support_label, previous.support_label if previous else None} - {None, ""}
	ours = [
		item
		for item in navbar.help_dropdown
		if not item.is_standard and item.item_type == "Route" and item.item_label in labels
	]
	keep = None
	if settings.support_url:
		label = settings.support_label or "Support"
		keep = ours[0] if ours else navbar.append("help_dropdown", {"item_type": "Route"})
		if keep.item_label != label or keep.route != settings.support_url or keep.hidden:
			keep.update({"item_label": label, "route": settings.support_url, "hidden": 0})
			changed = True
	for item in ours:
		if item is not keep:
			navbar.remove(item)
			changed = True

	if changed:
		navbar.save(ignore_permissions=True)


def sync_text_replacements(settings, previous=None):
	"""Each replacement is a Translation for the system language. The row keeps the Translation's
	name, so editing a row updates it and removing a row deletes it."""
	language = frappe.db.get_single_value("System Settings", "language") or "en"
	kept = set()

	for row in settings.text_replacements:
		name = (
			row.translation if row.translation and frappe.db.exists("Translation", row.translation) else None
		)
		# A Translation the site already has for this text is taken over rather than duplicated:
		# with two, which one wins is arbitrary.
		name = name or frappe.db.get_value(
			"Translation",
			{"language": language, "source_text": row.source_text, "context": ("is", "not set")},
		)
		translation = frappe.get_doc("Translation", name) if name else frappe.new_doc("Translation")
		values = {
			"language": language,
			"source_text": row.source_text,
			"translated_text": row.translated_text,
		}
		if translation.is_new() or any(translation.get(key) != value for key, value in values.items()):
			translation.update(values)
			translation.save(ignore_permissions=True)
		if row.translation != translation.name:
			row.db_set("translation", translation.name, update_modified=False)
		kept.add(translation.name)

	for row in previous.text_replacements if previous else []:
		if row.translation and row.translation not in kept:
			frappe.delete_doc_if_exists("Translation", row.translation)


def after_setup_wizard(args=None):
	apply()


def boot_session(bootinfo):
	if frappe.session.user == "Guest":
		return

	settings = get_settings()
	bootinfo.whitelabel = {
		"app_name": settings.app_name,
		"logo": settings.app_logo,
		"hide_vendor_help": cint(settings.hide_vendor_help),
		"branded_about": cint(settings.branded_about),
		"support_label": settings.support_label,
		"support_url": settings.support_url,
	}
	rebrand_app_tiles(bootinfo.get("app_data") or [], settings)


def rebrand_app_tiles(app_data: list[dict], settings):
	"""The apps screen, the dock and the sidebar header draw each app from boot's app_data, with
	the logo and title the app ships. Swap in the client's where the settings say so."""
	overrides = {row.app: row for row in settings.app_overrides}
	for app in app_data:
		app_name = app.get("app_name")
		if cint(settings.replace_framework_logos) and settings.app_logo and app_name in FRAMEWORK_APPS:
			app["app_logo_url"] = settings.app_logo
		if row := overrides.get(app_name):
			if row.app_title:
				app["app_title"] = row.app_title
			if row.logo:
				app["app_logo_url"] = row.logo


def extend_bootinfo(bootinfo):
	# Frappe Cloud shows its billing menu and trial banner (billing.bundle.js) and its support and
	# update links in About to System Managers when is_fc_site is set, using site_info.
	if bootinfo.get("is_fc_site") and cint(get_settings().hide_frappe_cloud):
		bootinfo.is_fc_site = False
		bootinfo.site_info = None


def update_website_context(context):
	# footer_info.html prints "Built on Frappe" only while footer_powered is empty, and the text
	# from Website Settings is already in the context by now.
	if not context.get("footer_powered") and cint(get_settings().hide_powered_by):
		context.footer_powered = " "
