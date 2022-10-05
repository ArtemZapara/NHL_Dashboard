import requests
import pickle
import os

def fetchPlayerList(seasons):
    """
    This function returns the list of players for all teams in a given list of seasons.
    """
    playerList = list()
    for season in seasons:
        URL = "https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster&season=" + season
        r = requests.get(url=URL)
        seasonData = r.json()

        teams = seasonData["teams"]
        for team in teams:
            for player in team["roster"]["roster"]:
                playerID = player["person"]["id"]
                URL2 = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
                r2 = requests.get(url=URL2)
                playerData = r2.json()
                playerInfo = playerData["people"][0]
                if playerInfo not in playerList:
                    playerList.append(playerInfo)

    playerList = sorted(playerList, key = lambda x: x["lastName"])
    print(f"The collection of players has been successfully loaded from statsapi.web.nhl.api: in total {len(playerList)} players.")

    return playerList

def fetchTeamList():
    """
    This function returns the full list of teams.
    """

    URL = "https://statsapi.web.nhl.com/api/v1/teams"
    r = requests.get(url=URL)
    teamData = r.json()
    teamList = teamData["teams"]
    return teamList

def mapRinkSide(period):
    """Determines the rink side for HOME and AWAY teams using
    the location of shots/goals for both teams in a given period.

    Args:
        period (list): list with x-coordinates of all shots/goals in a given period.
                        If the shot/goal is comitted by HOME team, then x-coordinates
                        is recorded as it is, otherwise the x-coordinate is flipped.

    Returns:
        result (dict): dictionary containing the rink side (left or right) for both teams
    """
    negativeCount = len(list(filter(lambda x: (x < 0), period)))
    positiveCount = len(list(filter(lambda x: (x >= 0), period)))
    if positiveCount > negativeCount:
        result = {"home":"left", "away":"right"}
    if positiveCount < negativeCount:
        result = {"home":"right", "away":"left"}
    if positiveCount == negativeCount:
        result = {"home":"UNKNOWN", "away":"UNKNOWN"}
    return result

def detectRinkSide(periods, plays, teamDict):
    per1, per2, per3 = list(), list(), list()
    if len(periods) == 4:
        perOT = list()
    for play in plays:
        if "players" in play:
            for player in play["players"]:
                if (
                player["playerType"] == "Shooter"
                and play["about"]["periodType"] != "SHOOTOUT"
                and play["result"]["event"] in ["Shot", "Missed Shot"]
                ) or (
                player["playerType"] == "Scorer"
                and play["about"]["periodType"] != "SHOOTOUT"
                ):

                    teamID = play["team"]["id"]
                    periodNum = play["about"]["ordinalNum"]
                    shotTeam = teamDict[teamID]

                    x = play["coordinates"]["x"]
                    y = play["coordinates"]["y"]

                    if periodNum == "1st":
                        if shotTeam == "home":
                            per1.append(x)
                        else:
                            per1.append(-x)

                    if periodNum == "2nd":
                        if shotTeam == "home":
                            per2.append(x)
                        else:
                            per2.append(-x)

                    if periodNum == "3rd":
                        if shotTeam == "home":
                            per3.append(x)
                        else:
                            per3.append(-x)

                    if periodNum == "OT":
                        if shotTeam == "home":
                            perOT.append(x)
                        else:
                            perOT.append(-x)

    periods[0]["home"]["rinkSide"] = mapRinkSide(per1)["home"]
    periods[0]["away"]["rinkSide"] = mapRinkSide(per1)["away"]
    periods[1]["home"]["rinkSide"] = mapRinkSide(per2)["home"]
    periods[1]["away"]["rinkSide"] = mapRinkSide(per2)["away"]
    periods[2]["home"]["rinkSide"] = mapRinkSide(per3)["home"]
    periods[2]["away"]["rinkSide"] = mapRinkSide(per3)["away"]
    if len(periods) == 4:
        periods[3]["home"]["rinkSide"] = mapRinkSide(perOT)["home"]
        periods[3]["away"]["rinkSide"] = mapRinkSide(perOT)["away"]

