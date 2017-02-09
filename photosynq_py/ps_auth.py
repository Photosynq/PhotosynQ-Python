import getpass
import requests

user_email = None
auth_token = None

def logout():
    global auth_token
    global user_email
    if auth_token is None:
        raise Exception( "not logged in." )
    r = requests.delete(api_url + "/sign_out.json", data = { "auth_token":auth_token } )
    content = getJsonContent( r )
    if "notice" in content.keys():
        print( content["notice"] )
    auth_token = None
    user_email = None

def login( u_email = None ):
    global auth_token
    global user_email
    if auth_token is not None:
        raise Exception( "already logged in as " + user_email + ". Use logout() to logout before logging in again" )
    if u_email is None:
        user_email = input( "enter your PhotosynQ account email: " )
    else:
        user_email = u_email
    password = getpass.getpass( "enter your PhotosynQ password for " + user_email + ": " )
    r = requests.post( api_url + "/sign_in.json", data = { "user[email]":user_email,"user[password]":password } )
    if r.status_code == 500:
        raise Exception( "invalid email/password combination" )
    content = getJsonContent( r )
    if "error" in content.keys():
        raise Exception( content["error"] )
    auth_token = content["user"]["auth_token"]