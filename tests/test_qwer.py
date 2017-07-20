from qwer.qwer import qwer
import unittest 

class QwerTests(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        # creates a test client
        self.qwer = qwer.qwer.test_client()
        # propagate the exceptions to the test client
        self.qwer.testing = True 

    def tearDown(self):
        pass 

    def test_home_status_code(self):
        # sends HTTP GET request to root and assert status is 200
        result = self.qwer.get('/') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200) 

    def test_home_data(self):
        # sends HTTP GET request to root and assert data in response is correct
        # on the specified path
        result = self.qwer.get('/') 

        # assert the response data
        self.assertEqual(result.data, ('{"data": {}, "links": '
            '{"check job status": "http://127.0.0.1:5000/job?id=[id]", '
            '"self": "http://127.0.0.1:5000/", "start a job": "http://127.0.0.1:5000/job"}}'))