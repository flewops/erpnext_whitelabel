# Changelog

Changes to FlewOps Whitelabel for Frappe / ERPNext v16, newest first.

## 2026-11-01

- Whitelabel Settings: app name, logo, favicon, loading screen image, app tile overrides,
  help menu (hide vendor links, own support link), branded About dialog, onboarding and update
  notifications, text replacements, website footer credit, email footer.
- Branding written into System / Website / Navbar Settings per site; re-applied after every
  migrate and after the setup wizard of a new site.
- v16 desk support: apps screen, dock and sidebar header tiles; help menu via Navbar Settings.
- Frappe Cloud ready: setup guide (`docs/FRAPPE_CLOUD.md`); hides Frappe Cloud's billing menu,
  trial banner and links from the client's administrators (on by default).
- Desk script built as a bundle, so a deploy reaches browsers without a stale cached copy.
- Refuses to install alongside another app named `whitelabel`, which would write the same settings.
- Branch flow: changes on `version-16`, merged into `main` by pull request.
