import streamlit as st
import requests
from utils import unpickle


st.set_page_config(layout="wide")
playerList = unpickle("playerList.pkl")

col1, col2, col3 = st.columns([1,2,1])

with col1:
    index = st.selectbox(
        "Select a player in the list below",
        range(len(playerList)),
        format_func=lambda x:
            f"({playerList[x]['primaryPosition']['code']}) {playerList[x]['fullName']} ({playerList[x]['currentTeam']['name']})"
            if "currentTeam" in playerList[x].keys()
            else  f"({playerList[x]['primaryPosition']['code']}) {playerList[x]['fullName']}"
    )

    playerID = playerList[index]["id"]

    imageURL = f"https://cms.nhl.bamgrid.com/images/headshots/current/168x168/{playerID}.jpg"
    response = requests.get(imageURL)
    if response.status_code == 200:
        st.image(imageURL)
    else:
        st.image("https://cms.nhl.bamgrid.com/images/headshots/current/168x168/skater.jpg")