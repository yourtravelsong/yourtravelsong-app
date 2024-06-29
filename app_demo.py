import streamlit as st
import requests
import os

def print_city_img(city: str):
    api_key = os.getenv("UNSPLASH_API_KEY") 
    search_url = f"https://api.unsplash.com/search/photos?query={city}&client_id={api_key}"
    
    response = requests.get(search_url)
    results = response.json().get("results")
    
    if results:
        image_url = results[0]["urls"]["regular"]
        image_response = requests.get(image_url)
        
        st.image(image_response.content)

def write_results(cities: list[str], expl: str) -> None:
    st.divider()
    st.write("Top result:")
    st.write(f"## {cities[0]}")
    st.write("")
    st.caption(expl)
    st.write("Other recommendations:")
    for city in cities[1:]:
        st.write(f"{city}")

def start_exec(song: str, author: str):
    recommended_cities = ["Denver", "Cincinatti", "Detroit"]
    result_explanation: str = "This would be a great location for your travel! It includes some museums in pop art and other activities you might fancy."
    req_completed = False
    #request output from our program and set req_completed to true (NOW HARDCODED)
    req_completed = True
    if not req_completed:
        st.write("loading...")
        st.stop()
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
    recommended_cities, result_explanation = start_exec(song, author)
    write_results(recommended_cities, result_explanation)
    print_city_img(recommended_cities[0])
    


if __name__ == "__main__":
    main()
