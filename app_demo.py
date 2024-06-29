# run with: streamlit run app_demo.py
import streamlit as st
import requests
import os
import json
import pandas as pd

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
        for offer in results["result"]["offers"]:
            st.header(f"Travel plan idea: {offer["i"]}")
            for travel_property in offer:
                if travel_property not in ["i", "type", "status"]:
                    st.write(f"· {travel_property} : {offer[travel_property]}")

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
        print_city_img(cities[0], show=False) # false to not waste credits for the unsplash api
        st.write("#### Other recommendations:")
        for city in cities[1:]:
            st.write(f"· {city}")


def start_exec(song, author, results):
    # get cities from each result
    recommended_cities = []
    for res in results:
        recommended_cities.append(results["result"]["city_sugg"])

    result_explanation: str = "This would be a *great* location for your travel! It includes some museums in pop art and other activities you might fancy."
    return recommended_cities, result_explanation

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
    song, author = get_input()

    json_path = ""
    if not os.path.exists(json_path):
        st.warning("Something went wrong :(")
        st.stop()

    # get the results
    results = get_res(json_path)
    
    # display output
    cities, explanation = start_exec(song, author, results)
    write_results(cities, explanation)
    travel_plan(results)

if __name__ == "__main__":
    main()
