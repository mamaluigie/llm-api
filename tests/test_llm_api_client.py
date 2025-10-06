import unittest
from unittest.mock import mock_open, patch

from src.llm_api_client import read_context_file

class TestReadContextFile(unittest.TestCase):

    @patch('src.llm_api_client.open', mock_open(read_data="123456"))
    def test_read_context_file(self):
        self.assertEqual(read_context_file(), "123456")

    def test_read_context_file_no_file(self):
        self.assertRaises(FileNotFoundError, read_context_file)

def TestReadContextFileSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestReadContextFile("test_read_context_file_no_file"))

    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run()

