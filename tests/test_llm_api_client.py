import unittest
import os
import requests
from unittest.mock import mock_open, patch

from src.llm_api_client import read_context_file
from src.llm_api_client import update_context_file
from src.llm_api_client import context_exists

class TestReadContextFile(unittest.TestCase):

    @patch('src.llm_api_client.open', mock_open(read_data="123456"))
    def test_read_context_file(self):
        self.assertEqual(read_context_file(), "123456")

    def test_read_context_file_no_file(self):
        self.assertRaises(FileNotFoundError, read_context_file)

class TestUpdateContextFile(unittest.TestCase):

    def test_update_with_correct_id(self):
        correct_context = "12345"

        # Uploading the id to locally created file
        update_context_file(correct_context)

        # check the contents of the file
        with open("./.context", "r") as context_file:
            read_context_id = context_file.read()
            self.assertEqual(correct_context, read_context_id)

        # Cleanup
        os.remove("./.context")
        
    def test_update_with_incorrect_id(self):
        incorrect_context = "abc123"

        self.assertRaises(ValueError, update_context_file, incorrect_context)
    
class TestContextExists(unittest.TestCase):

    # Testing to see if the correct endpoint being called
    @patch("src.llm_api_client.requests.get")
    def test_server_context_file_exists(self, mock_requests_get):
        endpoint = "context_exists/"
        test_url = "10.0.0.1/"
        test_context_id = "1234"

        request_url = "".join([test_url, endpoint])

        # Return json message
        mock_response_byte_data = b'{"data" : "True"}'

        # Return object
        mock_response = requests.Response()
        mock_response._content = mock_response_byte_data

        # Setting the return object for the requests get
        mock_requests_get.return_value = mock_response

        json_response = context_exists(test_url, test_context_id)

        # Checking if the proper json was returned along with the proper endpoint with params being called
        mock_requests_get.assert_called_once_with(request_url, params={"context_id" : test_context_id})
        self.assertEqual(json_response, mock_requests_get.return_value.json())
        
def testReadContextFileSuite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestReadContextFile))
    suite.addTest(unittest.makeSuite(TestUpdateContextFile))
    suite.addTest(unittest.makeSuite(TestContextExists))

    return suite

if __name__ == "__main__":
    # Initializing the test suite for organizational purporses
    suite = testReadContextFileSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
