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
    YourTravelSong is a product  built specifically to
    interpret songs into desired travel destinations and real-time found travel plans.
    \n**👈 Select the App page from the sidebar** to see some examples
    of what Streamlit can do!
    \n### Want to learn more?
    """)
st.markdown("- Perfect for **music-integrated apps** to display heavily **personalized travel ads**.")
st.markdown("- Versatile and easy to integrate, it _only_ needs a song and an author to work.")
st.markdown("- Gives up many destinations ordered in relevance and fully built travel plans.") 

st.image("st_images/img1.png")

st.divider()
    
# Explain project
st.write("## How did we do it?")
    #add images to display in here
st.image(["st_images/scheme.png"])
# st_player("https://soundcloud.com/toto-official/africa-1?in=alana97/sets/80s")

# print links randomly ordered

st.divider()
st.markdown("Developed by:\n")

links = ["Matias Martínez - www.linkedin.com/in/matiassebastianmartinez", "Manel Palacín - www.linkedin.com/in/manel-palacin-diaz", "Eyuel Muse - www.linkedin.com/in/eyuel-muse-woldesembet"]
random.shuffle(links)
for link in links:
    st.markdown(f"- {link}")

    

