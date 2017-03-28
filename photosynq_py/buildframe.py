"""
Creates accessible dataframes from Photosynq project info and project data json structures.
"""

from datetime import datetime
from pandas import DataFrame, Series
from numpy import nan
import numpy

import photosynq_py.getjson as getJson

TIME_FORMAT = '%m/%d/%Y, %H:%M:%S %p'

DEFAULT_PARAMS = [
    "datum_id", "time", "user_id", "device_id", "status", "notes", "longitude", "latitute",
    "protocol"
]

PARAMS_TO_EXCLUDE = [
    "protocol_number", "protocol_id", "id", "protocol_name", "baseline_values",
    "chlorophyll_spad_calibration", "averages", "data_raw", "baseline_sample", "HTML", "Macro",
    "GraphType", "time", "time_offset", "get_ir_baseline", "get_blank_cal", "get_userdef0",
    "get_userdef1", "get_userdef2", "get_userdef3", "get_userdef4", "get_userdef5",
    "get_userdef6", "get_userdef7", "get_userdef8", "get_userdef9", "get_userdef10",
    "get_userdef11", "get_userdef12", "get_userdef13", "get_userdef14", "get_userdef15",
    "get_userdef16", "get_userdef17", "get_userdef18", "get_userdef19", "get_userdef20",
    "r", "g", "b", "recall", "messages", "order"
]

def get_project_dataframe(project_id, include_raw_data=False):
    """
    Get a DataFrame for the given PhotosynQ project.

    This function calls :func:`~photosynq_py.getjson.get_project_info` and
    :func:`~photosynq_py.getjson.get_project_data`, and then combines the project info and data into
    one dataframe using :func:`~photosynq_py.buildframe.build_project_data_frame`.

    :param project_id: the ID number for the PhotosynQ project to retrieve info and data from.
    :param include_raw_data: True if raw data should be requested and included in the result
        (default False)
    :returns: a dataframe containing project info and data, created by calling
        :func:`~photosynq_py.buildframe.build_project_dataframe`
    :raises Exception: if an I/O exception occurs or the user is not logged in.
        (see :func:`~photosynq_py.auth.login`)
    """
    project_info = getJson.get_project_info(project_id)
    project_data = getJson.get_project_data(project_id, include_raw_data)
    return build_project_dataframe(project_info, project_data)


def build_project_dataframe(project_info, project_data):
    """
    Get a DataFrame for the given PhotosynQ project info and data.

    This function is intended for use within
    :func:`~photosynq_py.buildframe.get_project_dataframe`, or for advanced users that need to
    retrieve project info/data as a separate step.

    Normal users should use :func:`~photosynq_py.buildframe.get_project_dataframe` instead.

    :param project_info: the project info json, typically retrieved using
            :func:`~photosynq_py.getjson.get_project_info`
    :param project_data: the project data json, normally retrieved using
            :func:`~photosynq_py.getjson.get_project_data`
    :returns: a dataframe containing project info and data
    :raises Exception: if the parameters are mismatched or malformed
    """
    if project_info is None:
        raise Exception("Project info missing")
    if project_data is None:
        raise Exception("Project data missing")

    # Print Project data receival information
    print("Project data received, generating dataframe.")

    # Exclusion list

    # Since we have all the information ready
    # now it is time to preprocess the data

    # Let's count the protocols first, to see which ones we actually need
    # and generate a lookup table
    protocols = {}
    for protocol in project_info["protocols"]:
        protocols[str(protocol["id"])] = {"name": protocol["name"], "parameters": [], "count": 0}

    # Add counter for custom data
    protocols["custom"] = {"name":"Imported Data (Custom Data)", "parameters":[], "count":0}

    # Now we work on the actual data
    for sampleindex in project_data:

        # Remove data entries that don't have the sample key
        if not "sample" in sampleindex.keys():
            # sampleindex = NULL
            continue

        # We skip the time changes for now
        # TODO: Implement the new timestamps here

        # Make sure location is false or an array
#        if "location" in sampleindex.keys():
#            if(typeof(sampleindex$location) == "character"){
#                sampleindex$location <- strsplit(sampleindex$location,",")
#            }

