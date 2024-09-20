import logging
import os
import unittest

from amadeus import ResponseError, Client
from dotenv import load_dotenv
from config import TestArguments

logger = logging.getLogger(__name__)


class TestFlighProviders(unittest.TestCase):

    def setUp(self):

        self.argument = TestArguments()
        logging.basicConfig(level=logging.getLevelName(self.argument.log_level))
        logging.debug(f"Env file {self.argument.env_file}")

        load_dotenv(self.argument.env_file)


    def testAmadeusAPI(self):
        apikey = os.getenv("AMADEUS_API_KEY")
        apisecret = os.getenv("AMADEUS_SECRET_KEY")

        self.assertIsNotNone(apikey)
        self.assertIsNotNone(apisecret)

        amadeus = Client(
            client_id=apikey,
            client_secret=apisecret
        )

        try:

            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode='MAD',
                destinationLocationCode='ATH',
                departureDate='2024-11-01',
                adults=1)

            self.assertTrue(len(response.data) > 0)

            # https://developers.amadeus.com/self-service/category/flights/api-doc/airline-code-lookup/api-reference
            response = amadeus.get('/v1/reference-data/airlines', airlineCodes='LH')

            self.assertTrue(len(response.data) > 0)
            self.assertTrue((response.data[0]["businessName"] is not None))

        except ResponseError as error:
            print(error.response.body)
            self.fail(error.response.body)


if __name__ == '__main__':
    unittest.main()
