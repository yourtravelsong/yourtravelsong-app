import os
import json
from amadeus import Client, ResponseError
from datetime import datetime, timedelta
from embeddings.query_dispatcher import QueryDispatcher

cacheAirlineData = {}

class TravelBackend:

    def __init__(self):
        print("Init TravelBackend")
        self.query_dispatcher = QueryDispatcher()
        self.amadeus = Client(
            client_id=os.getenv("AMADEUS_API_KEY"),
            client_secret=os.getenv("AMADEUS_SECRET_KEY")
        )


    def retrieveSuggestion(self, artist, song):
        response = self.query_dispatcher.get_response(song=song, artist=artist)
        print("Response from query_dispatcher: ", response)
        responseJson = json.loads(response)
        return responseJson



    def computeIATACode(self,model, obtainedCity):
        obtain_sentiments_list = model.complete(
            "which is the IATA code of {} airport? return just the code, no explanation, just the code".format(obtainedCity))

        print("IATA obtained from a LLM: ", obtain_sentiments_list.text)
        candidateIATA =  obtain_sentiments_list.text.strip()

        message =  "IATA code must have 3 characters: "+candidateIATA+" but have "+str(len(candidateIATA))
        assert len(candidateIATA) == 3, message
        return candidateIATA

    def getAirlineData(self,airlineCodes):

        if len(airlineCodes) == 0:
            return "Unknown-Airline-Code", "Unknown-Airline-Code"
        airlineCode = airlineCodes[0]

        print("Asking for airline data for code: {}".format(airlineCode))
        ## Return cached data if available
        if airlineCode in cacheAirlineData:
            print("Returning cached data for airline code: ", airlineCode)
            response =  cacheAirlineData[airlineCode]
            return response.data[0]["businessName"], response.data[0]["icaoCode"]
        else:
            ### Ask Amadeus for the airline data
            try:
                response = self.amadeus.get('/v1/reference-data/airlines', airlineCodes=airlineCode)
                print("Searching Airlines from code {}: response {}".format(airlineCode, response))
                if response is not None and len(response.data) > 0:
                    cacheAirlineData[airlineCode] = response
                    return response.data[0]["businessName"], response.data[0]["icaoCode"]
                else:
                    return "Unknown-Airline-Code"
            except ResponseError as error:
                print(error)
                return None
    def get_suggestion(self, artist, song):

        suggestion = self.retrieveSuggestion(artist, song)

        obtainedCities = suggestion["cities"]

        if len(obtainedCities) == 0:
            print("NO cities found")
            return {"artist": artist, "song": song, "city_sugg": "X", "sentiments": [], "recommendations": []}

        allOffers = []
        for aCity in obtainedCities:
            IATAcode = self.computeIATACode(self.query_dispatcher.llm, aCity)
            print(f"IATA code for city: {aCity}: {IATAcode}")
            currentLocation = self.getCurrentLocation()

            current_date = datetime.now()
            candidate_dep_date = current_date + timedelta(days=10)
            formatted_candidate_dep_date = candidate_dep_date.strftime('%Y-%m-%d')
            dataflights = self.getFlights(IATAcode, currentLocation, departureDate=formatted_candidate_dep_date, adults=1)

            dataCity = {"city": aCity, "offers": dataflights, "reason": suggestion["reasons_why"][aCity] }
            allOffers.append(dataCity)


        sentimentsFromLyric = suggestion['sentiment']
        print(f"All offers for cities: {len(allOffers)}")
        return {"artist": artist, "song": song,  "sentiments": sentimentsFromLyric, "recommendations": allOffers}

    def getCurrentLocation(self):
        ### TODO: obtain client location
        return "BCN"

    def getFlights(self, codeDestination, codeOrigin, departureDate='2024-11-01', adults=1, topFlights=3):

        try:
            print("Searching flights from {} to {} on {}".format(codeOrigin, codeDestination, departureDate))
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=codeOrigin,
                destinationLocationCode=codeDestination,
                departureDate=departureDate,
                adults=adults)
            if len(response.data) > 0:
                resultAllFlights = []

                print(f"Flight found: ({len(response.data)})" )

                for i in range(min(topFlights, len(response.data)) ):
                    print(f"\n----Flight {i}:")
                    firstFlight = response.data[i]
                    price = firstFlight['price']['total']
                    currency = firstFlight['price']['currency']
                    airlinecode = firstFlight['validatingAirlineCodes']
                    print("Retrieving airlineData from flight: {}".format(firstFlight))
                    airlinename, icaoCode = self.getAirlineData(airlinecode)
                    print("Price: ", price, currency, " Airline_code: ", airlinecode, " Airline_name: ", airlinename,
                          "Airline_icao_code", icaoCode)
                    aFlight = {"type": "flight", "airline_name": airlinename, "price": price,
                               "currency": currency,
                               "departure": departureDate,
                               "airline_code": airlinecode,
                               "airline_icao_code": icaoCode,
                               "status": "success", "i": i}
                    resultAllFlights.append(aFlight)
                return resultAllFlights
        except ResponseError as error:
            print("----Error Asking for flights  to Amadeus")
            print(error)
            resultAllFlights = []
            return resultAllFlights