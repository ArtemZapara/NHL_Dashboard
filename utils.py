import streamlit as st
import pickle
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from datetime import date, datetime

@st.cache(show_spinner=False, allow_output_mutation=True)
def unpickle(file):
    """This helper function loads a file in the pickle format
    from the ./data/ folder.

    Args:
        file (str): name of the file to be loaded

    Returns:
        data: loaded data
    """
    with open(f"./data/{file}", "rb") as f:
        data = pickle.load(f)
    return data

@st.cache(show_spinner=False)
def fetchPlayerInfo(playerList, selected):
    playerID = playerList[selected]["id"]
    if "currentAge" in playerList[selected]:
        age = playerList[selected]["currentAge"]
    elif "birthDate" in playerList[selected]:
        birthDate = playerList[selected]["birthDate"]
        born = datetime.strptime(birthDate, "%Y-%m-%d")
        today = date.today()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    else:
        age = "No data"
    height = playerList[selected]["height"]
    weight = playerList[selected]["weight"]
    primaryPosition = playerList[selected]["primaryPosition"]["code"]
    return playerID, age, height, weight, primaryPosition

@st.cache(show_spinner=False)
def checkImageURL(ID):
    imageURL = f"https://cms.nhl.bamgrid.com/images/headshots/current/168x168/{ID}.jpg"
    response = requests.get(imageURL)
    if response.status_code != 200:
        imageURL = "https://cms.nhl.bamgrid.com/images/headshots/current/168x168/skater.jpg"
    return imageURL

@st.cache(show_spinner=False)
def loadStats(ID, season):
    """This function loads single season statistics for a player.

    Args:
        ID (int): player ID
        season (str): season in the format YYYYYYYY

    Returns:
        stats (dict): dictionary with statistics d
    """
    statsURL = f"https://statsapi.web.nhl.com/api/v1/people/{ID}/stats?stats=statsSingleSeason&season={season}"
    response = requests.get(url=statsURL)
    statsData = response.json()
    stats = statsData["stats"][0]["splits"][0]["stat"]
    return stats

@st.cache(show_spinner=False)
def loadTeams(season):
    seasonURL = f"https://statsapi.web.nhl.com/api/v1/standings?season={season}"
    r = requests.get(url=seasonURL)
    data = r.json()
    records = data["records"]
    teams = list()
    for record in records:
        for team in record["teamRecords"]:
            teams.append(team["team"])
    teams = sorted(teams, key = lambda x: x["name"])
    return teams

@st.cache(show_spinner=False)
def loadTeamStats(teamID, season):
    statsURL = f"https://statsapi.web.nhl.com/api/v1/teams/{teamID}?expand=team.stats&season={season}"
    r = requests.get(url=statsURL)
    data = r. json()
    splits = data["teams"][0]["teamStats"][0]["splits"]
    teamStats = splits[0]["stat"]
    return teamStats

@st.cache(show_spinner=False)
def loadRoster(teamID, season):
    rosterURL = f"https://statsapi.web.nhl.com/api/v1/teams/{teamID}?expand=team.roster&season={season}"
    r = requests.get(url=rosterURL)
    data = r.json()
    roster = data["teams"][0]["roster"]["roster"]
    roster = sorted(roster, key = lambda x: x["person"]["fullName"])
    return roster

@st.cache(show_spinner=False)
def get_index_by_teamID(teams, teamID):
    index = None
    teamIDs = [i["id"] for i in teams]
    if teamID in teamIDs:
        index = teamIDs.index(teamID)
    return index

@st.cache(show_spinner=False)
def get_index_by_playerID(roster, playerID):
    index = None
    playerIDs = [i["person"]["id"] for i in roster]
    if playerID in playerIDs:
        index = playerIDs.index(playerID)
    return index

@st.cache(show_spinner=False)
def loadPlayerInfo(playerID):
    playerURL = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    r = requests.get(url=playerURL)
    data = r.json()
    playerInfo = data["people"][0]
    return playerInfo

