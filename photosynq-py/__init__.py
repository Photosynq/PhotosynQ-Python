import requests
import getpass
import json

class Photosynq:
    api_url = "https://photosynq.org/api/v3/"
    user_email = None
    auth_token = None
    
    def getJsonContent( response ):
        return json.loads( response.content.decode('utf-8') )
    
    def logout():
        if Photosynq.auth_token is None:
            raise Exception( "not logged in." )
        r = requests.delete(Photosynq.api_url + "/sign_out.json", data = { "auth_token":Photosynq.auth_token } )
        content = Photosynq.getJsonContent( r )
        if "notice" in content.keys():
            print( content["notice"] )
        Photosynq.auth_token = None
        Photosynq.user_email = None
    
    def login():
        if Photosynq.auth_token is not None:
            raise Exception( "already logged in as " + Photosynq.user_email + ". Use logout() to logout before logging in again" )
        Photosynq.user_email = input( "enter your email: " )
        password = getpass.getpass( "enter your password: " )
        r = requests.post( Photosynq.api_url + "/sign_in.json", data = { "user[email]":Photosynq.user_email,"user[password]":password } )
        if r.status_code == 500:
            raise Exception( "invalid email/password combination" )
        content = Photosynq.getJsonContent( r )
        if "error" in content.keys():
            raise Exception( content["error"] )
        Photosynq.auth_token = content["user"]["auth_token"]
        
    def getProjectInfo( projectId ):
        if Photosynq.auth_token is None:
            raise Exception( "not logged in." )
        r = requests.get(Photosynq.api_url + "/projects/" + str(projectId) + ".json", data = { "user_token":Photosynq.auth_token, "user_email":Photosynq.user_email } )
        content = Photosynq.getJsonContent( r )
        return content;
        
    def getProjectData( projectId ):
        if Photosynq.auth_token is None:
            raise Exception( "not logged in." )
        r = requests.get(Photosynq.api_url + "/projects/" + str(projectId) + "/data.json", data = { "user_token":Photosynq.auth_token, "user_email":Photosynq.user_email, "upd":True } )
        content = Photosynq.getJsonContent( r )
        return content;
        