import streamlit as st
import pickle
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@st.cache(show_spinner=False)
def unpickle(file):
    with open(f"./data/{file}", "rb") as f:
        data = pickle.load(f)
    return data

@st.cache(show_spinner=False)
def checkImageURL(ID):
    imageURL = f"https://cms.nhl.bamgrid.com/images/headshots/current/168x168/{ID}.jpg"
    response = requests.get(imageURL)
    if response.status_code != 200:
        imageURL = "https://cms.nhl.bamgrid.com/images/headshots/current/168x168/skater.jpg"
    return imageURL

@st.cache(show_spinner=False)
def loadStats(ID, season):
    statsURL = f"https://statsapi.web.nhl.com/api/v1/people/{ID}/stats?stats=statsSingleSeason&season={season}"
    response = requests.get(url=statsURL)
    statsData = response.json()
    stats = statsData["stats"][0]["splits"][0]["stat"]
    return stats

def displayStats(stats1, stats2):
    def computeColorList(dict1, dict2, keys):
        colorList = list()
        for key in keys:
            if dict1[key] > dict2[key]:
                colorList.append("forestgreen")
                colorList.append("crimson")
            elif dict1[key] < dict2[key]:
                colorList.append("crimson")
                colorList.append("forestgreen")
            else:
                colorList.append("darkgrey")
                colorList.append("darkgrey")
        return colorList

    keys = [
        "games",
        "goals",
        "assists",
        "points",
        "pim",
        "powerPlayGoals",
        "powerPlayPoints",
        "shortHandedGoals",
        "shortHandedPoints",
        "gameWinningGoals",
        "overTimeGoals",
        "shots",
        "shotPct"
    ]

    abbr = {
        "games": "GP",
        "goals": "G",
        "assists": "A",
        "points": "P",
        "plusMinus": "+/-",
        "pim": "PIM",
        "powerPlayGoals": "PPG",
        "powerPlayPoints": "PPP",
        "shortHandedGoals": "SHG",
        "shortHandedPoints": "SHP",
        "gameWinningGoals": "GWG",
        "overTimeGoals": "OTG",
        "shots": "S",
        "shotPct": "S%"
    }

    colorList = computeColorList(stats1, stats2, keys)
    limits = {k: 1.1*(stats1[k] + stats2[k])+1 for k in set(stats1) if k in keys}

    layouts = {}
    layouts["xaxis"] = {}
    fig = go.Figure()
    fig = make_subplots(rows=len(keys), cols=2)
    for i in range(2*len(keys)):
        row = (i+2)//2
        key = keys[row-1]

        if i % 2 == 0:
            fig.append_trace(
                go.Bar(
                    y=[key],
                    x=[stats1[key]],
                    orientation="h",
                    text=stats1[key],
                    textposition="outside",
                    marker={"color": colorList[i]}),
                    row=row,
                    col=1
                )
            if i == 0:
                layouts["xaxis"]["range"] = [limits[key],0]
                layouts['yaxis'] = {"showticklabels" : False}
            else:
                layouts['xaxis'+str(i+1)] = {}
                layouts["xaxis"+str(i+1)]["range"] = [limits[key],0]
                layouts['yaxis'+str(i+1)] = {"showticklabels" : False}
        else:
            fig.append_trace(
                go.Bar(
                    y=[f"{abbr[key]:{' '}<{8}}"],
                    x=[stats2[key]],
                    orientation="h",
                    text=stats2[key],
                    textposition="outside",
                    marker={"color": colorList[i]}),
                    row=row,
                    col=2)
            layouts['xaxis'+str(i+1)] = {}
            layouts["xaxis"+str(i+1)]["range"] = [0, limits[key]]

    fig.update_layout(**layouts, showlegend=False, height=500)
    fig.update_xaxes(showticklabels=False, showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config={"staticPlot":True})