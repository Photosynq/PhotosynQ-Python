import json
import requests

import photosynq_py.globalVars as gvars
  
def getJsonContent( response ):
    return json.loads( response.content.decode('utf-8') )
    
def getProjectInfo( projectId ):
    """
    Get info for the given PhotosynQ project.
    
    This function is intended for use within :func:`~photosynq_py.buildDataFrame.getProjectDataFrame`, or for advanced users that need to retrieve project info as a separate step.
    
    Normal users should use :func:`~photosynq_py.buildDataFrame.getProjectDataFrame` instead.
    
    :param projectId: the ID number for the PhotosynQ project to retrieve info from.
    :returns: a json string containing info for the given project
    :raises Exception: if an I/O exception occurs or the user is not logged in. (see :func:`~photosynq_py.auth.login`)
    """
    if gvars.auth_token is None:
        raise Exception( "not logged in." )
    r = requests.get(gvars.api_url + "/projects/" + str(projectId) + ".json?user_email=" + gvars.user_email + "&user_token=" + gvars.auth_token )
    content = getJsonContent( r )
    return content["project"];
    
def getProjectData( projectId, include_raw_data = False ):
    """
    Get data for the given PhotosynQ project.
    
    This function is intended for use within :func:`~photosynq_py.buildDataFrame.getProjectDataFrame`, or for advanced users that need to retrieve project info as a separate step.
    
    Normal users should use :func:`~photosynq_py.buildDataFrame.getProjectDataFrame` instead.
    
    :param projectId: the ID number for the PhotosynQ project to retrieve data from.
    :returns: a json string containing data for the given project
    :raises Exception: if an I/O exception occurs or the user is not logged in. (see :func:`~photosynq_py.auth.login`)
    """
    if gvars.auth_token is None:
        raise Exception( "not logged in." )
    r = requests.get(gvars.api_url + "/projects/" + str(projectId) + "/data.json?user_email=" + gvars.user_email + "&user_token=" + gvars.auth_token + "&upd=true&include_raw_data=" + str(include_raw_data) )
    content = getJsonContent( r )
    return content["data"];