@st.cache(show_spinner=False)
def parseInfo(playerInfo):
    if "currentAge" in playerInfo:
        age = playerInfo["currentAge"]
    elif "birthDate" in playerInfo:
        birthDate = playerInfo["birthDate"]
        born = datetime.strptime(birthDate, "%Y-%m-%d")
        today = date.today()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    else:
        age = "No data"
    height = playerInfo["height"]
    weight = playerInfo["weight"]
    primaryPosition = playerInfo["primaryPosition"]["code"]
    return age, height, weight, primaryPosition

def displayStats(stats1, stats2, statsType):
    def computeColorDict(dict1, dict2, keys):
        colorDict = dict()
        for key in keys:
            if dict1[key] > dict2[key]:
                colorDict[key] = ["forestgreen", "crimson"]
            elif dict1[key] < dict2[key]:
                colorDict[key] = ["crimson", "forestgreen"]
            else:
                colorDict[key] = ["darkgrey", "darkgrey"]
        return colorDict

    if statsType == "F":
        keys = [
            "games",
            "goals",
            "assists",
            "points",
            "plusMinus",
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
        footnote_string = f"""GP - Games Played; G - Goals; A - Assists; P - Points; +/- - Plus/Minus;
                                PIM - Penalty Minutes; PPG - Power Play Goals; PPP - Powe Play Points;
                                SHG - Shorthanded Goals; SHG - Shorthanded Points; GWG - Game Winning Goals;
                                OTG - Overtime Goals; S - Shots; S% - Shooting Percentage
                            """

    if statsType == "G":
        keys = [
            "games",
            "gamesStarted",
            "wins",
            "losses",
            "ot",
            "shotsAgainst",
            "goalsAgainst",
            "goalAgainstAverage",
            "savePercentage",
            "shutouts"
        ]
        footnote_string = f"""GP - Games Played; GS - Games Started; W - Wins; L - Losses; OT - Overtime losses;
                              SA - Shots Against; GA - Goals Against; GAA - Goals Against Average;
                              SV% - Save Percentage; SO - Shutouts
                            """

    if statsType == "T":
        keys = [
            "gamesPlayed",
            "wins",
            "losses",
            "ot",
            "pts",
            "ptPctg",
            "goalsPerGame",
            "goalsAgainstPerGame",
            "evGGARatio",
            "powerPlayOpportunities",
            "powerPlayPercentage",
            "powerPlayGoals",
            "powerPlayGoalsAgainst",
            "shotsPerGame",
            "shotsAllowed",
            "faceOffsTaken",
            "faceOffWinPercentage",
            "shootingPctg",
            "savePctg"
        ]

        footnote_string = f"""GP - Games Played; W - Wins; L - Losses; OT - Overtime/Shootout Losses (Worth One Point);
                              PTS - Points; PTS% - Points Percentage; GFA - Goals Per Game; GAA - Goals Against Per Game;
                              GGARatio - Goals Scored Versus Goals Against Ratio; PP - Power Play Opportunities; PP% - Power Play Percentage;
                              PPG - Power Play Goals; PPGA - Power Play Goals Against; SA - Shots Per Game; SAA - Shots Allowed Per Game;
                              FO - Face Offs Taken; FO% - Face Off Winning Percentage; S% - Shooting Percentage;
                              SV% - Save Percentage
                            """

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
        "shotPct": "S%",
        "gamesStarted": "GS",
        "wins": "W",
        "losses": "L",
        "ot": "OT",
        "shotsAgainst": "SA",
        "goalsAgainst": "GA",
        "goalAgainstAverage": "GAA",
        "savePercentage": "SV%",
        "shutouts": "SO",
        "gamesPlayed": "GP",
        "pts": "PTS",
        "ptPctg": "PTS%",
        "goalsPerGame": "GFA",
        "goalsAgainstPerGame": "GAA",
        "evGGARatio": "GGARatio",
        "powerPlayPercentage": "PP%",
        "powerPlayGoalsAgainst": "PPGA",
        "powerPlayOpportunities": "PP",
        "shotsPerGame": "SA",
        "shotsAllowed": "SAA",
        "faceOffsTaken": "FO",
        "faceOffWinPercentage": "FO%",
        "shootingPctg": "S%",
        "savePctg": "SV%"

    }

    colorDict = computeColorDict(stats1, stats2, keys)

    if statsType == "T":
        stats1 = {k:int(float(v)) if int(float(v)) == float(v) else float(v) for k,v in stats1.items()}
        stats2 = {k:int(float(v)) if int(float(v)) == float(v) else float(v) for k,v in stats2.items()}

    limits = {k: 1.1*(abs(stats1[k]) + abs(stats2[k]))+0.05 for k in set(stats1) if k in keys}

    layouts = {}
    layouts["xaxis"] = {}
    fig = make_subplots(rows=len(keys), cols=2)
    for i in range(2*len(keys)):
        row = (i+2)//2
        key = keys[row-1]

        if i % 2 == 0:
            fig.append_trace(
                go.Bar(
                    y=[key],
                    x=[abs(stats1[key])],
                    orientation="h",
                    text=stats1[key],
                    textposition="outside",
                    marker={"color": colorDict[key][0], "line":{"color":"black"}}),
                    row=row,
                    col=1
                )
            if i == 0:
                layouts["xaxis"]["range"] = [limits[key],0]
                layouts["yaxis"] = {"showticklabels" : False}
            else:
                layouts["xaxis"+str(i+1)] = {}
                layouts["xaxis"+str(i+1)]["range"] = [limits[key],0]
                layouts["yaxis"+str(i+1)] = {"showticklabels" : False}
        else:
            fig.append_trace(
                go.Bar(
                    y=[f"{abbr[key]:{' '}<{12}}"],
                    x=[abs(stats2[key])],
                    orientation="h",
                    text=stats2[key],
                    textposition="outside",
                    marker={"color": colorDict[key][1], "line":{"color":"black"}}),
                    row=row,
                    col=2)
            layouts["xaxis"+str(i+1)] = {}
            layouts["xaxis"+str(i+1)]["range"] = [0, limits[key]]

    fig.update_layout(**layouts,
        showlegend=False,
        height=500,
        font={"family":"Arial"},
        margin=dict(b=0, t=0, l=0, r=0))
    fig.update_xaxes(showticklabels=False, showgrid=False)

    return fig, footnote_string

