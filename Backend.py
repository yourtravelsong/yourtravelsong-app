#from llama_index.llms.ollama import Ollama
import os
import json
from amadeus import Client, ResponseError
from datetime import datetime, timedelta


from embeddings.query_dispatcher import QueryDispatcher


class TravelBackend:

    def __init__(self):
        print("Init TravelBackend")
        self.query_dispatcher = QueryDispatcher()


    def retrieveLyric(self, artist, song):
        ## todo
        print("WARNING, HARDCODED LYRIC")
        return "I'm a creep, I'm a weirdo. What the hell am I doing here? I don't belong here."


    def retrieveSuggestion(self, artist, song):
        response = self.query_dispatcher.get_response(song=song, artist=artist)
        print("Response from query_dispatcher: ", response)
        responseJson = json.loads(response)
        print("Formated response: ", json.dumps(responseJson, indent=4))
        return responseJson

    amadeus = Client(
        client_id=os.environ['AMADEUS_API_KEY'],
        client_secret=os.environ['AMADEUS_SECRET_KEY']
    )

    def computeIATACode(self,model, obtainedCity):
        obtain_sentiments_list = model.complete("which is the IATA code of {} airport? return just the code, no explanation".format(obtainedCity))
        print("IATACode: ", obtain_sentiments_list.text)
        return obtain_sentiments_list.text.strip()

    def getAirlineCode(self,airlineCode):
        try:
            response = self.amadeus.get('/v1/reference-data/airlines', airlineCodes=airlineCode)
            print("Airlines response {}".format( response))
            if len(response.data) > 0:
                return response.data[0]["businessName"]
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
            return {"artist": artist, "song": song, "city_sugg": "X", "sentiments": [], "offers": []}

        allOffers = []
        for aCity in obtainedCities:
            IATAcode = self.computeIATACode(self.query_dispatcher.llm, aCity)
            print("IATA code: ", IATAcode, " for city: ", aCity)
            currentLocation = self.getCurrentLocation()

            current_date = datetime.now()
            candidate_dep_date = current_date + timedelta(days=10)
            formatted_candidate_dep_date = candidate_dep_date.strftime('%Y-%m-%d')
            dataflights = self.getFlights(IATAcode, currentLocation, departureDate=formatted_candidate_dep_date, adults=1)

            dataCity = {"city": aCity, "offers": dataflights, "reason": suggestion["reasons_why"][aCity] }

            allOffers.append(dataCity)


        sentimentsFromLyric = suggestion['sentiment']
        return {"artist": artist, "song": song,  "sentiments": sentimentsFromLyric, "offers": allOffers}

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

                print("Flight found")

                for i in range(min(topFlights, len(response.data)) ):
                    firstFlight = response.data[i]
                    price = firstFlight['price']['total']
                    currency = firstFlight['price']['currency']
                    airlinecode = firstFlight['validatingAirlineCodes']
                    airlinename = self.getAirlineCode(airlinecode)
                    print("Price: ", price, currency, " Airline_code: ", airlinecode, " Airline_name: ",airlinename)
                    aFlight = { "type": "flight", "airline_name":airlinename, "price": price,   "currency": currency, "departure": departureDate,"airline_code": airlinecode,"status": "success","i":i}
                    resultAllFlights.append(aFlight)
                return resultAllFlights
        except ResponseError as error:
            print("Error Asking for flights  to Amadeus")
            resultAllFlights = []
            print("Generating fake data for flights")
            aFlight = {"type": "flight", "airline_name": "TAP", "price": 87, "currency": "EUR",
                       "departure": "2024-11-11", "airline_code": "TP", "status": "success", "i":0}

            resultAllFlights.append(aFlight)
            return resultAllFlights