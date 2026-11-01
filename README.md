# FlewOps Whitelabel

White-label branding for **Frappe Framework / ERPNext v16**, by FlewOps Global.
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
| Branded About dialog | Help → About shows the client's name and logo. System Managers also see app versions and a "built on Frappe / ERPNext" note |
| Hide Frappe Cloud billing and links | The Manage Billing menu, trial banner and Frappe Cloud links that Frappe Cloud shows the site's administrators |
| Disable Onboarding / Update Notifications | The onboarding tours and the new-version / changelog popups |
| Text Replacements | Exact-match UI text, saved as Translations for the system language (ships with "ERPNext Settings" → "Settings") |
| Hide "Built on Frappe" / Footer Credit | Website footer |
| Email footer | Standard "Sent via …" footer and footer address on outgoing emails |

### How it works

The branding is written into the settings Frappe already reads: **System Settings**, **Website
Settings** and **Navbar Settings**. That means:

- **Per site.** Several clients on one bench group each keep their own brand; nothing is stored in
  the bench, site config or app code.
- **Your manual edits survive.** A blank field here leaves Frappe's own value alone. Clearing a field
  you had set clears it in Frappe too.
- **Survives updates.** It is written again after every migrate (every Frappe Cloud deploy) and after
  the setup wizard of a new site.

Only two things happen in the browser (`public/js/flewops_whitelabel.bundle.js`): hiding the
per-page documentation links and replacing the About dialog.

## Install on Frappe Cloud

Client sites run on Frappe Cloud. The full walkthrough — bench group, adding the app, deploying,
installing on a site, custom domain and email — is in **[docs/FRAPPE_CLOUD.md](docs/FRAPPE_CLOUD.md)**.

In short: add `flewops/erpnext_whitelabel` (branch `main`) to a **Version 16** private bench group,
deploy, install **FlewOps Whitelabel** on the site, then fill in **Whitelabel Settings**.

## Install on a bench (development)

```bash
bench get-app https://github.com/flewops/erpnext_whitelabel --branch version-16
bench --site <site> install-app flewops_whitelabel
```

The repository is `erpnext_whitelabel`; the Frappe app inside it is `flewops_whitelabel`, which is
the name `install-app`, `bench --site … run-tests --app` and `apps.txt` use.

If the site has another app named `whitelabel` installed, uninstall it first; the installer
refuses to run alongside it, since both write the same settings.

## Branches

| Branch | Purpose |
| --- | --- |
| `version-16` | Development for Frappe v16. All changes are made here. |
| `main` | What client sites run. Updated only by pull request from `version-16`. |

1. Commit to `version-16` and push. CI runs lint and the tests.
2. Open a pull request `version-16` → `main`. CI runs again on the pull request.
3. Merge when it is green. Frappe Cloud then shows an update for the bench group; deploy it.

Changes are recorded in `CHANGELOG.md` by date. After each Frappe update, check on a test site:
the login page, the apps screen, the help menu and the About dialog. Those read Frappe's desk
markup and are the parts most likely to move.

## Uninstall

Frappe Cloud: Site → Apps → FlewOps Whitelabel → Uninstall. On a bench:
`bench --site <site> uninstall-app flewops_whitelabel`.

What was written into System / Website / Navbar Settings stays. Clear those fields in
Whitelabel Settings and save before uninstalling if you want Frappe's defaults back.

## Development

```bash
bench --site <site> set-config allow_tests true
bench --site <site> run-tests --app flewops_whitelabel
pre-commit install   # ruff, eslint, prettier
```

CI (`.github/workflows/ci.yml`) runs lint and the tests on a fresh v16 site with ERPNext, on every
push to `version-16` / `main` and on every pull request.

## License

MIT. Copyright © 2026 FlewOps Global. See `LICENSE`.

Frappe Framework is MIT-licensed and ERPNext is GPL-3.0. This app only changes branding; it does
not modify or redistribute either. The About dialog keeps a "built on Frappe / ERPNext" note for
administrators.
