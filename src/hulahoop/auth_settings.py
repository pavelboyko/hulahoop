AUTHENTICATION_BACKENDS = ("allauth.account.auth_backends.AuthenticationBackend",)

# required for Django Allauth to function
SITE_ID = 1
# turns off verification emails. Django automatically sets up an email verification workflow.
# We do not need this functionality right now.
ACCOUNT_EMAIL_VERIFICATION = "none"
# redirects the user to the homepage after a successful login
LOGIN_REDIRECT_URL = "index"
# directly logs the user out when the logout button is clicked via a GET request. This skips the confirm logout page.
ACCOUNT_LOGOUT_ON_GET = True
