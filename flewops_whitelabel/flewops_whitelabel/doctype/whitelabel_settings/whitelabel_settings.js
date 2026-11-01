// Copyright (c) 2026, FlewOps Global and contributors
// For license information, please see LICENSE

frappe.ui.form.on("Whitelabel Settings", {
	refresh(frm) {
		// The installed apps, for the override rows' App field.
		const apps = (frappe.boot.app_data || []).map((app) => app.app_name);
		frm.fields_dict.app_overrides.grid.update_docfield_property("app", "options", apps);
	},

	after_save() {
		// Reload so the boot, and with it the logos and help menu, come from the new settings.
		frappe.ui.toolbar.clear_cache();
	},
});
