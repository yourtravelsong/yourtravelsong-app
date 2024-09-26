import json
import logging
import os
import unittest
from time import sleep

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

        self.amadeus = Client(
            client_id=self.apikey,
            client_secret=self.apisecret
        )

    def testAmadeusAPI(self):


        self.assertIsNotNone(self.apikey)
        self.assertIsNotNone(self.apisecret)

        amadeus = Client(
            client_id=self.apikey,
            client_secret=self.apisecret
        )

        try:
            sleep(1)
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode='MAD',
                destinationLocationCode='ATH',
                departureDate='2024-11-01',
                adults=1)

            logger.debug(f"Response from Amadeus: {response.data}" )
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
            sleep(1)
            response = amadeus.reference_data.locations.get(
                keyword='LON',
                subType='CITY'
            )
            logger.debug(f"Response from Amadeus city: {response.data}" )
            self.assertTrue(len(response.data) > 0)
            #print(response.data)
            #print(json.dumps(response.data, indent=4))
            ## Now also airport
            response = amadeus.reference_data.locations.get(
                keyword='LON',
                subType='CITY,AIRPORT'
            )
            logger.debug(f"Response from Amadeus city and airport: {response.data}" )
            self.assertTrue(len(response.data) > 0)
            self.assertTrue(response.data[0]["type"] == "location")
            # print(response.data)
            #logger.debug(json.dumps(response.data, indent=4))


            ### JUST AIRPORTS
            sleep(1)
            response = amadeus.reference_data.locations.get(
                keyword='Barcelona',
                subType='AIRPORT'
            )
            logger.debug(f"Response from Amadeus Just airport {response.data}" )
            self.assertTrue(len(response.data) > 0)
            self.assertTrue(response.data[0]["type"] == "location")
            #logger.debug(json.dumps(response.data, indent=4))

            aCity = "London"
            self.helperAssertCity(aCity, amadeus)

            aCity = "Barcelona"
            self.helperAssertCity(aCity, amadeus)

            aCity = "Florianopolis"
            self.helperAssertCity(aCity, amadeus)

            aCity = "Paris"
            self.helperAssertCity(aCity, amadeus)

            aCity = "Buenos Aires"
            self.helperAssertCity(aCity, amadeus)

            aCity = "Auckland"
            self.helperAssertCity(aCity, amadeus)

            aCity = "Rio de Janeiro"
            self.helperAssertCity(aCity, amadeus)

        except ResponseError as error:
            print(error.response.body)
            self.fail(error.response.body)

    def helperAssertCity(self, aCity, amadeus):
        sleep(0.5)
        response = amadeus.reference_data.locations.get(
            keyword=aCity,
            subType='CITY'
        )
        logger.debug(f"Response from Amadeus  {aCity} city : {response.data}")
        self.assertTrue(len(response.data) > 0)
        self.assertTrue(response.data[0]["type"] == "location")
        self.assertTrue(response.data[0]["subType"] == "CITY")
        self.assertTrue("geoCode" in response.data[0])


    def testURL(self):

        response = self.amadeus.get('/v1/reference-data/locations/cities', countryCode="FR", keyword='PARIS')
        logger.debug(f"Response from Amadeus city: {response.data}" )
        self.helperAssertCityApi(response)

        response = self.amadeus.get('/v1/reference-data/locations/cities', keyword='PARIS')
        logger.debug(f"Response from Amadeus city: {response.data}")
        self.helperAssertCityApi(response)
        for r in response.data:
            print(r)

        response = self.amadeus.get('/v1/reference-data/locations/cities', keyword='AUCKLAND')
        logger.debug(f"Response from Amadeus city: {response.data}")
        self.helperAssertCityApi(response)
        for r in response.data:
            print(r)

        response = self.amadeus.get('/v1/reference-data/locations/cities', keyword='Buenos Aires')
        logger.debug(f"Response from Amadeus city: {response.data}")
        self.helperAssertCityApi(response)
        for r in response.data:
            print(r)

    def helperAssertCityApi(self, response):
        self.assertTrue(len(response.data) > 0)
        self.assertTrue(response.data[0]["type"] == "location")
        self.assertTrue(response.data[0]["subType"] == "city")
        self.assertTrue("geoCode" in response.data[0])


    def testAirportsAndCities(self):
        #https://developers.amadeus.com/self-service/category/flights/api-doc/airport-and-city-search/api-reference
        ## https://test.api.amadeus.com/v1/reference-data/locations?subType=AIRPORT&keyword=MUC&page%5Blimit%5D=10&page%5Boffset%5D=0&sort=analytics.travelers.score&view=FULL
        response = self.amadeus.get('/v1/reference-data/locations', keyword='paris', subType='AIRPORT')
        logger.debug(f"Response from Amadeus city: {response.data}")
        for r in response.data:
            print(r)

        response = self.amadeus.get('/v1/reference-data/locations', keyword='paris', subType='CITY')
        logger.debug(f"Response from Amadeus city: {response.data}")
        for r in response.data:
            print(r)

        response = self.amadeus.get('/v1/reference-data/locations', keyword='EZE', subType='AIRPORT')
        logger.debug(f"Response from Amadeus city: {response.data}")
        for r in response.data:
            print(r)

    def testNearAirport(self):
        # https://developers.amadeus.com/self-service/category/flights/api-doc/airport-nearest-relevant
        ## Baires -34.61315 -58.37723
    #    response = self.amadeus.get('/v1/reference-data/locations/airports',latitude=-34.6037, longitude=-58.3816)
        response = self.amadeus.get('/v1/reference-data/locations/airports', latitude=50.8317114, longitude=4.372624)
        logger.debug(f"Response from Amadeus city: {response.data}")
        for r in response.data:
            print(r)
        print("Baires")
        response = self.amadeus.get('/v1/reference-data/locations/cities', keyword='Buenos Aires')
        logger.debug(f"Response from Amadeus city: {response.data}")

        self.assertTrue(len(response.data) > 0)
        databaires = response.data[0]
        self.assertEqual(databaires["name"], "Buenos Aires")
        self.assertEqual(databaires["iataCode"], "BUE")

        response = self.amadeus.get('/v1/reference-data/locations/airports', latitude=databaires["geoCode"]["latitude"], longitude=databaires["geoCode"]["latitude"])
        logger.debug(f"Response from Amadeus Baires city: {response.data}")


if __name__ == '__main__':
    unittest.main()
