# run with: streamlit run Introduction.py
import streamlit as st
from streamlit_player import st_player
import random


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


st.write("# Welcome to YourTravelSong! 👋")

st.sidebar.success("Try our app by selecting the ""App"" page above!.")

st.markdown(
    """
    YourTravelSong is a product with an API-like framework built specifically for
    interpreting songs into desired travel destinations and real-time travel plans.
    \n**👈 Select the App page from the sidebar** to see some examples
    of what Streamlit can do!
    \n### Want to learn more?
    """)
st.markdown("- Perfect for **music-integrated apps** to display heavily **personalized travel ads**.")
st.markdown("- Versatile and easy to integrate, it _only_ needs a song and an author to work.")
st.markdown("- Gives up many destinations ordered in relevance and fully built travel plans.") 

st.divider()
    
# Embed a youtube video
st_player("https://soundcloud.com/toto-official/africa-1?in=alana97/sets/80s")

# print links randomly ordered

st.divider()
st.markdown("Developed by:\n")

links = ["www.linkedin.com/in/matiassebastianmartinez", "www.linkedin.com/in/manel-palacin-diaz", "www.linkedin.com/in/eyuel-muse-woldesembet"]
random.shuffle(links)
for link in links:
    st.markdown(f"- {link}")

    
