"""
Test file corresponding with photosynq_py.buildframe
"""

from numbers import Number
from datetime import datetime
from unittest import TestCase
from pandas import DataFrame
import json
import numpy as np
import photosynq_py as ps

RESOURCE_FOLDER = "tests/resources/"
PS_PROTOCOL_TO_TEST = 'Leaf Photosynthesis MultispeQ V1.0'
IGNORABLE_CSV_HEADERS = ["Series", "Repeat", "Color", "ecs_r_squared"]

class BuildframeTest(TestCase):
    """
    Test class corresponding with photosynq_py.buildframe
    """
    
    def setUp(self):
        """
        Load json structures taken from the photosynq API, 
        as well as a corresponding csv taken from the photosynq website
        """
        self.test_info = self.load_json(RESOURCE_FOLDER + "1224_info_from_api")["project"]
        self.test_data = self.load_json(RESOURCE_FOLDER + "1224_data_from_api")["data"]
        self.resource_dataframe = DataFrame.from_csv(RESOURCE_FOLDER + "1224_csv_from_website.csv")
        
    
    def test_build_project_dataframe(self):
        """
        Pass canned json structures to
        :func:`~photosynq_py.buildframe.build_project_dataframe`, 
        and assert that the resulting dataframe matches a canned csv.
        """

        # build a dataframe
        built_dataframe = ps.build_project_dataframe(self.test_info, self.test_data)
        built_dataframe = built_dataframe[PS_PROTOCOL_TO_TEST]

        # assert that built dataframe "datum_id" values match the "ID" column in the csv
        csv_ids = list(self.resource_dataframe.index)
        builtDatumIds = list(built_dataframe['datum_id'])
        self.assertListEqual(csv_ids, builtDatumIds, "build_project_dataframe() result datum_ids \
                        do not match the ID column in test resources csv")

        #deubg
        print( "test-resource columns: " + str( self.resource_dataframe.columns ) );
        print( "built dataframe columns: " + str( built_dataframe.columns ) );
        
        # iterate through each relevant column in the csv
        for header in self.resource_dataframe.columns:
            if header in IGNORABLE_CSV_HEADERS:
                continue
                
            # assert that the column header exists in the built dataframe
            self.assertIn(header, built_dataframe.columns,
                          "buildProjectDataFrame() result is missing header \"{0}\", \
                          which is present in test resources csv".format(header))

            # assert that this column's contents match between the csv and the built dataframe
            (csv_col_data, built_col_data) = self.extract_column_data( header, built_dataframe )       
            self.assert_columns_match( csv_col_data, built_col_data, header )

    def assert_columns_match( self, csv_col_data, built_col_data, header ):
        """
        Assert that the two given lists/arrays are equivalent, accounting for the type of data they contain
        """
        
        # for numerical arrays, use a numpy testing method that allows for insignifcant differences due to number formatting
        if isinstance(built_col_data, np.ndarray):
            np.testing.assert_array_almost_equal(csv_col_data, built_col_data, \
                err_msg="buildProjectDataFrame() result \"{0}\" numerical values do not match \
                the corresponding column in the test resources csv".format(header))
                
        # otherwise, assert that the two lists are exactly the same
        else:
            self.assertListEqual(csv_col_data, built_col_data,
                        "buildProjectDataFrame() result \"{0}\" values do not match the \
                        corresponding column in the test resources csv".format(header))    
        
                    
    def extract_column_data( self, header, built_dataframe ):
        """
        Extract data for one column into a common format, from both the canned csv dataframe and the given dataframe generated from json structures.
        """
    
        # retrieve raw column contents from both the canned csv and the dataframe generated from json
        csv_col_data = list(self.resource_dataframe[header])
        built_col_data = list(built_dataframe[header][:])
        
        # if necessary, convert time data to a common format
        if header == "time":
            csv_col_data = [datetime.strptime(x, '%m/%d/%Y %I:%M %p') for x in csv_col_data]
            built_col_data = [datetime.strptime(x, ps.TIME_FORMAT) for x in built_col_data]
            built_col_data = [datetime(x.year, x.month, x.day, x.hour, x.minute) \
                for x in built_col_data]
                
        # if necessary, convert numerical data to numpy arrays, 
        elif isinstance(built_col_data[0], Number) or isinstance(csv_col_data[0], Number):
            csv_col_data = np.asarray( \
                [None if x == 'null' else x for x in csv_col_data], dtype=float)
            built_col_data = np.asarray( \
                [None if x == 'null' else x for x in built_col_data], dtype=float)
                
        # otherwise, just replace "null" entries with None
        else:
            csv_col_data = [None if x == 'null' else x for x in csv_col_data]
                
        # return both sets of column contents
        return (csv_col_data, built_col_data)
                            
                            
    def load_json(self, file):
        """
        load a json structure from a file
        """
        with open(file, "rb") as test_info_file:
            result_bytes = test_info_file.read()
        return json.loads(result_bytes.decode('utf-8'))
