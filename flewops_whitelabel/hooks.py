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
app_include_js = "/assets/flewops_whitelabel/js/flewops_whitelabel.js"

# Installation
# ------------

before_install = "flewops_whitelabel.install.before_install"
after_install = "flewops_whitelabel.install.after_install"

# Updates to Frappe or ERPNext can reset what the branding wrote, so it is written again after
# every migrate.
after_migrate = "flewops_whitelabel.branding.apply"

# Boot / website context
# ----------------------

# Rebrands the app tiles (apps screen, dock, sidebar header) and hands the desk script its flags.
boot_session = "flewops_whitelabel.branding.boot_session"

# Hides "Built on Frappe" in the website footer, per site.
update_website_context = "flewops_whitelabel.branding.update_website_context"
