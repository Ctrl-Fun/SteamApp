import os 
import endpoints
import colors
from utils import *

token = os.environ["TOKEN"]
base_path = os.environ["BASE_PATH"]
app_id = 578080


### STARTING APP
print(f'{colors.Green["linestart"]}Starting App...{colors.Green["lineend"]}')
# Starting App: Loading Endpoints
endpoints_url = endpoints.GetApiEndpoints()
# Starting App: Loading Endpoints
userFriends = endpoints.GetUserFriends()
# Starting App: Loading  User Games
userGames = endpoints.GetUserGames()
print(f'{colors.Green["linestart"]}Data loaded{colors.Green["lineend"]}')

# Get and Save All Api Info
# response = endpoints.GetApiList(basePath=base_path, token=token)
# response_public = endpoints.GetApiList(basePath=base_path)
# saveJSON(response)
# saveJSON(response_public, "dataPublic.json")
# ApiMethodsList(publicFilePath="src/dataPublic.json" , privateFilePath="src/data.json")

# Testing GetNewsForApp
def GetNewsForApp():
    print("\n")
    print("Testing GetNewsForApp")
    endpoints.GetNewsForApp(appId=app_id)

GetNewsForApp()



# for i in range(len(userFriends["friends"])):
    # print(userFriends["friends"][i])
    # steamId = userFriends["friends"][i]["steamid"]
    # userName =  endpoints.GetPlayerSummaries(steamId=steamId)["players"][0]["personaname"]
    # print(colors.boldPurple["linestart"]+userName+colors.boldPurple["lineend"])
    # print(steamId)
    # userGames = endpoints.GetUserGames(steamId=steamId)
    # if(userGames):
    #     for i in range(userGames["game_count"]):
    #         print(userGames["games"][i]["name"])

# for steamId in 
# endpoints.GetPlayerSummaries()

# Testing GetAchivements
def GetAchivements():
    print("\n")
    print("Testing GetAchivements")
    endpoints.GetAchivements(appId=app_id, steamId=76561199042832616)

GetAchivements()