@st.cache(show_spinner=False)
def displayScores(scores1, scores2, shots1, shots2):
    arena = Image.open("./data/rink.png")

    xScores1 = [i["x"] for i in scores1]
    yScores1 = [i["y"] for i in scores1]
    xScores2 = [i["x"] for i in scores2]
    yScores2 = [i["y"] for i in scores2]

    xShots1 = [i["x"] for i in shots1]
    yShots1 = [i["y"] for i in shots1]
    xShots2 = [i["x"] for i in shots2]
    yShots2 = [i["y"] for i in shots2]

    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.0)
    fig.add_layout_image(
        dict(
            source=arena,
            xref="x",
            yref="y",
            x=-42.5,
            y=100,
            sizex=85,
            sizey=200,
            sizing="stretch",
            opacity=1.0,
            layer="below"),
        row=1,
        col=1
    )

    fig.add_layout_image(
        dict(
            source=arena,
            xref="x",
            yref="y",
            x=-42.5,
            y=100,
            sizex=85,
            sizey=200,
            sizing="stretch",
            opacity=1.0,
            layer="below"),
        row=1,
        col=2
    )

    fig.add_trace(
        go.Scatter(
            x=yShots1,
            y=xShots1,
            mode="markers",
            marker=dict(size=12, color="orangered", opacity=0.8, line=dict(width=2, color="DarkSlateGrey"))
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=yShots2,
            y=xShots2,
            mode="markers",
            marker=dict(size=12, color="orangered", opacity=0.8, line=dict(width=2, color="DarkSlateGrey"))
        ),
        row=1,
        col=2
    )

    fig.add_trace(
        go.Scatter(
            x=yScores1,
            y=xScores1,
            mode="markers",
            marker=dict(size=12, color="lime", opacity=0.8, line=dict(width=2, color="DarkSlateGrey"))
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=yScores2,
            y=xScores2,
            mode="markers",
            marker=dict(size=12, color="lime", opacity=0.8, line=dict(width=2, color="DarkSlateGrey"))
        ),
        row=1,
        col=2
    )

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                showactive=True,
                x=0.42,
                xanchor="left",
                y=1.05,
                yanchor="top",
                buttons=list(
                    [
                        dict(
                            label="Goals",
                            method="update",
                            args=[
                                {"visible": [False, False, True, True]}
                            ]
                        ),
                        dict(
                            label="Shots",
                            method="update",
                            args=[
                                {"visible": [True, True, False, False]}
                            ]
                        ),
                        dict(
                            label="Both",
                            method="update",
                            args=[
                                {"visible": [True, True, True, True]}
                            ]
                        )
                    ]
                )
            )
        ]
    )

    fig.update_layout(
        yaxis_scaleanchor="x",
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        xaxis_range=[-42.5,42.5],
        yaxis_range=[-100,100],
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_zeroline=False,
        yaxis2_scaleanchor="x2",
        xaxis2_showticklabels=False,
        yaxis2_showticklabels=False,
        xaxis2_range=[-42.5,42.5],
        yaxis2_range=[-100,100],
        xaxis2_showgrid=False,
        yaxis2_showgrid=False,
        xaxis2_zeroline=False,
        yaxis2_zeroline=False,
        margin=dict(b=0, t=0, l=0, r=0),
        showlegend=False,
        height=4*200,
        width=8*85,
        template="plotly_white"
    )

    for trace in fig.data:
        if trace["marker"]["color"] == "orangered":
            trace.update(visible=False)
    return fig

