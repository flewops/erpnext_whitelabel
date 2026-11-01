import frappe


def execute():
	# A site installed before "Hide Frappe Cloud billing and links" existed has no value stored for
	# it; give it the default a new install gets. New installs skip patches.
	stored = frappe.db.sql(
		"select 1 from `tabSingles` where doctype = 'Whitelabel Settings' and field = 'hide_frappe_cloud'"
	)
	if not stored:
		frappe.db.set_single_value("Whitelabel Settings", "hide_frappe_cloud", 1)