def loadLiveData(season, seasonType):
    allScores = dict()
    allShots = dict()

    standingURL = f"https://statsapi.web.nhl.com/api/v1/standings?season={season}"
    r = requests.get(url=standingURL)
    data = r.json()
    records = data["records"]
    teams = list()
    for record in records:
        for team in record["teamRecords"]:
            teams.append(team["team"])
    nTeams = len(teams)

    seasonURL = f"https://statsapi.web.nhl.com/api/v1/seasons/{season}"
    r = requests.get(url=seasonURL)
    data = r.json()
    nGames = data["seasons"][0]["numberOfGames"]

    maxGameID = int(nTeams * nGames / 2)

    year = season[:4]
    for game in range(1,maxGameID + 1):
        r = requests.get(url=f"http://statsapi.web.nhl.com/api/v1/game/{year}{seasonType}{str(game).zfill(4)}/feed/live")
        data = r.json()
        teams = data["gameData"]["teams"]
        teamDict = {teams["home"]["id"] : "home", teams["away"]["id"] : "away"}
        periods = data["liveData"]["linescore"]["periods"]
        plays = data["liveData"]["plays"]["allPlays"]

        if len(plays) == 0:
            continue

        if "rinkSide" not in periods[0]["home"]:
            detectRinkSide(periods, plays, teamDict)

        for play in plays:
            if "players" in play:
                for player in play["players"]:
                    if (
                        player["playerType"] == "Scorer"
                        and play["about"]["periodType"] != "SHOOTOUT"
                        ):
                        teamID = play["team"]["id"]
                        periodNum = play["about"]["ordinalNum"]
                        period = [d for d in periods if d["ordinalNum"] == periodNum][0]
                        scoredTeam = teamDict[teamID]

                        playerID = player["player"]["id"]
                        x = play["coordinates"]["x"]
                        y = play["coordinates"]["y"]

                        scoredSide = period[scoredTeam]["rinkSide"]
                        if scoredSide == "right":
                            x = -x
                            y = -y

                        if playerID not in allScores:
                            allScores[playerID] = list()

                        allScores[playerID].append({"x": x, "y": y})

                    if (
                        player["playerType"] == "Shooter"
                        and play["about"]["periodType"] != "SHOOTOUT"
                        and play["result"]["event"] == "Shot"
                        ):
                        teamID = play["team"]["id"]
                        periodNum = play["about"]["ordinalNum"]
                        period = [d for d in periods if d["ordinalNum"] == periodNum][0]
                        scoredTeam = teamDict[teamID]

                        playerID = player["player"]["id"]
                        x = play["coordinates"]["x"]
                        y = play["coordinates"]["y"]

                        scoredSide = period[scoredTeam]["rinkSide"]
                        if scoredSide == "right":
                            x = -x
                            y = -y

                        if playerID not in allShots:
                            allShots[playerID] = list()
                        allShots[playerID].append({"x": x, "y": y})

    os.makedirs(f"./data/{season}", exist_ok=True)
    with open(f"./data/{season}/allScores.pkl", "wb") as file:
        pickle.dump(allScores, file, pickle.HIGHEST_PROTOCOL)

    with open(f"./data/{season}/allShots.pkl", "wb") as file:
        pickle.dump(allShots, file, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":

    seasons = [
        "20192020",
        "20202021",
        "20212022"
        ]
    for season in seasons:
        loadLiveData(season, seasonType="02")

    playerList = fetchPlayerList(seasons)
    with open("./data/playerList.pkl", "wb") as file:
        pickle.dump(playerList, file)

    teamList = fetchTeamList()
    with open("./data/teamList.pkl", "wb") as file:
        pickle.dump(teamList, file)