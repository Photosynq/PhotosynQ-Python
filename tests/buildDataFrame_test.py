from unittest import TestCase
from pandas import DataFrame
import json

import photosynq_py as ps

def loadTestJson( file ):
    with open(file, "rb") as testinfo_file:
        result_bytes = testinfo_file.read()
    return json.loads( result_bytes.decode('utf-8') )
        
class buildDataFrame_test(TestCase):
    def test_buildDataFrame(self):
        
        # load test resources
        resourceFolder = "tests/resources/"
        testInfo = loadTestJson( resourceFolder + "1224_info_from_api" )["project"]
        testData = loadTestJson( resourceFolder + "1224_data_from_api" )["data"]
        expectedDataFrame = DataFrame.from_csv( resourceFolder + "1224_csv_from_website.csv" )

        # build a dataframe 
        builtDataFrame = ps.buildProjectDataFrame( testInfo, testData )
        
        # compare the built dataframe to the one loaded from csv resource