import requests
import pickle

gameData = list()
year = "2021"
seasonType = "02"
maxGameId = 1290

allScores = list()
allShots = list()
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
                    if player["playerType"] == "Scorer":
                        playerID = player["player"]["id"]
                        x = play["coordinates"]["x"]
                        y = play["coordinates"]["y"]
                        if x < 0:
                            x = -x
                            y = -y
                        allScores.append({playerID: {"x": x, "y": y}})

with open(f"./data/allScores2021_2.pkl", "wb") as file:
    pickle.dump(allScores, file, pickle.HIGHEST_PROTOCOL)