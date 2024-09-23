import logging
import os
import json
from amadeus import Client, ResponseError
from datetime import datetime, timedelta
from embeddings.query_dispatcher import QueryDispatcher
logger = logging.getLogger(__name__)
cacheAirlineData = {}

class TravelBackend:

    def __init__(self):
        logger.debug("Init TravelBackend")
        self.query_dispatcher = QueryDispatcher()
        self.amadeus = Client(
            client_id=os.getenv("AMADEUS_API_KEY"),
            client_secret=os.getenv("AMADEUS_SECRET_KEY")
        )

    def retrieveSuggestion(self, artist, song):
        response = self.query_dispatcher.get_response(song=song, artist=artist)
        logger.debug(f"Response from query_dispatcher: {response}" )
        responseJson = json.loads(response)
        return responseJson

    def computeIATACode(self,model, obtainedCity):
        obtain_sentiments_list = model.complete(
            "which is the IATA code of {} airport? return just the code, no explanation, just the code".format(obtainedCity))

        logger.debug("IATA obtained from a LLM: ", obtain_sentiments_list.text)
        candidateIATA =  obtain_sentiments_list.text.strip()

        message =  "IATA code must have 3 characters: "+candidateIATA+" but have "+str(len(candidateIATA))
        assert len(candidateIATA) == 3, message
        return candidateIATA
    
    def obtainAIATACodeFromAmadeusAPI(self, model, obtainedCity):

        response = self.amadeus.reference_data.locations.get(
            keyword=obtainedCity,
            subType='AIRPORT'
        )
        ### let's get the first airport
        if response is not None and len(response.data) > 0:
            return response.data[0]["iataCode"]
        else: 
            ## let's try with the city
            response = self.amadeus.reference_data.locations.get(
                keyword=obtainedCity,
                subType='CITY'
            )
            
            if response is not None and len(response.data) > 0:
                return response.data[0]["iataCode"]
        

    def getAirlineData(self,airlineCodes):

        if len(airlineCodes) == 0:
            return "Unknown-Airline-Code", "Unknown-Airline-Code"
        airlineCode = airlineCodes[0]

        logger.debug("Asking for airline data for code: {}".format(airlineCode))
        ## Return cached data if available
        if airlineCode in cacheAirlineData:
            logger.debug(f"Returning cached data for airline code: {airlineCode}" )
            response =  cacheAirlineData[airlineCode]
            return response.data[0]["businessName"], response.data[0]["icaoCode"]
        else:
            ### Ask Amadeus for the airline data
            try:
                response = self.amadeus.get('/v1/reference-data/airlines', airlineCodes=airlineCode)
                logger.debug("Searching Airlines from code {}: response {}".format(airlineCode, response))
                if response is not None and len(response.data) > 0:
                    cacheAirlineData[airlineCode] = response
                    return response.data[0]["businessName"], response.data[0]["icaoCode"]
                else:
                    return "Unknown-Airline-Code"
            except ResponseError as error:
                logger.error(error)
                return None

    def get_suggestionFromLyric(self, lyric):
            logger.info("Getting suggestion from lyric")
            pass

    def get_suggestion(self, artist, song):

        suggestion = self.retrieveSuggestion(artist, song)

        obtainedCities = suggestion["cities"]

        if len(obtainedCities) == 0:
            logger.error("NO cities found")
            return {"artist": artist, "song": song, "city_sugg": "X", "sentiments": [], "recommendations": []}

        allOffers = []
        for aCity in obtainedCities:
            IATAcode = self.obtainAIATACodeFromAmadeusAPI(self.query_dispatcher.llm, aCity)
            logger.debug(f"IATA code for city: {aCity}: {IATAcode}")
            currentLocation = self.getCurrentLocation()

            current_date = datetime.now()
            candidate_dep_date = current_date + timedelta(days=10)
            formatted_candidate_dep_date = candidate_dep_date.strftime('%Y-%m-%d')
            dataflights = self.getFlights(IATAcode, currentLocation, departureDate=formatted_candidate_dep_date, adults=1)

            dataCity = {"city": aCity, "offers": dataflights, "reason": suggestion["reasons_why"][aCity] }
            allOffers.append(dataCity)

        sentimentsFromLyric = suggestion['sentiment']
        logger.debug(f"All offers for cities: {len(allOffers)}")
        return {"artist": artist, "song": song,  "sentiments": sentimentsFromLyric, "recommendations": allOffers}

    def getCurrentLocation(self):
        ### TODO: obtain client location
        return "BCN"

    def getFlights(self, codeDestination, codeOrigin, departureDate='2024-11-01', adults=1, topFlights=3):

        try:
            logger.debug("Searching flights from {} to {} on {}".format(codeOrigin, codeDestination, departureDate))
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=codeOrigin,
                destinationLocationCode=codeDestination,
                departureDate=departureDate,
                adults=adults)
            if len(response.data) > 0:
                resultAllFlights = []

                logger.debug(f"Flight found: ({len(response.data)})" )

                for i in range(min(topFlights, len(response.data)) ):
                    logger.debug(f"\n----Flight {i}:")
                    firstFlight = response.data[i]
                    price = firstFlight['price']['total']
                    currency = firstFlight['price']['currency']
                    airlinecode = firstFlight['validatingAirlineCodes']
                    logger.debug("Retrieving airlineData from flight: {}".format(firstFlight))
                    airlinename, icaoCode = self.getAirlineData(airlinecode)
                    logger.debug(f"Price: {price} {currency},  Airline_code:  {airlinecode},  Airline_name: {airlinename} Airline_icao_code {icaoCode}")
                    aFlight = {"type": "flight", "airline_name": airlinename, "price": price,
                               "currency": currency,
                               "departure": departureDate,
                               "airline_code": airlinecode,
                               "airline_icao_code": icaoCode,
                               "status": "success", "i": i}
                    resultAllFlights.append(aFlight)
                return resultAllFlights
        except ResponseError as error:
            logger.error(f"----Error Asking for flights  to Amadeus {error}")
            resultAllFlights = []
            return resultAllFlights