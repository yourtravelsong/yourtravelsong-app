from llama_index.llms.ollama import Ollama
import os
import json
from amadeus import Client, ResponseError

class TravelBackend:

    def __init__(self):
        print("Init TravelBackend")


    def retrieveLyric(self, artist, song):
        ## todo
        print("WARNING, HARDCODED LYRIC")
        return "I'm a creep, I'm a weirdo. What the hell am I doing here? I don't belong here."

    def retrieveCity(self, artist, song):
        ## todo
        print("WARNING, HARDCODED CITY")
        return "New York"

    amadeus = Client(
        client_id=os.environ['AMADEUS_API_KEY'],
        client_secret=os.environ['AMADEUS_SECRET_KEY']
    )

    def computeIATACode(self,model, obtainedCity):
        obtain_sentiments_list = model.complete("which is the IATA code of {} airport? return just the code".format(obtainedCity))
        print("Sentiments retrieved: ", obtain_sentiments_list.text)

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

        retrievedLyric = self.retrieveLyric(artist, song)

        llama = Ollama(
            model="llama3",
           # request_timeout=40.0,
        )

        obtain_sentiments_list = llama.complete(f"return the sentiments you find in this lyric, just the sentiments, no more words, separated by commas:\n  {retrievedLyric}")
        print("Sentiments retrieved: ",obtain_sentiments_list.text)
        sentimentsFromLyric = obtain_sentiments_list.text.split(",")


        obtainedCity = self.retrieveCity(artist, song)

        IATAcode = self.computeIATACode(llama, obtainedCity)
        print("IATA code: ", IATAcode, " for city: ", obtainedCity)

        print("sentimentsFromLyric", sentimentsFromLyric)

        dataflights = self.getFlights(IATAcode, "MAD", departureDate='2024-11-01', adults=1)

        return {"artist": artist, "song": song, "city_sugg": "X", "sentiments": sentimentsFromLyric, "offers": dataflights}


    def getFlights(self, codeDestination, codeOrigin, departureDate='2024-11-01', adults=1, topFlights=3):

        try:
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
            print("Error retrieving flights {}".format(error))
            return  None