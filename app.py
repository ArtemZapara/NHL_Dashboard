import streamlit as st
from utils import *

st.set_page_config(layout="wide")
st.title(":ice_hockey_stick_and_puck: NHL Dashboard")

playerList = unpickle("playerList.pkl")
seasons = ["20212022","20202021","20192020"]

st.markdown(
    """
    <style>
    [data-baseweb="select"] {
        margin-top: -40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1,4,1])

with col1:
    season1 = st.selectbox(
            "Select a season",
            range(len(seasons)),
            key="s1",
            format_func=lambda x: f"{seasons[x][:4]}-{seasons[x][4:]}"
        )

    selectedSeason1 = seasons[season1]

    teams1 = loadTeams(selectedSeason1)
    team1 = st.selectbox(
        "Select team",
        range(len(teams1)),
        key = "t1",
        format_func=lambda x: f"{teams1[x]['name']}"
    )

    teamID1 = teams1[team1]["id"]
    roster1 = loadRoster(teamID1, selectedSeason1)

    player1 = st.selectbox(
        "Select player",
        range(len(roster1)),
        key="r1",
        format_func=lambda x: f"({roster1[x]['position']['code']}) {roster1[x]['person']['fullName']}"
    )

    playerID1 = roster1[player1]["person"]["id"]
    playerInfo1 = loadPlayerInfo(playerID1)

    age1, height1, weight1, position1 = parseInfo(playerInfo1)
    imageURL1 = checkImageURL(playerID1)
    st.image(imageURL1)
    st.write(f"Age: {age1}")
    st.write(f"Height: {height1}")
    st.write(f"Weight: {weight1}")

with col3:
    season2 = st.selectbox(
            "Select a season",
            range(len(seasons)),
            key="s2",
            format_func=lambda x: f"{seasons[x][:4]}-{seasons[x][4:]}"
        )

    selectedSeason2 = seasons[season2]

    teams2 = loadTeams(selectedSeason2)
    team2 = st.selectbox(
        "Select team",
        range(len(teams2)),
        key = "t2",
        format_func=lambda x: f"{teams2[x]['name']}"
    )

    teamID2 = teams2[team2]["id"]
    roster2 = loadRoster(teamID2, selectedSeason2)

    player2 = st.selectbox(
        "Select player",
        range(len(roster2)),
        key="r2",
        format_func=lambda x: f"({roster2[x]['position']['code']}) {roster2[x]['person']['fullName']}"
    )

    playerID2 = roster2[player2]["person"]["id"]
    playerInfo2 = loadPlayerInfo(playerID2)

    age2, height2, weight2, position2 = parseInfo(playerInfo2)
    imageURL2 = checkImageURL(playerID2)
    st.image(imageURL2)
    st.write(f"Age: {age2}")
    st.write(f"Height: {height2}")
    st.write(f"Weight: {weight2}")

with col2:

    stats1 = loadStats(playerID1, selectedSeason1)
    stats2 = loadStats(playerID2, selectedSeason2)

    if position1 != "G" and position2 != "G":
        figureStats = displayStats(stats1, stats2, playerType="F")
        st.plotly_chart(figureStats, use_container_width=True, config={"staticPlot":True})

<<<<<<< HEAD
        allScores1 = unpickle(f"{selectedSeason1}/allScores.pkl")
        allShots1 = unpickle(f"{selectedSeason1}/allShots.pkl")
        allScores2 = unpickle(f"{selectedSeason2}/allScores.pkl")
        allShots2 = unpickle(f"{selectedSeason2}/allShots.pkl")

        scores1, shots1 = list(), list()
        scores2, shots2 = list(), list()
        if playerID1 in allScores1:
            scores1 = allScores1[playerID1]
        if playerID1 in allShots1:
            shots1 = allShots1[playerID1]
        if playerID2 in allScores2:
            scores2 = allScores2[playerID2]
        if playerID2 in allShots2:
            shots2 = allShots2[playerID2]
=======
        allScores = unpickle(f"{selectedSeason1}/allScores.pkl")
        allShots = unpickle(f"{selectedSeason2}/allShots.pkl")

        scores1, scores2 = list(), list()
        shots1, shots2 = list(), list()
        if playerID1 in allScores:
            scores1 = allScores[playerID1]
        if playerID2 in allScores:
            scores2 = allScores[playerID2]
        if playerID1 in allShots:
            shots1 = allShots[playerID1]
        if playerID2 in allShots:
            shots2 = allShots[playerID2]
>>>>>>> 92335d9186961bd0f16f408ba626c8feb07427af

        figureScores = displayScores(scores1, scores2, shots1, shots2)
        st.plotly_chart(figureScores, use_container_width=True, config={"staticPlot":True})

    elif position1 == "G" and position2 == "G":
        figureStats = displayStats(stats1, stats2, playerType="G")
        st.plotly_chart(figureStats, use_container_width=True, config={"staticPlot":True})

    else:
        st.error("You cannot compare a field player with a goaltender!")