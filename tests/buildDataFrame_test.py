from unittest import TestCase
from pandas import DataFrame
import json

import photosynq_py as ps

def loadTestJson( file ):
    with open(file, "rb") as testinfo_file:
        result_bytes = testinfo_file.read()
    return json.loads( result_bytes.decode('utf-8') )
        
ignorableCsvHeaders = [ "Series", "Repeat" ]
    
class buildDataFrame_test(TestCase):
    def test_buildDataFrame(self):
        
        # load test resources
        resourceFolder = "tests/resources/"
        testInfo = loadTestJson( resourceFolder + "1224_info_from_api" )["project"]
        testData = loadTestJson( resourceFolder + "1224_data_from_api" )["data"]
        csvDataFrame = DataFrame.from_csv( resourceFolder + "1224_csv_from_website.csv" )

        # build a dataframe 
        builtDataFrame = ps.buildProjectDataFrame( testInfo, testData )
        
        # compare the built dataframe to the one loaded from csv resource
        builtDataKeys = builtDataFrame['Leaf Photosynthesis MultispeQ V1.0'].keys()
        for csvColumnHeader in csvDataFrame.columns:
            if csvColumnHeader in ignorableCsvHeaders:
                continue;
            self.assertIn( csvColumnHeader, builtDataKeys, "buildProjectDataFrame() result is missing header \"{0}\", which is present in test resources csv".format( csvColumnHeader ) )
            
            csvColumnData =  list(csvDataFrame[csvColumnHeader])
            builtColumnData = builtDataFrame['Leaf Photosynthesis MultispeQ V1.0'][csvColumnHeader]
            self.assertListEqual( csvColumnData, builtColumnData, "buildProjectDataFrame() result \"{0}\" values do not match the corresponding column in the test resources csv".format( csvColumnHeader ) ) 
           
            