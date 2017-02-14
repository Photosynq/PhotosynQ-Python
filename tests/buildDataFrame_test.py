from unittest import TestCase
from pandas import DataFrame
from numbers import Number
from datetime import datetime
import json
import numpy

import photosynq_py as ps

def loadTestJson( file ):
    with open(file, "rb") as testinfo_file:
        result_bytes = testinfo_file.read()
    return json.loads( result_bytes.decode('utf-8') )
        
ignorableCsvHeaders = [ "Series", "Repeat", "Color", "ecs_r_squared" ]
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
        builtDatumIds = list(builtDataFrame['Leaf Photosynthesis MultispeQ V1.0']['datum_id'])
        self.assertListEqual( csvIds, builtDatumIds, "buildProjectDataFrame() result datum_ids do not match the ID column in test resources csv" )
        
        # assert that each column in the csv exists in the built dataframe
        builtDataKeys = builtDataFrame['Leaf Photosynthesis MultispeQ V1.0'].keys()
        for csvColumnHeader in csvDataFrame.columns:
            if csvColumnHeader in ignorableCsvHeaders:
                continue;
            self.assertIn( csvColumnHeader, builtDataKeys, "buildProjectDataFrame() result is missing header \"{0}\", which is present in test resources csv".format( csvColumnHeader ) )
            
            # assert that this column's content match between the csv and the built dataframe
            print( "testing consistency with csv values in column " + csvColumnHeader )
            csvColumnData = list(csvDataFrame[csvColumnHeader])
            builtColumnData = list(builtDataFrame['Leaf Photosynthesis MultispeQ V1.0'][csvColumnHeader][:])
            if csvColumnHeader == "time": 
                csvColumnData = [ datetime.strptime(x, '%m/%d/%Y %I:%M %p') for x in csvColumnData] 
                builtColumnData = [ datetime.strptime(x, ps.time_format) for x in builtColumnData] 
                builtColumnData = [ datetime( x.year, x.month, x.day, x.hour, x.minute ) for x in builtColumnData] 
            if isinstance( builtColumnData[0], Number ) or isinstance( csvColumnData[0], Number ):
                csvColumnData = numpy.asarray([None if x == 'null' else x for x in csvColumnData] , dtype=float)
                builtColumnData = numpy.asarray([None if x == 'null' else x for x in builtColumnData] , dtype=float)
                numpy.testing.assert_array_almost_equal( csvColumnData, builtColumnData, err_msg="buildProjectDataFrame() result \"{0}\" numerical values do not match the corresponding column in the test resources csv".format( csvColumnHeader ) )
            else:
                csvColumnData = [None if x == 'null' else x for x in csvColumnData]
                self.assertListEqual( csvColumnData, builtColumnData, "buildProjectDataFrame() result \"{0}\" values do not match the corresponding column in the test resources csv".format( csvColumnHeader ) )