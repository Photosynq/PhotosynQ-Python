import getpass
import requests

import photosynq_py.globalVars as gvars
import photosynq_py.getJson as getJson


def login( u_email = None ):
    """
    Login to the PhotosynQ API using your PhotosynQ account email address and password.
    
    This function must be called before making any requests (see :func:`~photosynq_py.buildDataFrame.getProjectDataFrame`)
    
    You will be prompted to type their email address (if it is not provided as an argument) and password.
    
    :param u_email: (optional) the PhotosynQ account email address to use for logging in. If not provided, you will be prompted to enter an email address.
    :raises Exception: if you are already logged in, the given login information is invalid, or an I/O exception occurs
    """
    if gvars.auth_token is not None:
        raise Exception( "already logged in as " + gvars.user_email + ". Use logout() to logout before logging in again" )
    if u_email is None:
        gvars.user_email = input( "enter your PhotosynQ account email: " )
    else:
        gvars.user_email = u_email
    password = getpass.getpass( "enter your PhotosynQ password for " + gvars.user_email + ": " )
    r = requests.post( gvars.api_url + "/sign_in.json", data = { "user[email]":gvars.user_email,"user[password]":password } )
    if r.status_code == 500:
        raise Exception( "invalid email/password combination" )
    content = getJson.getJsonContent( r )
    if "error" in content.keys():
        raise Exception( content["error"] )
    gvars.auth_token = content["user"]["auth_token"]


def logout():
    """
    Logout of the PhotosynQ API.
    
    This function is not strictly necessary, but may take some pressure off of the PhotosynQ website API.
    
    :raises Exception: if you are not logged in (see :func:`~photosynq_py.auth.login`), or an I/O exception occurs.
    """
    if gvars.auth_token is None:
        raise Exception( "not logged in." )
    r = requests.delete(gvars.api_url + "/sign_out.json", data = { "auth_token":gvars.auth_token } )
    content = getJson.getJsonContent( r )
    if "notice" in content.keys():
        print( content["notice"] )
    gvars.auth_token = None
    gvars.user_email = None