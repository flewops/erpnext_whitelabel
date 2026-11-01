// Copyright (c) 2026, FlewOps Global and contributors
// For license information, please see LICENSE
//
// The desk's share of the branding: what exists only in the browser. The logo, app name,
// favicon, loading screen, app tiles and help menu rows are already branded on the server
// (flewops_whitelabel/branding.py) by the time this runs.

(() => {
	const settings = frappe.boot && frappe.boot.whitelabel;
	if (!settings) return;

	if (settings.hide_vendor_help) {
		// The help menu lists the documentation links registered for the current route.
		// Frappe and ERPNext register them as `frappe.help.help_links[route] = [...]`, some
		// lazily from form scripts that load later, so swallow every registration instead of
		// clearing the table once.
		frappe.help.help_links = new Proxy(
			{},
			{
				get: () => [],
				set: () => true,
			}
		);
	}

	if (settings.branded_about) {
		frappe.ui.misc.about = () => show_about(settings);
	}

	function show_about(settings) {
		const esc = frappe.utils.escape_html;
		const app_name = settings.app_name || frappe.boot.sysdefaults.app_name || __("About");
		const logo = settings.logo
			? `<img src="${esc(settings.logo)}" alt="${esc(
					app_name
			  )}" style="max-height: 56px; max-width: 220px;">`
			: "";
		const support = settings.support_url
			? `<a href="${esc(settings.support_url)}" target="_blank" rel="noopener">${esc(
					__(settings.support_label || "Support")
			  )}</a>`
			: "";

		// Admins get what support needs: every installed app and its version, and a plain
		// statement of the open-source stack the site runs on.
		let versions = "";
		if (frappe.user.has_role("System Manager")) {
			const rows = Object.entries(frappe.boot.versions || {})
				.map(
					([app, version]) =>
						`<tr><td>${esc(app)}</td><td class="text-right text-muted">${esc(
							version
						)}</td></tr>`
				)
				.join("");
			versions = `
				<table class="table table-sm mt-4 mb-2"><tbody>${rows}</tbody></table>
				<p class="text-muted small mb-0">${__(
					"Built on the open-source Frappe Framework and ERPNext."
				)}</p>`;
		}

		const dialog = new frappe.ui.Dialog({ title: __("About") });
		dialog.$body.html(`
			<div class="text-center py-3">
				${logo}
				<h4 class="mt-3 mb-1">${esc(app_name)}</h4>
				${support}
			</div>
			${versions}
		`);
		dialog.show();
	}
})();
