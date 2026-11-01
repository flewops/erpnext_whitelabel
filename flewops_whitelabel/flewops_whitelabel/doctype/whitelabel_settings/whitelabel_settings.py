# Copyright (c) 2026, FlewOps Global and contributors
# For license information, please see LICENSE

import frappe
from frappe import _
from frappe.model.document import Document

from flewops_whitelabel import branding


class WhitelabelSettings(Document):
	def validate(self):
		self.validate_app_overrides()
		self.validate_text_replacements()

	def on_update(self):
		# on_update rather than validate: the branding goes out only once this save has gone through.
		branding.apply(self, self.get_doc_before_save())

	def validate_app_overrides(self):
		installed = frappe.get_installed_apps()
		seen = set()
		for row in self.app_overrides:
			if row.app not in installed:
				frappe.throw(
					_("Row {0}: {1} is not installed on this site.").format(row.idx, frappe.bold(row.app))
				)
			if row.app in seen:
				frappe.throw(_("Row {0}: {1} is overridden twice.").format(row.idx, frappe.bold(row.app)))
			seen.add(row.app)

	def validate_text_replacements(self):
		seen = set()
		for row in self.text_replacements:
			if row.source_text in seen:
				frappe.throw(
					_("Row {0}: {1} is replaced twice.").format(row.idx, frappe.bold(row.source_text))
				)
			seen.add(row.source_text)
