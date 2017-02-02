import requests
import getpass
import json

api_url = "https://photosynq.org/api/v3/"
user_email = None
auth_token = None

def getJsonContent( response ):
    return json.loads( response.content.decode('utf-8') )

def logout():
    global auth_token
    if auth_token is None:
        raise Exception( "not logged in." )
    r = requests.delete(api_url + "/sign_out.json", data = { "auth_token":auth_token } )
    content = getJsonContent( r )
    if "notice" in content.keys():
        print( content["notice"] )
    auth_token = None
    user_email = None

def login():
    global auth_token
    if auth_token is not None:
        raise Exception( "already logged in as " + user_email + ". Use logout() to logout before logging in again" )
    user_email = input( "enter your email: " )
    password = getpass.getpass( "enter your password: " )
    r = requests.post( api_url + "/sign_in.json", data = { "user[email]":user_email,"user[password]":password } )
    if r.status_code == 500:
        raise Exception( "invalid email/password combination" )
    content = getJsonContent( r )
    if "error" in content.keys():
        raise Exception( content["error"] )
    auth_token = content["user"]["auth_token"]
    
def getProjectInfo( projectId ):
    if auth_token is None:
        raise Exception( "not logged in." )
    r = requests.get(api_url + "/projects/" + str(projectId) + ".json", data = { "user_token":auth_token, "user_email":user_email } )
    content = getJsonContent( r )
    return content;
    
def getProjectData( projectId ):
    if auth_token is None:
        raise Exception( "not logged in." )
    r = requests.get(api_url + "/projects/" + str(projectId) + "/data.json", data = { "user_token":auth_token, "user_email":user_email, "upd":True } )
    content = getJsonContent( r )
    return content;
        