import streamlit as st
import requests
from utils import *

st.set_page_config(layout="wide")
st.title(":ice_hockey_stick_and_puck: NHL Dashboard")

playerList = unpickle("playerList.pkl")
teamList = unpickle("teamList.pkl")
allScores = unpickle("allScores2021.pkl")

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

    playerID1, age1, height1, weight1 = fetchPlayerInfo(playerList, select1)
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

    playerID2, age2, height2, weight2 = fetchPlayerInfo(playerList, select2)
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
        figureStats = displayStats(stats1, stats2)
        st.plotly_chart(figureStats, use_container_width=True, config={"staticPlot":True})

        scores1 = [i[playerID1] for i in allScores if playerID1 in i.keys()]
        scores2 = [i[playerID2] for i in allScores if playerID2 in i.keys()]

        st.write(len(scores1), len(scores2))

        figureScores = displayScores(scores1, scores2)
        st.plotly_chart(figureScores, use_container_width=True, config={"staticPlot":True})