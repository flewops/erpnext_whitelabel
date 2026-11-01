# Copyright (c) 2026, FlewOps Global and contributors
# For license information, please see LICENSE

import frappe
from frappe.tests import IntegrationTestCase

from flewops_whitelabel import branding

LOGO = "/files/acme-logo.png"
FAVICON = "/files/acme-favicon.png"


def website(fieldname):
	return frappe.db.get_single_value("Website Settings", fieldname)


def system(fieldname):
	return frappe.db.get_single_value("System Settings", fieldname)


def help_rows():
	return frappe.get_single("Navbar Settings").help_dropdown


class TestWhitelabelSettings(IntegrationTestCase):
	def setUp(self):
		self.settings = frappe.get_single("Whitelabel Settings")

	def update(self, **values):
		self.settings.update(values)
		self.settings.save()
		self.settings.reload()
		return self.settings

	def test_branding_reaches_frappe_settings(self):
		self.update(app_name="Acme ERP", app_logo=LOGO, favicon=None, splash_image=None)

		self.assertEqual(system("app_name"), "Acme ERP")
		self.assertEqual(website("app_name"), "Acme ERP")
		self.assertEqual(website("app_logo"), LOGO)
		self.assertEqual(frappe.db.get_single_value("Navbar Settings", "app_logo"), LOGO)
		# favicon and loading screen fall back to the logo
		self.assertEqual(website("favicon"), LOGO)
		self.assertEqual(website("splash_image"), LOGO)

		self.update(favicon=FAVICON)
		self.assertEqual(website("favicon"), FAVICON)

	def test_clearing_a_field_clears_it_in_frappe(self):
		self.update(app_logo=LOGO, favicon=None, splash_image=None)
		self.update(app_logo=None)

		self.assertFalse(website("app_logo"))
		self.assertFalse(website("favicon"))
		self.assertFalse(frappe.db.get_single_value("Navbar Settings", "app_logo"))

	def test_blank_field_leaves_site_value_alone(self):
		self.update(footer_powered=None)
		frappe.db.set_single_value("Website Settings", "footer_powered", "Set by hand")

		self.update(app_name="Acme ERP")  # footer_powered was blank and still is
		self.assertEqual(website("footer_powered"), "Set by hand")

		branding.apply()  # after_migrate
		self.assertEqual(website("footer_powered"), "Set by hand")

	def test_flags(self):
		self.update(disable_onboarding=1, disable_update_notifications=1, disable_standard_email_footer=1)
		self.assertEqual(system("enable_onboarding"), 0)
		self.assertEqual(system("disable_system_update_notification"), 1)
		self.assertEqual(system("disable_change_log_notification"), 1)
		self.assertEqual(system("disable_standard_email_footer"), 1)

		self.update(disable_onboarding=0, disable_update_notifications=0, disable_standard_email_footer=0)
		self.assertEqual(system("enable_onboarding"), 1)
		self.assertEqual(system("disable_system_update_notification"), 0)
		self.assertEqual(system("disable_standard_email_footer"), 0)

	def test_vendor_help_rows(self):
		def external_hidden():
			return {row.item_label: row.hidden for row in help_rows() if branding._is_external(row.route)}

		self.update(hide_vendor_help=1)
		self.assertTrue(external_hidden())
		self.assertTrue(all(external_hidden().values()))
		# rows inside the site stay
		self.assertFalse(any(row.hidden for row in help_rows() if row.item_label == "System Health"))

		self.update(hide_vendor_help=0)
		self.assertFalse(any(external_hidden().values()))

	def test_support_row(self):
		def support_rows():
			return [(row.item_label, row.route) for row in help_rows() if not row.is_standard]

		self.update(support_label="Helpdesk", support_url="https://help.example.com")
		self.assertEqual(support_rows(), [("Helpdesk", "https://help.example.com")])

		self.update(support_label="Get Help")  # renamed, not duplicated
		self.assertEqual(support_rows(), [("Get Help", "https://help.example.com")])

		self.update(support_url=None)
		self.assertEqual(support_rows(), [])

	def test_text_replacements(self):
		def translated(source_text):
			return frappe.db.get_value("Translation", {"source_text": source_text}, "translated_text")

		self.settings.text_replacements = []
		self.settings.append("text_replacements", {"source_text": "Sales Invoice", "translated_text": "Bill"})
		self.settings.save()
		self.assertEqual(translated("Sales Invoice"), "Bill")

		self.settings.reload()
		self.settings.text_replacements[0].translated_text = "Invoice"
		self.settings.save()
		self.assertEqual(translated("Sales Invoice"), "Invoice")
		self.assertEqual(frappe.db.count("Translation", {"source_text": "Sales Invoice"}), 1)

		self.settings.reload()
		self.settings.text_replacements = []
		self.settings.save()
		self.assertIsNone(translated("Sales Invoice"))

	def test_duplicate_rows_rejected(self):
		self.settings.text_replacements = []
		self.settings.append("text_replacements", {"source_text": "Item", "translated_text": "Product"})
		self.settings.append("text_replacements", {"source_text": "Item", "translated_text": "Thing"})
		self.assertRaises(frappe.ValidationError, self.settings.save)

	def test_override_needs_installed_app(self):
		self.settings.app_overrides = []
		self.settings.append("app_overrides", {"app": "not_an_app", "app_title": "X"})
		self.assertRaises(frappe.ValidationError, self.settings.save)

	def test_app_tiles(self):
		self.settings.update({"app_logo": LOGO, "replace_framework_logos": 1, "app_overrides": []})
		self.settings.append("app_overrides", {"app": "frappe", "app_title": "Platform"})
		app_data = [
			{"app_name": "frappe", "app_title": "Frappe Framework", "app_logo_url": ["/f.svg"]},
			{"app_name": "erpnext", "app_title": "ERPNext", "app_logo_url": ["/e.svg"]},
			{"app_name": "hrms", "app_title": "Frappe HR", "app_logo_url": ["/h.svg"]},
		]
		branding.rebrand_app_tiles(app_data, self.settings)

		self.assertEqual(app_data[0], {"app_name": "frappe", "app_title": "Platform", "app_logo_url": LOGO})
		self.assertEqual(app_data[1]["app_logo_url"], LOGO)
		self.assertEqual(app_data[2]["app_logo_url"], ["/h.svg"])  # not a framework app, not overridden

	def test_footer_context(self):
		self.update(hide_powered_by=1)
		context = frappe._dict(footer_powered=None)
		branding.update_website_context(context)
		self.assertTrue(context.footer_powered)

		context = frappe._dict(footer_powered="Powered by Acme")
		branding.update_website_context(context)
		self.assertEqual(context.footer_powered, "Powered by Acme")

		self.update(hide_powered_by=0)
		context = frappe._dict(footer_powered=None)
		branding.update_website_context(context)
		self.assertFalse(context.footer_powered)
