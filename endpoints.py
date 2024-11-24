import os
import requests
import colors
import utils
from errors import error as error
import json

# API List
def GetApiList(basePath: str, token: str = ""):
    key =""
    if(token != ""):
        key = f"/?key={token}"

    data = requests.get(f"{basePath}/ISteamWebAPIUtil/GetSupportedAPIList/v0001{key}")
    if(not data.ok):
        error("Error in request")
        return
    return data.json()

# API List
def GetApiEndpoints():
    token = os.environ["TOKEN"]
    base_path = os.environ["BASE_PATH"]
    url = f"{base_path}/ISteamWebAPIUtil/GetSupportedAPIList/v0001/?key={token}"
    response = requests.get(url)

    if(not response.ok):
        error("Error loading endpoints")
        return
    
    data = response.json()
    interfaces = data['apilist']['interfaces']
    endpoints = {}

    for interface in interfaces:
        intName = interface['name']
        for method in interface['methods']:
            methodName = method['name']
            version = method['version']
            # Construir la ruta del endpoint
            endpoint = f"{base_path}/{intName}/{methodName}/v{version}/"
            endpoints[methodName] = endpoint

    utils.saveJSON(endpoints, "endpoints.json")

# Games list (maybe in the future...)
# def GetGamesList(dlc: bool = False, maxResults: int = 10000):
#     token = os.environ["TOKEN"]
    


# Game news
def GetNewsForApp(appId: str, count:str = "3", maxLength:str = "300", format:str = "json", displayNews:bool = True):
    endpoint_url = utils.getEndpoint("GetNewsForApp")
    data = requests.get(f"{endpoint_url}?appid={appId}&count={count}&maxlength={maxLength}&format={format}")
    if(not data.ok):
        error("Error in request")
        return
    
    appnews = data.json()["appnews"]
    newsitems = appnews["newsitems"]
    if(displayNews):
        print(f"{colors.Green["linestart"]}Las noticias del juego son:{colors.Green["lineend"]}")
        for new in newsitems:
            print(new["title"])
    return appnews

def GetUserGames(steamId: int=os.environ["STEAM_ID"], appInfo:bool = True, freeGames: bool = True, freeSub: bool = True, SkipUnvettedApps: bool = False, language: str = "Spanish", extendedInfo: bool = True):
    token = os.environ["TOKEN"]
    # steamId = os.environ["STEAM_ID"]
    endpoint_url = utils.getEndpoint("GetOwnedGames")
    data = requests.get(f"{endpoint_url}?key={token}&steamid={steamId}&include_appinfo={appInfo}&include_played_free_games={freeGames}&skip_unvetted_apps={SkipUnvettedApps}&language={language}&include_extended_appinfo={extendedInfo}")
    
    if(not data.ok):
        error("Error getting user games information")
        return
    # print(json.dumps(data.json(), indent=4))
    return data.json()["response"]

def GetUserFriends():
    token = os.environ["TOKEN"]
    steamId = os.environ["STEAM_ID"]
    endpoint_url = utils.getEndpoint("GetFriendList")
    data = requests.get(f"{endpoint_url}?key={token}&steamid={steamId}")
    
    if(not data.ok):
        error("Error getting user friends")
        return
    
    # print(json.dumps(data.json(), indent=4))
    return data.json()["friendslist"]

def GetPlayerSummaries(steamId: int = os.environ["STEAM_ID"]):
    token = os.environ["TOKEN"]
    endpoint_url =utils.getEndpoint("GetPlayerSummaries")
    data = requests.get(f"{endpoint_url}?key={token}&steamids={steamId}")
    if(not data.ok):
        error("Error getting user info")
        print(data)
        return 
    
    # print(json.dumps(data.json(), indent=4))
    return data.json()["response"]

def GetAchivements(appId: int, steamId: int = os.environ["STEAM_ID"]):
    token = os.environ["TOKEN"]
    endpoint_url =utils.getEndpoint("GetPlayerAchievements")
    print(f"{endpoint_url}?key={token}&steamid={steamId}&appid{appId}")
    data = requests.get(f"{endpoint_url}?key={token}&steamid={steamId}&appid={appId}")
    if(not data.ok):
        error("Error getting user achievements")
        print(data)
        return 
    print(json.dumps(data.json(), indent=4))
    # return data.json()["friendslist"]