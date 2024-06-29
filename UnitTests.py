import unittest
import http.client
import json
import requests
class UnitTestCase(unittest.TestCase):

    def test_SingleCall(self):
        response = requests.post(headers={"Content-Type": "application/json"},
                                 json={'artist': 'Radiohead', 'title': 'Creep'},
                                 # json=serialized,
                                 url="http://127.0.0.1:5000/getsuggestion")
        print(response.content)

        res = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone("success", res['status'])
        print("Result",res['result'])
        self.assertIsNotNone(res['result'])


if __name__ == '__main__':
    unittest.main()
