import os
import time
import unittest
import json
import requests
from dotenv import load_dotenv

from config import TestArguments


class APIUnitTestCase(unittest.TestCase):

    def setUp(self):
        arguments = TestArguments()
        if os.getenv("MONGODB_CONNECTION_STRING") is None and os.path.exists(arguments.env_file):
            load_dotenv(arguments.env_file)

    def test_Suggestion_SingleCall(self):
        response = requests.post(headers={"Content-Type": "application/json"},
                                 json={'artist': 'Radiohead', 'title': 'Creep'},
                                 url="http://127.0.0.1:5000/getsuggestion")

        res = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone("success", res['status'])
        self.assertIsNotNone(res['result'])
        self.assertIsNotNone(res['result']['recommendations'])
        self.assertIsNotNone(res['result']['sentiments'])
        self.assertTrue(len(res['result']['recommendations']) > 0)
        self.assertTrue(len(res['result']['sentiments']) > 0)

        self.assertTrue("offers" in res['result']['recommendations'][0])
        self.assertTrue(len(res['result']['recommendations'][0]["offers"]) > 0 )

        dataString = json.dumps(res, indent=4)
        print(dataString)





if __name__ == '__main__':
    unittest.main()
