"""
Provides a login() function that should be called before querying the Photosynq API.
"""

import getpass
import requests

import photosynq_py.globals as gvars
import photosynq_py.getjson as getJson


def login(u_email=None, api_domain=gvars.DEFAULT_API_DOMAIN):
    """
    Login to the PhotosynQ API using your PhotosynQ account email address and password.

    This function must be called before making any requests
    (see :func:`~photosynq_py.buildframe.get_project_dataframe`)

    You will be prompted to type their email address (if it is not provided as an argument) and
    password.

    :param u_email: (optional) the PhotosynQ account email address to use for logging in. If not
        provided, you will be prompted to enter an email address.
    :param api_domain: (optional) the domain name for making queries. Default is "https://photosynq.org"
    :raises Exception: if you are already logged in, the given login information is invalid,
        or an I/O exception occurs
    """
    gvars.API_DOMAIN = api_domain
    if gvars.AUTH_TOKEN is not None:
        raise Exception("Already logged in as {0}. Use logout() first.".format(gvars.USER_EMAIL))
    if u_email is None:
        gvars.USER_EMAIL = input("Enter your PhotosynQ account email: ")
    else:
        gvars.USER_EMAIL = u_email
    password = getpass.getpass("Enter your PhotosynQ password for " + gvars.USER_EMAIL + ": ")
    req_data = {"user[email]":gvars.USER_EMAIL, "user[password]":password}

    rsp = requests.post( gvars.get_api_url() + "/sign_in.json", 
                    data = req_data,
                    headers = {"user-agent": "photosynq/1.6.2"}
                    )

    if rsp.status_code != 200:
        raise Exception("Server responeded with status {0} - {1}".format(rsp.status_code, rsp.reason))
    
    else:
        content = rsp.json()
    
    if content["status"] == "success":
        gvars.AUTH_TOKEN = content["user"]["auth_token"]
        print("Logged in successfully as {0}".format(gvars.USER_EMAIL))
    
    elif content["status"] == "failed":
        raise Exception(content["notice"])

    else:
        raise Exception("Unknown Status: {0}".format(content["status"]))


def logout():
    """
    Logout of the PhotosynQ API.

    This function is not strictly necessary, but may take some pressure off of the PhotosynQ
    website API.

    :raises Exception: if you are not logged in (see :func:`~photosynq_py.auth.login`), or an I/O
        exception occurs.
    """
    if gvars.AUTH_TOKEN is None:
        raise Exception("not logged in.")
    # rsp = requests.delete(gvars.get_api_url() + "/sign_out.json", data={"auth_token":gvars.AUTH_TOKEN})
    # content = getJson.get_json_content(rsp)
    # if "notice" in content.keys():
    #     print(content["notice"])
    gvars.AUTH_TOKEN = None
    gvars.USER_EMAIL = None
