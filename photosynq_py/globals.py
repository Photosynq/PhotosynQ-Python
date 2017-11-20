"""
Defines global constant (URL for photosynw API) and variables (current login session info).
"""


DEFAULT_API_DOMAIN = "https://photosynq.org"
API_DOMAIN = DEFAULT_API_DOMAIN
USER_EMAIL = None
AUTH_TOKEN = None

def get_api_url():
    return API_DOMAIN + "/api/v3/"
