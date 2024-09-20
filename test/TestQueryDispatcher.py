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

        logger.debug(response)
        self.assertIsNotNone(response)
        self.assertEqual(response["song"], 'Africa')
        self.assertTrue(len(response["cities"]) > 0)
        self.assertTrue(len(response["sentiment"]) > 0)
        self.assertTrue(len(response["reasons_why"]) > 0)

if __name__ == '__main__':
    unittest.main()