#        if "time" in sampleindex.keys():
#            sampleindex$time <- sampleindex$time

        # Make sure answers are an array
        if not "user_answers" in sampleindex.keys():
            sampleindex["user_answers"] = {}

        # Loop through measurements of one sample
        for sampleprotocol in sampleindex["sample"]:

            # Skip Measurements without protocol id
            if not "protocol_id" in sampleprotocol.keys():
                continue

            # Correct timestamp
            if not "time" in sampleprotocol.keys():
                sampleprotocol["time"] = sampleindex["time"]

            # Build the user answers
            answers = {}
            for filters in project_info["filters"]:
                answers["answer_"+str(filters["id"])] = filters["label"]

            protocolkey = str(sampleprotocol["protocol_id"])
            if not protocolkey in protocols.keys():
                protocols[protocolkey] = {"parameters": None}

            if (not "parameters" in protocols[protocolkey].keys()) \
                        or (protocols[protocolkey]["parameters"] is None):
                protocols[protocolkey]["parameters"] = []
            for key in sampleprotocol.keys():
                if not key in protocols[protocolkey]["parameters"]:
                    protocols[protocolkey]["parameters"].append(key)

            # Add Dummy for unknown protocols
            if not str(sampleprotocol["protocol_id"]) in protocols.keys():
                protocols[str(sampleprotocol["protocol_id"])] = {
                    "name": "Unknown Protocol (ID: {0})".format(sampleprotocol["protocol_id"]),
                    "parameters": [],
                    "count": 0}
            else:
                if not "count" in protocols[str(sampleprotocol["protocol_id"])].keys():
                    protocols[str(sampleprotocol["protocol_id"])]["count"] = 1
                else:
                    protocols[str(sampleprotocol["protocol_id"])]["count"] = \
                    protocols[str(sampleprotocol["protocol_id"])]["count"] + 1

            # Check if there is custom data
            if "custom" in sampleindex.keys():
                protocols["custom"] = protocols["custom"] + 1


    for prot in protocols.keys():
        protocols[prot]["parameters"] = unique(protocols[prot]["parameters"])

    # Now that the preprocessing is done, we can start putting
    # the data into the data frame
    all_params = DEFAULT_PARAMS[:]
    for prot in protocols.keys():
        if protocols[prot]["count"] == 0:
            continue
        for ans in answers.keys():
            if not ans in all_params:
                all_params.append(ans)
        # Add the protocol to the list
        for i in range(len(protocols[prot]["parameters"])):
            new_key = encode_utf_8(protocols[prot]["parameters"][i])
            # new_key = str(protocols[prot]["parameters"][i])
            if (new_key not in PARAMS_TO_EXCLUDE) and (new_key not in all_params):
                all_params.append(new_key)

    spreadsheet = DataFrame(columns=all_params)
    row_index = 0

    for measurement in project_data:

        if not "location" in measurement.keys():
            measurement["location"] = [None, None]

        for prot in measurement["sample"]:

            msmnt_dict = {"protocol":str(prot["protocol_id"])}

            for param in all_params:

                if param == "datum_id":
                    msmnt_dict["datum_id"] = measurement["datum_id"]

                elif param == "time":
                    unix_time = int(prot[str(param)])/1000
                    time = datetime.utcfromtimestamp(unix_time).strftime(TIME_FORMAT)
                    msmnt_dict["time"] = str(time)

                elif param == "user_id":
                    msmnt_dict["user_id"] = str(measurement["user_id"])

                elif param == "device_id":
                    msmnt_dict["device_id"] = str(measurement["device_id"])

                elif param == "longitude":
                    msmnt_dict["longitude"] = str(measurement["location"][1])

                elif param == "latitute":
                    msmnt_dict["latitute"] = str(measurement["location"][0])

                elif param == "notes":
                    note_values = None
                    if "note" in measurement.keys():
                        note_values = measurement["note"]
                    msmnt_dict["notes"] = str(note_values)

                elif param == "status":
                    msmnt_dict["status"] = str(measurement["status"])

                elif param.startswith("answer_"):
                    answer_index = param.split("_")[1]
                    answer = None
                    if answer_index in measurement["user_answers"].keys():
                        answer = measurement["user_answers"][answer_index]
                    msmnt_dict[param] = answer

                else:
                    for key in prot.keys():
                        prot[encode_utf_8(key)] = prot.pop(key)
                    if param in prot.keys():
                        value = prot[param]
                        if value == 'NA':
                            value = nan
                        if isinstance(value, list):
                            value = numpy.asarray(value)
                        msmnt_dict[param] = value

            spreadsheet.loc[row_index] = Series(msmnt_dict)
            row_index += 1
        # append empty cells as necesary so that each column is the same length
#        n = len( spreadsheet["datum_id"][protocolID] )
#        for param in allParams:
#            while len( spreadsheet[param][protocolID] ) < n:
#                spreadsheet[param][protocolID].append( None )


#                    if type(prot[str(param)]) is list:
#                        for elem in prot[str(param)]:
#                            spreadsheet[protocolID][param].append( elem )
#                    else:
#                        spreadsheet[protocolID][param].append( prot[str(param)] )

    # switch all data to numpy arrays
#    for parameter in allParams:
#        spreadsheet[parameter] = numpy.asarray( spreadsheet[parameter] )

    # switch some parameters to human-readable names
    for parameter in all_params:
        if parameter in answers.keys():
            print("based on user answers, renaming column \"{0}\" to \"{1}\"" \
                    .format(parameter, answers[parameter]))
            spreadsheet.rename(columns={parameter: answers[parameter]}, inplace=True)

    for protocol in unique(spreadsheet['protocol']):
        if str(protocol) in protocols.keys() and "name" in protocols[str(protocol)].keys():
            new_key = protocols[str(protocol)]["name"]
            print("based on protocol names in project info, renaming protocol \"{0}\" to \"{1}\"" \
                    .format(protocol, new_key))
            spreadsheet['protocol'] \
                    = [new_key if x == protocol else x for x in spreadsheet['protocol']]


            #spreadsheet.rename(index={protocol: new_key}, inplace=True)

    #convert lists to numpy arrays

    # result = DataFrame( spreadsheet )
    return spreadsheet


def encode_utf_8(text):
    """
    Hack to encode utf-8 (if necessary) in python 2 and 3, untiI find a better way.
    """
    try:
        result = str(text.encode('utf-8'))
    except:
        return text
    if(result.startswith("b'") and result.endswith("'")):
        result = result[2:-1]
    return result

def unique(seq):
    """
    Get a list of unique elements from the given list.
    """
    seq_type = type(seq)
    if seq_type == str:
        seq_type = (list, ''.join)[True]
    seen = []
    return seq_type(c for c in seq if not (c in seen or seen.append(c)))
