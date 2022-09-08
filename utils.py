import streamlit as st
import pickle

@st.cache(show_spinner=False)
def unpickle(file):
    with open(f"./data/{file}", "rb") as f:
        data = pickle.load(f)
    return data

@st.cache(show_spinner=False)
def sortNames(playerList):
    names = [
        f"{player['fullName']} ({player['currentTeam']['name']})" if "currentTeam" in player.keys()
        else f"{player['fullName']}"
        for player in playerList
    ]
    names = sorted(names, key = lambda x: x.split("(")[0].split()[-1])
    return names