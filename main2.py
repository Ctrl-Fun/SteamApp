import os 
from modules.logging import error, success
import modules.endpoints as endpoints
import modules.colors as colors
from modules.utils import *
from modules.database import Database

database=Database()

app_id = 578080

### STARTING APP


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

# GetNewsForApp()



# for i in range(len(userFriends["friends"])):
    # print(userFriends["friends"][i])
    # steamId = userFriends["friends"][i]["steamid"]
    # userName =  endpoints.GetPlayerSummaries(steamId=steamId)["players"][0]["personaname"]
    # print(colors.boldPurple+userName+colors.End)
    # print(steamId)
# userGames = endpoints.GetFamilyGames()
# print(userGames)
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

# GetAchivements()
