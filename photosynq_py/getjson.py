"""
Provides functions for retriving project info/data from the Photosynq API, in the form of json
structures.
"""

import json
import requests

import photosynq_py.globals as gvars

INFO_URL = gvars.API_URL + "/projects/{0}.json?user_email={1}&user_token={2}"

DATA_URL = gvars.API_URL + \
    "/projects/{0}/data.json?user_email={1}&user_token={2}&upd={3}&include_raw_data={4}"

def get_json_content(response):
    """
    Parse a json object from the content of the given HTTP response.
    """
    return json.loads(response.content.decode('utf-8'))

def get_project_info(project_id):
    """
    Get info for the given PhotosynQ project.

    This function is intended for use within
    :func:`~photosynq_py.buildframe.get_project_dataframe`, or for advanced users that need to
    retrieve project info as a separate step.

    Normal users should use :func:`~photosynq_py.buildframe.get_project_dataframe` instead.

    :param project_id: the ID number for the PhotosynQ project to retrieve info from.
    :returns: a json string containing info for the given project
    :raises Exception: if an I/O exception occurs or the user is not logged in.
        (see :func:`~photosynq_py.auth.login`)
    """
    if gvars.AUTH_TOKEN is None:
        raise Exception("not logged in.")
    req_url = INFO_URL.format(str(project_id), gvars.USER_EMAIL, gvars.AUTH_TOKEN)    
    rsp = requests.get(req_url)
    content = get_json_content(rsp)
    return content["project"]

def get_project_data(project_id, processed_data=True, raw_traces=False):
    """
    Get data for the given PhotosynQ project.

    This function is intended for use within
    :func:`~photosynq_py.buildframe.get_project_dataframe`, or for advanced users that need to
    retrieve project info as a separate step.

    Normal users should use :func:`~photosynq_py.buildframe.get_project_dataframe` instead.

    :param project_id: the ID number for the PhotosynQ project to retrieve data from.
    :returns: a json string containing data for the given project
    :raises Exception: if an I/O exception occurs or the user is not logged in.
        (see :func:`~photosynq_py.auth.login`)
    """
    if gvars.AUTH_TOKEN is None:
        raise Exception("not logged in.")
    req_url = DATA_URL.format(project_id, gvars.USER_EMAIL, gvars.AUTH_TOKEN, processed_data, raw_traces)
    rsp = requests.get(req_url)
    content = get_json_content(rsp)
    return content["data"]
    