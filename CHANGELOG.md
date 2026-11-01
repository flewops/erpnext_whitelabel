# Changelog

## v1.0.0 — 2026-11-01

First release, for Frappe / ERPNext v16.

- Whitelabel Settings: app name, logo, favicon, loading screen image, app tile overrides,
  help menu (hide vendor links, own support link), branded About dialog, onboarding and update
  notifications, text replacements, website footer credit, email footer.
- Branding written into System / Website / Navbar Settings per site; re-applied after migrate.
- v16 desk support: apps screen, dock and sidebar header tiles; help menu via Navbar Settings.
- Refuses to install alongside another app named `whitelabel`, which would write the same settings.
