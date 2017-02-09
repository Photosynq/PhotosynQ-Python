import getpass
import requests

import photosynq_py.globalVars as gvars
import photosynq_py.getJson as getJson

def logout():
    if gvars.auth_token is None:
        raise Exception( "not logged in." )
    r = requests.delete(gvars.api_url + "/sign_out.json", data = { "auth_token":gvars.auth_token } )
    content = getJson.getJsonContent( r )
    if "notice" in content.keys():
        print( content["notice"] )
    gvars.auth_token = None
    gvars.user_email = None

def login( u_email = None ):
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