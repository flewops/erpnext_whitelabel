import frappe
from frappe import _

# Shown in place of these strings for the system language, out of the box.
DEFAULT_TEXT_REPLACEMENTS = [
	("ERPNext Settings", "Settings"),
]


def before_install():
	# An app named "whitelabel" writes the same Frappe settings from its own settings page, so with
	# both installed each save undoes the other.
	if "whitelabel" in frappe.get_installed_apps():
		frappe.throw(
			_("Uninstall the 'whitelabel' app first: it manages the same settings as FlewOps Whitelabel.")
		)


def after_install():
	settings = frappe.get_single("Whitelabel Settings")
	for source_text, translated_text in DEFAULT_TEXT_REPLACEMENTS:
		settings.append("text_replacements", {"source_text": source_text, "translated_text": translated_text})
	# Saving applies the defaults (help menu, notifications, footers) through on_update.
	settings.save(ignore_permissions=True)