@st.cache(show_spinner=False)
def displayTeamLogo(logoURL):

    fig = go.Figure()

    fig.add_layout_image(
        dict(
            source=logoURL,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            sizex=1.0,
            sizey=1.0,
            xanchor="center",
            yanchor="middle",
            opacity=1.0,
            layer="above"
        )
    )

    fig.update_layout(
        yaxis_scaleanchor="x",
        yaxis_scaleratio=1,
        xaxis_range=[0,1],
        yaxis_range=[0,1],
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        height=100,
        template="plotly_white",
        margin=dict(b=0, t=0, l=0, r=0)
    )

    return fig

@st.cache(show_spinner=False)
def displayPlayerInfo(age, height, weight):

    s1 = f"Age               {age}"
    s2 = f"Height         {height}"
    s3 = f"Weight      {weight} lb"


    fig = go.Figure()

    fig.add_annotation(
        x=0.5,
        y=0.8,
        xref="paper",
        yref="paper",
        xanchor="center",
        yanchor="middle",
        align="left",
        text=s1,
        font=dict(
            family="Arial",
            size=20
            ),
        showarrow=False
    )

    fig.add_annotation(
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        xanchor="center",
        yanchor="middle",
        align="left",
        text=s2,
        font=dict(
            family="Arial",
            size=20
            ),
        showarrow=False
    )

    fig.add_annotation(
        x=0.5,
        y=0.2,
        xref="paper",
        yref="paper",
        xanchor="center",
        yanchor="middle",
        align="left",
        text=s3,
        font=dict(
            family="Arial",
            size=20
            ),
        showarrow=False
    )

    fig.update_layout(
        xaxis_range=[0,1],
        yaxis_range=[0,1],
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        height=100,
        template="plotly_white",
        margin=dict(b=0, t=0, l=0, r=0)
    )

    return fig