import requests
import pickle

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

if __name__ == "__main__":

    seasons = ["20212022"]
    playerList = fetchPlayerList(seasons)
    with open("./data/playerList.pkl", "wb") as file:
        pickle.dump(playerList, file)

    teamList = fetchTeamList()
    with open("./data/teamList.pkl", "wb") as file:
        pickle.dump(teamList, file)