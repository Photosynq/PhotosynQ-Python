import json
import requests

import photosynq_py.globalVars as gvars
  
def getJsonContent( response ):
    return json.loads( response.content.decode('utf-8') )
    
def getProjectInfo( projectId ):
    if gvars.auth_token is None:
        raise Exception( "not logged in." )
    r = requests.get(gvars.api_url + "/projects/" + str(projectId) + ".json?user_email=" + gvars.user_email + "&user_token=" + gvars.auth_token )
    content = getJsonContent( r )
    return content["project"];
    
def getProjectData( projectId, include_raw_data = False ):
    if gvars.auth_token is None:
        raise Exception( "not logged in." )
    r = requests.get(gvars.api_url + "/projects/" + str(projectId) + "/data.json?user_email=" + gvars.user_email + "&user_token=" + gvars.auth_token + "&upd=true&include_raw_data=" + str(include_raw_data) )
    content = getJsonContent( r )
    return content["data"];