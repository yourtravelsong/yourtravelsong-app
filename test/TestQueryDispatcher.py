import json
import logging
import unittest
from dotenv import load_dotenv
import os
from config import TestArguments
from embeddings.query_dispatcher import QueryDispatcher
logger = logging.getLogger(__name__)

class QueryDispacher(unittest.TestCase):

    def setUp(self):
        self.argument = TestArguments()
        logging.basicConfig(level=logging.getLevelName(self.argument.log_level))
        load_dotenv(self.argument.env_file)

    def test_queryDispatcher(self):

        distpacher = QueryDispatcher()
        response = distpacher.get_response('Africa', 'Toto')

        responseJson = json.loads(response)

        logger.debug(responseJson)
        self.assertIsNotNone(responseJson)
        self.assertEqual(responseJson["song"], 'Africa')
        self.assertTrue(len(responseJson["cities"]) > 0)
        self.assertTrue(len(responseJson["sentiment"]) > 0)
        self.assertTrue(len(responseJson["reasons_why"]) > 0)

if __name__ == '__main__':
    unittest.main()
