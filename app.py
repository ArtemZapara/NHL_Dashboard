import streamlit as st
import requests
from utils import *

st.set_page_config(layout="wide")
st.title(":ice_hockey_stick_and_puck: NHL Dashboard")

playerList = unpickle("playerList.pkl")
seasons = ["20212022"]

col1, col2, col3 = st.columns([1,2.5,1])
with col1:
    select1 = st.selectbox(
        "Select a player in the list below",
        range(len(playerList)),
        key = "select1",
        format_func=lambda x:
            f"({playerList[x]['primaryPosition']['code']}) {playerList[x]['fullName']} ({playerList[x]['currentTeam']['name']})"
            if "currentTeam" in playerList[x].keys()
            else  f"({playerList[x]['primaryPosition']['code']}) {playerList[x]['fullName']}"
    )

    playerID1 = playerList[select1]["id"]
    age1 = playerList[select1]["currentAge"]
    height1 = playerList[select1]["height"]
    weight1 = playerList[select1]["weight"]
    # st.write(playerList[select1])

    imageURL1 = checkImageURL(playerID1)
    st.image(imageURL1)
    st.write(f"Age: {age1}")
    st.write(f"Height: {height1}")
    st.write(f"Weight: {weight1}")

with col3:
    select2 = st.selectbox(
        "Select a player in the list below",
        range(len(playerList)),
        key = "select2",
        format_func=lambda x:
            f"({playerList[x]['primaryPosition']['code']}) {playerList[x]['fullName']} ({playerList[x]['currentTeam']['name']})"
            if "currentTeam" in playerList[x].keys()
            else  f"({playerList[x]['primaryPosition']['code']}) {playerList[x]['fullName']}"
    )

    playerID2 = playerList[select2]["id"]
    age2 = playerList[select2]["currentAge"]
    height2 = playerList[select2]["height"]
    weight2 = playerList[select2]["weight"]

    imageURL2 = checkImageURL(playerID2)
    st.image(imageURL2)
    st.write(f"Age: {age2}")
    st.write(f"Height: {height2}")
    st.write(f"Weight: {weight2}")

with col2:
    seasonID = st.selectbox(
        "Select a season",
        range(len(seasons)),
        format_func=lambda x: f"{seasons[x][:4]}-{seasons[x][4:]}"
    )

    selectedSeason = seasons[seasonID]
    stats1 = loadStats(playerID1, selectedSeason)
    stats2 = loadStats(playerID2, selectedSeason)
    if st.button(label="Get stats"):
        displayStats(stats1, stats2)