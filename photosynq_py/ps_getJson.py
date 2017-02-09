import json
  
def getJsonContent( response ):
    return json.loads( response.content.decode('utf-8') )
    

def getProjectInfo( projectId ):
    if auth_token is None:
        raise Exception( "not logged in." )
    r = requests.get(api_url + "/projects/" + str(projectId) + ".json?user_email=" + user_email + "&user_token=" + auth_token )
    content = getJsonContent( r )
    return content["project"];
    
def getProjectData( projectId, include_raw_data = False ):
    if auth_token is None:
        raise Exception( "not logged in." )
    r = requests.get(api_url + "/projects/" + str(projectId) + "/data.json?user_email=" + user_email + "&user_token=" + auth_token + "&upd=true&include_raw_data=" + str(include_raw_data) )
    content = getJsonContent( r )
    return content["data"];