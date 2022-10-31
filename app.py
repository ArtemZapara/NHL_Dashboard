import streamlit as st
from utils import *

st.set_page_config(layout="wide")
st.title(":ice_hockey_stick_and_puck: NHL Dashboard")

logos = unpickle("teamLogos.pkl")
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

with st.sidebar:

    sidebarButton = st.radio("Side", ("Players", "Teams"), horizontal=False, label_visibility="collapsed")

if sidebarButton == "Teams":

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

        logoURL1 = logos[teamID1]
        teamLogo1 = displayTeamLogo(logoURL1)
        st.plotly_chart(teamLogo1, use_container_width=True, config={"staticPlot":True})

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
            key = "t1=2",
            format_func=lambda x: f"{teams2[x]['name']}"
        )

        teamID2 = teams2[team2]["id"]

        logoURL2 = logos[teamID2]
        teamLogo2 = displayTeamLogo(logoURL2)
        st.plotly_chart(teamLogo2, use_container_width=True, config={"staticPlot":True})

    with col2:

        radioB = st.radio("Type of display", ("Overall stats", "Shot chart"), horizontal=True, label_visibility="collapsed")

        if radioB == "Overall stats":

            team1stats = loadTeamStats(teamID1, selectedSeason1)
            team2stats = loadTeamStats(teamID2, selectedSeason2)

            figureStats = displayStats(team1stats, team2stats, statsType="T")
            st.plotly_chart(figureStats, use_container_width=True, config={"staticPlot":True})

        if radioB == "Shot chart":

            st.write("To be added")


if sidebarButton == "Players":

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

        logoURL1 = logos[teamID1]
        teamLogo1 = displayTeamLogo(logoURL1)
        playerCard1 = displayPlayerInfo(age1, height1, weight1)

        st.plotly_chart(teamLogo1, use_container_width=True, config={"staticPlot":True})
        st.image(imageURL1, use_column_width=True)
        st.plotly_chart(playerCard1, use_container_width=True, config={"staticPlot":True})

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

        logoURL2 = logos[teamID2]
        teamLogo2 = displayTeamLogo(logoURL2)
        playerCard2 = displayPlayerInfo(age2, height2, weight2)

        st.plotly_chart(teamLogo2, use_container_width=True, config={"staticPlot":True})
        st.image(imageURL2, use_column_width=True)
        st.plotly_chart(playerCard2, use_container_width=True, config={"staticPlot":True})

    with col2:
        radioB = st.radio("Type of display", ("Overall stats", "Shot chart"), horizontal=True, label_visibility="collapsed")

        if radioB == "Overall stats":
            stats1 = loadStats(playerID1, selectedSeason1)
            stats2 = loadStats(playerID2, selectedSeason2)

            if position1 != "G" and position2 != "G":
                figureStats = displayStats(stats1, stats2, statsType="F")
                st.plotly_chart(figureStats, use_container_width=True, config={"staticPlot":True})

            elif position1 == "G" and position2 == "G":
                figureStats = displayStats(stats1, stats2, statsType="G")
                st.plotly_chart(figureStats, use_container_width=True, config={"staticPlot":True})

            else:
                st.error("You cannot compare a field player with a goaltender!")

        if radioB == "Shot chart":

            if position1 != "G" and position2 != "G":
                if selectedSeason1 == selectedSeason2:
                    allScores1 = allScores2 = unpickle(f"{selectedSeason1}/allScores.pkl")
                    allShots1 = allShots2 = unpickle(f"{selectedSeason1}/allShots.pkl")

                else:
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

                figureScores = displayScores(scores1, scores2, shots1, shots2)
                st.plotly_chart(figureScores, use_container_width=True, config={"staticPlot":True})

            elif position1 == "G" and position2 == "G":
                st.write("To be added.")

            else:
                st.error("You cannot compare a field player with a goaltender!")