# Frappe Cloud setup

How FlewOps puts a client's site on Frappe Cloud with FlewOps Whitelabel. Frappe Cloud renames
buttons from time to time; if one below has moved, the step is still the same.

## Before you start

- A Frappe Cloud account for the FlewOps team. Custom apps need a **private bench group**, which
  Frappe Cloud offers from its $25/month plan up.
- Access to this repository from Frappe Cloud. When Frappe Cloud asks to connect GitHub, install
  its GitHub app on the `flewops` account and give it access to `erpnext_whitelabel`. That is
  required if the repository is private.

## 1. Bench group

Create a bench group on **Version 16**, in the region nearest the clients, with the apps the
clients need (ERPNext, and HRMS or others as required). One bench group can host many client
sites; each keeps its own branding.

## 2. Add the app

Bench group → **Apps** → **Add App** → GitHub:

| Field | Value |
| --- | --- |
| Repository | `flewops/erpnext_whitelabel` |
| Branch | `main` |

Frappe Cloud reads the app from `pyproject.toml`: it appears as **FlewOps Whitelabel**
(`flewops_whitelabel`) and requires Frappe 16.

## 3. Deploy

Click **Update Available** (or **Deploy**) on the bench group, select the sites to update, and
**Deploy and update**. Frappe Cloud builds the bench with the app and its assets; this takes a few
minutes. A site can only install the app after this deploy.

## 4. Install on the client's site

- **New site:** create it on this bench group and tick FlewOps Whitelabel with the other apps.
- **Existing site:** Site → **Apps** → **Install App** → FlewOps Whitelabel.

Installing applies the defaults at once: Frappe / ERPNext help links hidden, Frappe Cloud billing
and links hidden from the client's admins, onboarding and update popups off, "Built on Frappe"
footer and standard email footer off. On a new site the setup wizard runs afterwards; the
branding is re-applied when it finishes.

## 5. Brand the site

Log in as Administrator → search **Whitelabel Settings**:

1. **App Name** — the client's product name, e.g. "Acme ERP".
2. **Logo** — upload as a **public** file (untick *Is Private*); the login page is seen by guests.
3. **Favicon** and **Loading Screen Image** — optional, both fall back to the logo.
4. **Desk** tab → **Support Link** — FlewOps' helpdesk or WhatsApp link for the client.
5. Save, then reload the browser.

## 6. Custom domain

The default address `<site>.frappe.cloud` shows Frappe Cloud in the address bar, so give every
client site its own domain:

1. Site → **Domains** → add the domain, e.g. `erp.acme.com`.
2. At the client's DNS provider, add a **CNAME** from `erp.acme.com` to `<site>.frappe.cloud`
   (for a bare domain like `acme.com`, an **A** record to the site's IP shown by Frappe Cloud).
3. Once verified, Frappe Cloud issues the SSL certificate. Set the domain as **Primary**, so the
   `.frappe.cloud` address redirects to it.

## 7. Outgoing email

Add an **Email Account** for the client's domain (Settings → Email Account, *Default Outgoing*)
so notifications and login emails come from the client's own address, then leave **Disable
Standard Email Footer** on in Whitelabel Settings.

## Updating

1. Changes are made on `version-16` and reach `main` by pull request (see the README).
2. After the merge, the bench group shows **Update Available**. Deploy and update the sites.
3. Each site runs a migrate during the update, and the branding is written again after it.

Check one client site after each deploy: login page, apps screen, help menu, About dialog.

## Staging (optional)

To try a change on Frappe Cloud before it reaches clients, keep a second bench group whose
FlewOps Whitelabel app tracks the `version-16` branch, with one test site. Merge to `main` once it
looks right there.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| FlewOps Whitelabel missing from *Install App* | The bench group hasn't been deployed since the app was added. Deploy it. |
| Logo missing on the login page | The file is private. Re-upload it as public. |
| Old branding after saving | Reload the browser; saving the settings clears the server cache. |
| The client needs to see Frappe Cloud billing | Untick **Hide Frappe Cloud billing and links** (Desk tab). FlewOps manages billing from its own Frappe Cloud dashboard either way. |
