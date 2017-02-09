from unittest import TestCase
import json

import photosynq_py as ps

def loadTestJson( file ):
    with open(file, "rb") as testinfo_file:
        result_bytes = testinfo_file.read()
    return json.loads( result_bytes.decode('utf-8') )
        
class buildDataFrame_test(TestCase):
    def test_buildDataFrame(self):
        testdata = loadTestJson( "tests/testdata" )["data"]
        testinfo = loadTestJson( "tests/testinfo" )["project"]
        print( "testinfo.keys(): " + str(testinfo.keys()) )
        ps.buildProjectDataFrame( testinfo, testdata )