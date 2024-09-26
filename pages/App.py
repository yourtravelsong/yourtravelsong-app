import json

import streamlit as st
import requests
import os

UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")

def travel_plan(results):
    st.divider()
    st.markdown("Would you like to know your :gray-background[personalized travel plans?] :airplane_departure: ")
    if (st.button("Show me!")):
        i = 0
        for offer in results["result"]["recommendations"][0]["offers"]:
            omit = False
            for key in offer:
                if offer[key] == None:
                    omit = True
            if (not omit):
                i += 1        
                st.header(f"Travel plan idea #{i}")
                if os.path.exists(f"../airline-logos/logos/{offer['airline_code'][0]}.png"):
                    st.image(f"../airline-logos/logos/{offer['airline_code'][0]}.png", None, 500)
                st.write(f"You have an available flight with {offer['airline_code'][0]} - {offer['airline_name']}, with its departure at {offer['departure']}, with a price of {offer['price']} {offer['currency']}.")

def print_city_img(city: str) -> None:
    search_url = f"https://api.unsplash.com/search/photos?query={city}&client_id={UNSPLASH_API_KEY}"
    response = requests.get(search_url)
    st.write(response)
    try:
        results = response.json().get("results")
        st.write(results)
        image_url = results["urls"]["regular"]
        image_response = requests.get(image_url)

        st.image(image_response.content)
    except Exception as e:
       print("Error {}".format(e))

def write_results(results) -> None:
    st.write(f"# You are listening {results['result']['song']} by {results['result']['artist']}")
    st.write(f"## Feeling from the song: {' - '.join(results['result']['sentiments'])}")

    if (len(results['result']['recommendations']) > 0):


        for aRecomentation  in results['result']['recommendations']:

            aCity = aRecomentation["city"]

            st.write(f"## Suggestion: Visit {aCity}")
            st.write("")
            st.write(f"### Why this suggestion? {aRecomentation['reason']}")
            st.write("")

            st.write(f"## Travel options to {aCity}:")
            st.divider()
            for i, offer in enumerate(aRecomentation["offers"]):

                    #st.header(f"Travel plan idea #{i}")

                    col1, col2, col3 = st.columns([2, 6, 1])  # The numbers represent the width ratio of the columns

                    # Place the image in the first column


                    # Place the link in the second column


                    logoPath = f"/Users/matias/develop/code/yourtravelsong-app/airline-logos/logos/{offer['airline_icao_code']}.png"

                    with col1:
                       #st.image("your_image.png", width=100)  # Replace with the path to your image
                        if os.path.exists(logoPath):
                            #st.image(logoPath, None, 500)

                            st.image(logoPath)

                        else:
                            st.write(f"Airline logo not found for {logoPath}")
                    with col2:
                        st.write(
                            f"### {offer['departure']} - {offer['price']} {offer['currency']}")

                    with col3:
                        #st.markdown("[BUY](https://www.edreams.com/travel/#results/type=R;from=BCN;to=PAR;dep=2024-09-27;ret=2024-10-22;buyPath=FLIGHTS_HOME_SEARCH_FORM;internalSearch=true)")
                        st.markdown(
                                 '<a href="https://www.edreams.com/travel/#results/type=R;from=BCN;to=PAR;dep=2024-09-27;ret=2024-10-22;buyPath=FLIGHTS_HOME_SEARCH_FORM;internalSearch=true" style="font-size:20px;">BUY</a>',
                                 unsafe_allow_html=True
                             )


def parseResults(song, author, results):
    # get cities from each result
    recommended_cities = []
    for res in results["result"]["recommendations"]:
        recommended_cities.append(res["city"])

    result_explanation: str = results["result"]["recommendations"][0]["reason"]
    return recommended_cities, result_explanation

def entry_point_request(song, author):
    url = "http://127.0.0.1:5000/getsuggestion"
    data = {
        "artist": author,
        "title": song
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        st.warning(f"Something went wrong: {e}")
        st.stop()
    return response.json()

def get_input() -> str:
    #get input from user (song - author)
    song = st.text_input("What is the name of a song that you're listening to right now?")
    #if not song:
    #    st.stop()
    author = st.text_input("What is the author?")

    #if not author and not song:
    #    st.stop()
    #st.success('Name and author correctly submitted. Thanks!')
    return song, author


def main():
    with st.form("mainForm"):
        # Add two text fields
        song = st.text_input("What is the name of a song that you're listening to right now?")
        author = st.text_input("What is the author?")

        # if not song:
        #    st.stop()

        # Add a submit button
        clicked = st.form_submit_button("Submit")

        # Once the form is submitted
        if clicked:
            results = entry_point_request(song, author)

            #print(json.dumps(results, indent=4))
            write_results(results)


if __name__ == "__main__":
    main()
