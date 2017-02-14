from pandas import DataFrame, Series
from numpy import nan
import numpy
from datetime import datetime

import photosynq_py.getJson as getJson

time_format = '%m/%d/%Y, %H:%M:%S %p'

def getProjectDataFrame( projectId, include_raw_data = False  ):
    """
    Get a DataFrame for the given PhotosynQ project.
    
    This function calls :func:`~photosynq_py.getJson.getProjectInfo` and :func:`~photosynq_py.getJson.getProjectData`, and then combines the project info and data into one dataframe using :func:`~photosynq_py.buildDataFrame.buildProjectDataFrame`.
    
    :param projectId: the ID number for the PhotosynQ project to retrieve info and data from.
    :param include_raw_data: True if raw data should be requested and included in the result (default False)
    :returns: a dataframe containing project info and data, created by calling :func:`~photosynq_py.buildDataFrame.buildProjectDataFrame`
    :raises Exception: if an I/O exception occurs or the user is not logged in. (see :func:`~photosynq_py.auth.login`)
    """
    project_info = getJson.getProjectInfo( projectId )
    project_data = getJson.getProjectData( projectId, include_raw_data )
    return buildProjectDataFrame( project_info, project_data )
    
    
def buildProjectDataFrame( project_info, project_data ):
    """
    Get a DataFrame for the given PhotosynQ project info and data.
    
    This function is intended for use within :func:`~photosynq_py.buildDataFrame.getProjectDataFrame`, or for advanced users that need to retrieve project info/data as a separate step.
    
    Normal users should use :func:`~photosynq_py.buildDataFrame.getProjectDataFrame` instead.
    
    :param project_info: the project info json, typically retrieved using :func:`~photosynq_py.getJson.getProjectInfo`
    :param project_data: the project data json, normally retrieved using :func:`~photosynq_py.getJson.getProjectData`
    :returns: a dataframe containing project info and data
    :raises Exception: if the parameters are mismatched or malformed
    """
    if project_info is None:
        raise Exception( "Project info missing" )
    if project_data is None:
        raise Exception( "Project data missing" )

    # Print Project data receival information
    print("Project data received, generating dataframe.")
    
    # Exclusion list
    ToExclude = ["protocol_number","protocol_id","id","protocol_name","baseline_values","chlorophyll_spad_calibration","averages","data_raw","baseline_sample","HTML","Macro","GraphType","time","time_offset","get_ir_baseline","get_blank_cal","get_userdef0","get_userdef1","get_userdef2","get_userdef3","get_userdef4","get_userdef5","get_userdef6","get_userdef7","get_userdef8","get_userdef9","get_userdef10","get_userdef11","get_userdef12","get_userdef13","get_userdef14","get_userdef15","get_userdef16","get_userdef17","get_userdef18","get_userdef19","get_userdef20","r","g","b","recall","messages","order"]
    
    # Since we have all the information ready
    # now it is time to preprocess the data
    
    # Let's count the protocols first, to see which ones we actually need
    # and generate a lookup table
    protocols = {}
    for protocol in project_info["protocols"]:
        protocols[str(protocol["id"])] = { "name": protocol["name"], "parameters": [], "count": 0 }
    
    # Add counter for custom data
    protocols["custom"] = { "name":"Imported Data (Custom Data)", "parameters":[], "count":0 }
    
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
        if not "user_answers" in sampleindex.keys(): # || typeof(sampleindex$user_answers) == "character")
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
                protocols[protocolkey] = { "parameters": None }

            # protocols[[protocol_key]]$parameters <- c(protocols[[protocol_key]]$parameters, names(sampleprotocol))
            if (not "parameters" in protocols[protocolkey].keys()) or ( protocols[protocolkey]["parameters"] is None ):
                protocols[protocolkey]["parameters"] = []
            for key in sampleprotocol.keys():
                if not key in protocols[protocolkey]["parameters"]:
                    protocols[protocolkey]["parameters"].append( key )
                      
            # Add Dummy for unknown protocols
            if not str(sampleprotocol["protocol_id"]) in protocols.keys():
                protocols[str(sampleprotocol["protocol_id"])] = { "name": "Unknown Protocol (ID: " + sampleprotocol["protocol_id"] + ")", "parameters": [], "count": 0 }
            else:
                if not "count" in protocols[str(sampleprotocol["protocol_id"])].keys():
                    protocols[str(sampleprotocol["protocol_id"])]["count"] = 1
                else:
                    protocols[str(sampleprotocol["protocol_id"])]["count"] = protocols[str(sampleprotocol["protocol_id"])]["count"] + 1
    
            # Check if there is custom data
            if "custom" in sampleindex.keys():
                protocols["custom"] = protocols["custom"] + 1

    
    for p in protocols.keys():
        protocols[p]["parameters"] = unique(protocols[p]["parameters"])
    
    # Now that the preprocessing is done, we can start putting 
    # the data into the data frame
    
    allParams = ["datum_id","time","user_id","device_id","status","notes","longitude","latitute","protocol"]
    for p in protocols.keys():
        if protocols[p]["count"] == 0:
            continue
        for a in answers.keys():
            if not a in allParams:
                allParams.append( a )
        # Add the protocol to the list
        for i in range(len(protocols[p]["parameters"])):
            newKey = str(protocols[p]["parameters"][i])
            if (not newKey in ToExclude) and (not newKey in allParams):
                allParams.append( newKey )

    spreadsheet = DataFrame( columns=allParams );
    spreadsheetRowIndex = 0

    for measurement in project_data:
        
        if not "location" in measurement.keys():
            measurement["location"] = [None,None]
        
        for prot in measurement["sample"]:
            
            measurementDict = { "protocol":str(prot["protocol_id"]) }
            
            for param in allParams:
    
                if param == "datum_id":
                    measurementDict["datum_id"] = measurement["datum_id"]
                        
                elif param == "time":
                    unix_time = int(prot[str(param)])/1000
                    time = datetime.utcfromtimestamp(unix_time).strftime(time_format)
                    measurementDict["time"] = str(time)                    
                        
                elif param == "user_id":
                    measurementDict["user_id"] = str(measurement["user_id"]) 
                        
                elif param == "device_id":
                    measurementDict["device_id"] = str(measurement["device_id"]) 
                          
                elif param == "longitude":
                    measurementDict["longitude"] = str(measurement["location"][0])                                                    
    
                elif param == "latitute":
                    measurementDict["latitute"] = str(measurement["location"][1]) 
    
                elif param == "notes":
                    noteValue = None
                    if "note" in measurement.keys():
                        noteValue = measurement["note"]
                    measurementDict["notes"] = str(noteValue) 
    
                elif param == "status":
                    measurementDict["status"] = str(measurement["status"]) 
    
                elif param.startswith( "answer_" ):
                    answer_index = param.split( "_" )[1]
                    answer = None
                    if answer_index in measurement["user_answers"].keys():
                        answer = measurement["user_answers"][answer_index]
                    measurementDict[param] = answer
                    
                elif str(param) in prot.keys():
                    value = prot[str(param)]
                    if value == 'NA':
                        value = nan
                    if isinstance( value, list ):
                        value = numpy.asarray( value )
                    measurementDict[param] = value
            
            spreadsheet.loc[spreadsheetRowIndex] = Series( measurementDict )
            spreadsheetRowIndex += 1
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
    for parameter in allParams:
        if parameter in answers.keys():
            print( "based on user answers, renaming column \"{0}\" to \"{1}\"".format( parameter, answers[parameter] ) )
            spreadsheet.rename(columns={parameter: answers[parameter]}, inplace=True)
            
    for protocol in unique( spreadsheet['protocol'] ):
        if str(protocol) in protocols.keys() and "name" in protocols[str(protocol)].keys():
            newKey = protocols[str(protocol)]["name"]
            print( "based on protocol names in project info, renaming protocol \"{0}\" to \"{1}\"".format( protocol, newKey ) )
            spreadsheet['protocol'] = [newKey if x == protocol else x for x in spreadsheet['protocol']]
            
            
            #spreadsheet.rename(index={protocol: newKey}, inplace=True)
            
    #convert lists to numpy arrays
        
    # result = DataFrame( spreadsheet )
    return spreadsheet

    
def unique(seq, keepstr=True):
    t = type(seq)
    if t==str:
        t = (list, ''.join)[bool(keepstr)]
    seen = []
    return t(c for c in seq if not (c in seen or seen.append(c)))