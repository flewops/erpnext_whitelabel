# FlewOps Whitelabel

White-label branding for **Frappe Framework / ERPNext v16**, maintained by FlewOps Global.
Install it on a client's site and the desk, login page, website and emails carry the client's
name and logo instead of Frappe's and ERPNext's.

## What it brands

Everything is set from **Whitelabel Settings** (search for it in the awesome bar; System Manager
only).

| Setting | Where it shows |
| --- | --- |
| App Name | Desk browser tab title, "Login to …" email subject, branded About dialog |
| Logo | Login page, desk, apps screen |
| Favicon | Browser tab, desk and website (falls back to the logo) |
| Loading Screen Image | Desk splash while it loads (falls back to the logo) |
| Use the logo for the Frappe and ERPNext tiles | Apps screen, dock, sidebar header |
| App Overrides | Rename or re-logo any installed app's tile (e.g. `hrms` → "People") |
| Hide Frappe / ERPNext help links | Help menu rows that leave the site (Frappe Support, …) and per-page documentation links |
| Support Link | Your own row in the help menu (helpdesk, WhatsApp, …) |
| Branded About dialog | Help → About shows the client's name and logo. System Managers also see app versions and an "built on Frappe / ERPNext" note |
| Disable Onboarding / Update Notifications | The onboarding tours and the new-version / changelog popups |
| Text Replacements | Exact-match UI text, saved as Translations for the system language (ships with "ERPNext Settings" → "Settings") |
| Hide "Built on Frappe" / Footer Credit | Website footer |
| Email footer | Standard "Sent via …" footer and footer address on outgoing emails |

### How it works

The branding is written into the settings Frappe already reads: **System Settings**, **Website
Settings** and **Navbar Settings**. That means:

- **Per site.** Several clients on one bench each keep their own brand; nothing is stored in the
  bench, site config or app code.
- **Your manual edits survive.** A blank field here leaves Frappe's own value alone. Clearing a field
  you had set clears it in Frappe too.
- **Survives updates.** It is written again after every `bench migrate`.

Only two things happen in the browser (`public/js/flewops_whitelabel.js`): hiding the per-page
documentation links and replacing the About dialog.

## Install

```bash
bench get-app https://github.com/flewops/erpnext_whitelabel
bench --site <site> install-app flewops_whitelabel
bench --site <site> migrate
```

The repository is `erpnext_whitelabel`; the Frappe app inside it is `flewops_whitelabel`, which is
the name `install-app`, `bench --site … run-tests --app` and `apps.txt` use.

Then open **Whitelabel Settings**, upload the logo (as a **public** file — guests see it on the
login page), set the app name and save. Reload the desk.

For Docker / frappe_docker images, add it to `apps.json`:

```json
{ "url": "https://github.com/flewops/erpnext_whitelabel", "branch": "v1.0.0" }
```

If the site has another app named `whitelabel` installed, uninstall it first; the installer
refuses to run alongside it, since both write the same settings.

## Uninstall

```bash
bench --site <site> uninstall-app flewops_whitelabel
```

What was written into System / Website / Navbar Settings stays. Clear those fields in
Whitelabel Settings and save before uninstalling if you want Frappe's defaults back.

## Development

```bash
bench --site <site> set-config allow_tests true
bench --site <site> run-tests --app flewops_whitelabel
pre-commit install   # ruff, eslint, prettier
```

CI (`.github/workflows/ci.yml`) runs lint and the tests on a fresh v16 site with ERPNext.

## Branches and releases

| Branch | Frappe |
| --- | --- |
| `main` | v16 (current) |

When Frappe v17 ships, branch `version-16` off `main` for the v16 clients, then move `main` to v17;
client sites stay on the branch matching their Frappe version. Releases are tags (`v1.0.0`, `v1.1.0`, …) on the
version branch, recorded in `CHANGELOG.md`. Pin client images to a tag, not a branch.

After each Frappe minor update, check on a test site: the login page, the apps screen, the help
menu and the About dialog. Those read Frappe's desk markup and are the parts most likely to move.

## License

MIT. Copyright © 2026 FlewOps Global. See `LICENSE`.

Frappe Framework is MIT-licensed and ERPNext is GPL-3.0. This app only changes branding; it does
not modify or redistribute either. The About dialog keeps a "built on Frappe / ERPNext" note for
administrators.
