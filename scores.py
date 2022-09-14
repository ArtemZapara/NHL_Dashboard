import requests
import pickle

gameData = list()
year = "2021"
seasonType = "02"
maxGameId = 1312

allScores = dict()
allShots = dict()
for game in range(1,maxGameId):
    r = requests.get(url=f"http://statsapi.web.nhl.com/api/v1/game/{year}{seasonType}{str(game).zfill(4)}/feed/live")
    data = r.json()
    if "liveData" not in data.keys():
        print(game)
    else:
        plays = data["liveData"]["plays"]["allPlays"]
        for play in plays:
            if "players" in play:
                for player in play["players"]:
                    if player["playerType"] == "Scorer" and play["about"]["periodType"] != "SHOOTOUT":
                        playerID = player["player"]["id"]
                        x = play["coordinates"]["x"]
                        y = play["coordinates"]["y"]
                        if x < 0:
                            x = -x
                            y = -y
                        if playerID not in allScores:
                            allScores[playerID] = list()
                        allScores[playerID].append({"x": x, "y": y})

                    if player["playerType"] == "Shooter" and play["result"]["event"] == "Shot":
                        playerID = player["player"]["id"]
                        x = play["coordinates"]["x"]
                        y = play["coordinates"]["y"]
                        if x < 0:
                            x = -x
                            y = -y
                        if playerID not in allShots:
                            allShots[playerID] = list()
                        allShots[playerID].append({"x": x, "y": y})

with open(f"./data/allScores2021.pkl", "wb") as file:
    pickle.dump(allScores, file, pickle.HIGHEST_PROTOCOL)

with open(f"./data/allShots2021.pkl", "wb") as file:
    pickle.dump(allShots, file, pickle.HIGHEST_PROTOCOL)