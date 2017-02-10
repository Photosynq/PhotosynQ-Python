from unittest import TestCase
from pandas import DataFrame
from numbers import Number
import json
import numpy

import photosynq_py as ps

def loadTestJson( file ):
    with open(file, "rb") as testinfo_file:
        result_bytes = testinfo_file.read()
    return json.loads( result_bytes.decode('utf-8') )
        
ignorableCsvHeaders = [ "Series", "Repeat" ]
seriesDataColumns = [ "ECSt", "gH+", ]
    
class buildDataFrame_test(TestCase):
    def test_buildDataFrame(self):
        
        # load test resources
        resourceFolder = "tests/resources/"
        testInfo = loadTestJson( resourceFolder + "1224_info_from_api" )["project"]
        testData = loadTestJson( resourceFolder + "1224_data_from_api" )["data"]
        csvDataFrame = DataFrame.from_csv( resourceFolder + "1224_csv_from_website.csv" )

        # build a dataframe 
        builtDataFrame = ps.buildProjectDataFrame( testInfo, testData )
        
        # assert that built data frame "datum_id" values match the "ID" column in the csv
        csvIds = list( csvDataFrame.index )
        builtDatumIds = builtDataFrame['Leaf Photosynthesis MultispeQ V1.0']['datum_id']
        self.assertListEqual( csvIds, builtDatumIds, "buildProjectDataFrame() result datum_ids do not match the ID column in tst resources csv" )
        
        # assert that each column in the csv exists in the built dataframe
        builtDataKeys = builtDataFrame['Leaf Photosynthesis MultispeQ V1.0'].keys()
        for csvColumnHeader in csvDataFrame.columns:
            if csvColumnHeader in ignorableCsvHeaders:
                continue;
            self.assertIn( csvColumnHeader, builtDataKeys, "buildProjectDataFrame() result is missing header \"{0}\", which is present in test resources csv".format( csvColumnHeader ) )
            
            # assert that this column's content match between the csv and the built dataframe
            # if csvColumnHeader in seriesDataColumns:
            print( "checcking series values in column " + csvColumnHeader )
            csvColumnData = list(csvDataFrame[csvColumnHeader])
            builtColumnData = builtDataFrame['Leaf Photosynthesis MultispeQ V1.0'][csvColumnHeader]
            if isinstance( csvColumnData[0], Number ):
                numpy.testing.assert_array_almost_equal( csvColumnData, builtColumnData, err_msg="buildProjectDataFrame() result \"{0}\" numerical values do not match the corresponding column in the test resources csv".format( csvColumnHeader ) )
            else:
                csvColumnData = [None if x == 'null' else x for x in csvColumnData]
                self.assertListEqual( csvColumnData, builtColumnData, "buildProjectDataFrame() result \"{0}\" values do not match the corresponding column in the test resources csv".format( csvColumnHeader ) )