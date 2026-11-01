app_name = "flewops_whitelabel"
app_title = "FlewOps Whitelabel"
app_publisher = "FlewOps Global"
app_description = "White-label branding for Frappe Framework / ERPNext v16"
app_email = "flewopsglobal@gmail.com"
app_license = "mit"

# No add_to_apps_screen: the app has no tile of its own. Its one page is Whitelabel Settings,
# reached from the awesome bar.

# Includes in <head>
# ------------------

# The parts of the branding that only exist in the browser: documentation links and the
# About dialog. Everything else is written into Frappe's own settings on the server.
# A bundle, so `bench build` gives it a hashed name and browsers pick up a new deploy at once.
app_include_js = "flewops_whitelabel.bundle.js"

# Installation
# ------------

before_install = "flewops_whitelabel.install.before_install"
after_install = "flewops_whitelabel.install.after_install"

# Updates to Frappe or ERPNext can reset what the branding wrote, so it is written again after
# every migrate.
after_migrate = "flewops_whitelabel.branding.apply"

# The setup wizard of a new site (Frappe Cloud installs the apps before it runs) sets the system
# language, which the text replacements are saved under.
setup_wizard_complete = "flewops_whitelabel.branding.after_setup_wizard"

# Boot / website context
# ----------------------

# Rebrands the app tiles (apps screen, dock, sidebar header) and hands the desk script its flags.
boot_session = "flewops_whitelabel.branding.boot_session"

# Hides Frappe Cloud's billing menu, trial banner and links. Not in boot_session: Frappe sets the
# Frappe Cloud flags after those hooks run, and this hook runs last, cached boot or not.
extend_bootinfo = "flewops_whitelabel.branding.extend_bootinfo"

# Hides "Built on Frappe" in the website footer, per site.
update_website_context = "flewops_whitelabel.branding.update_website_context"
