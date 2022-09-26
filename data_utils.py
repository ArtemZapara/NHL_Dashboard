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
    This function returns the fulle list of teams.
    """

    URL = "https://statsapi.web.nhl.com/api/v1/teams"
    r = requests.get(url=URL)
    teamData = r.json()
    teamList = teamData["teams"]
    return teamList

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
        plays = data["liveData"]["plays"]["allPlays"]
        for play in plays:
            if "players" in play:
                for player in play["players"]:
                    if (
                        player["playerType"] == "Scorer"
                        and play["about"]["periodType"] != "SHOOTOUT"
                        ):
                        playerID = player["player"]["id"]
                        x = play["coordinates"]["x"]
                        y = play["coordinates"]["y"]
                        if x < 0:
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
                        playerID = player["player"]["id"]
                        x = play["coordinates"]["x"]
                        y = play["coordinates"]["y"]
                        if x < 0:
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