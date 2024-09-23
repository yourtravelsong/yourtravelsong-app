import json
import logging
import os
import unittest

from amadeus import ResponseError, Client
from dotenv import load_dotenv
from config import TestArguments

logger = logging.getLogger(__name__)


class TestFlightProviders(unittest.TestCase):

    def setUp(self):

        self.argument = TestArguments()
        logging.basicConfig(level=logging.getLevelName(self.argument.log_level))

        if os.getenv("AMADEUS_API_KEY") is None and os.path.exists(self.argument.env_file):
            load_dotenv(self.argument.env_file)

        self.apikey = os.getenv("AMADEUS_API_KEY")
        self.apisecret = os.getenv("AMADEUS_SECRET_KEY")


    def testAmadeusAPI(self):


        self.assertIsNotNone(self.apikey)
        self.assertIsNotNone(self.apisecret)

        amadeus = Client(
            client_id=self.apikey,
            client_secret=self.apisecret
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


    def testGetCities(self):
        amadeus = Client(
            client_id=self.apikey,
            client_secret=self.apisecret
        )

        try:
            response = amadeus.reference_data.locations.get(
                keyword='LON',
                subType='CITY'
            )

            self.assertTrue(len(response.data) > 0)
            #print(response.data)
            print(json.dumps(response.data, indent=4))
            ## Now also airport
            response = amadeus.reference_data.locations.get(
                keyword='LON',
                subType='CITY,AIRPORT'
            )
            logger.debug("Response from Amadeus city and airport: ", response)
            self.assertTrue(len(response.data) > 0)
            # print(response.data)
            logger.debug(json.dumps(response.data, indent=4))


            ### JUST AIRPORTS

            response = amadeus.reference_data.locations.get(
                keyword='Barcelona',
                subType='AIRPORT'
            )
            logger.debug("Response from Amadeus Just airport ", response)
            self.assertTrue(len(response.data) > 0)
            logger.debug(json.dumps(response.data, indent=4))

        except ResponseError as error:
            print(error.response.body)
            self.fail(error.response.body)

if __name__ == '__main__':
    unittest.main()
