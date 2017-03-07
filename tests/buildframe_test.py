"""
Test file corresponding with photosynq_py.buildframe
"""

from numbers import Number
from datetime import datetime
import json

from unittest import TestCase
from pandas import DataFrame
import numpy

import photosynq_py as ps

IGNORABLE_CSV_HEADERS = ["Series", "Repeat", "Color", "ecs_r_squared"]

def load_test_json(file):
    """
    load a json structure from a file
    """
    with open(file, "rb") as test_info_file:
        result_bytes = test_info_file.read()
    return json.loads(result_bytes.decode('utf-8'))

class BuildframeTest(TestCase):
    """
    Test class corresponding with photosynq_py.buildframe
    """

    def test_build_project_dataframe(self):
        """
        Load canned json structures from test resources, pass them to
        :func:`~photosynq_py.buildframe.build_project_dataframe`, and assert that the resulting
        dataframe matches a canned csv.
        """
        # load test resources
        resource_folder = "tests/resources/"
        test_info = load_test_json(resource_folder + "1224_info_from_api")["project"]
        test_data = load_test_json(resource_folder + "1224_data_from_api")["data"]
        csv_dataframe = DataFrame.from_csv(resource_folder + "1224_csv_from_website.csv")

        # build a dataframe
        built_dataframe = ps.build_project_dataframe(test_info, test_data)
        built_dataframe = built_dataframe \
            .loc[built_dataframe['protocol'] == 'Leaf Photosynthesis MultispeQ V1.0']

        # assert that built data frame "datum_id" values match the "ID" column in the csv
        csv_ids = list(csv_dataframe.index)
        print(str(built_dataframe['datum_id']))
        builtDatumIds = list(built_dataframe['datum_id'])
        self.assertListEqual(csv_ids, builtDatumIds, "build_project_dataframe() result datum_ids \
                        do not match the ID column in test resources csv")

        #deubg
        print( "csv columns: " + str( csv_dataframe.columns ) );
        print( "built columns: " + str( built_dataframe.columns ) );
        
        # assert that each column in the csv exists in the built dataframe
        built_keys = built_dataframe.columns
        for csv_col_header in csv_dataframe.columns:
            if csv_col_header in IGNORABLE_CSV_HEADERS:
                continue
            self.assertIn(csv_col_header, built_keys,
                          "buildProjectDataFrame() result is missing header \"{0}\", \
                          which is present in test resources csv".format(csv_col_header))

            # assert that this column's content match between the csv and the built dataframe
            print("testing consistency with csv values in column " + csv_col_header)
            csv_col_data = list(csv_dataframe[csv_col_header])
            built_col_data = list(built_dataframe[csv_col_header][:])
            if csv_col_header == "time":
                csv_col_data = [datetime.strptime(x, '%m/%d/%Y %I:%M %p') for x in csv_col_data]
                built_col_data = [datetime.strptime(x, ps.TIME_FORMAT) for x in built_col_data]
                built_col_data = [datetime(x.year, x.month, x.day, x.hour, x.minute) \
                    for x in built_col_data]
            if isinstance(built_col_data[0], Number) or isinstance(csv_col_data[0], Number):
                csv_col_data = numpy.asarray( \
                    [None if x == 'null' else x for x in csv_col_data], dtype=float)
                built_col_data = numpy.asarray( \
                    [None if x == 'null' else x for x in built_col_data], dtype=float)
                numpy.testing.assert_array_almost_equal(csv_col_data, built_col_data, \
                    err_msg="buildProjectDataFrame() result \"{0}\" numerical values do not match \
                    the corresponding column in the test resources csv".format(csv_col_header))
            else:
                csv_col_data = [None if x == 'null' else x for x in csv_col_data]
                self.assertListEqual(csv_col_data, built_col_data,
                            "buildProjectDataFrame() result \"{0}\" values do not match the \
                            corresponding column in the test resources csv".format(csv_col_header))
