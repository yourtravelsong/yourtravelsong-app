import streamlit as st
import requests
import os
import json
import pandas as pd
import subprocess

API_KEY = os.getenv("UNSPLASH_API_KEY")

def get_res(json_path: str):
    f = open(json_path)
    res = json.load(f)
    f.close()
    return res

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
                st.image(f"../airline-logos/logos/{offer["airline_code"][0]}", None, 500)
                st.write(f"You have an available flight with {offer["airline_code"][0]} - {offer["airline_name"]}, with its departure at {offer["departure"]}, with a price of {offer["price"]} {offer["currency"]}.")

def print_city_img(city: str, show: bool) -> None:
    if (show):
        search_url = f"https://api.unsplash.com/search/photos?query={city}&client_id={API_KEY}"
        
        response = requests.get(search_url)
        results = response.json().get("results")
        
        if results:
            image_url = results[0]["urls"]["regular"]
            image_response = requests.get(image_url)
            
            st.image(image_response.content)

def write_results(cities: list[str], expl: str) -> None:
    if (len(cities) > 0):
        st.divider()
        st.write("Top result:")
        st.write(f"## {cities[0]}")
        st.write("")
        if (expl):
            st.caption(expl)
        print_city_img(cities[0], show=True) # false to not waste credits for the unsplash api
        st.write("#### Other recommendations:")
        for city in cities[1:]:
            st.write(f"· {city}")


def start_exec(song, author, results):
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
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        st.warning(f"Something went wrong: {e}")
        st.stop()
    
    return response.json()

def get_input() -> str:
    #get input from user (song - author)
    song = st.text_input("What is the name of a song that you're listening to right now?")
    if not song:
        st.stop()
    author = st.text_input("What is the author?")
    if not author:
        st.stop()
    st.success('Name and author correctly submitted. Thanks!')
    return song, author

def main() -> None:
    st.title("YourTravelSong")
    st.divider()

    # get input from streamlit and start request to entry point
    song, author = get_input()

    # get the results
    results = entry_point_request(song, author)

    # display output
    cities, explanation = start_exec(song, author, results)
    write_results(cities, explanation)
    travel_plan(results)

if __name__ == "__main__":
    main()
