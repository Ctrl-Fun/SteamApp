import os
import requests
import modules.utils as utils
from modules.logging import error, success
import json
from modules.database import Database
import modules.dictionary as dictionary


# API List (WE MUST REMOVE THIS FUNCTION)
def GetApiList(basePath: str, token: str = ""):
    key =""
    if(token != ""):
        key = f"/?key={token}"

    data = requests.get(f"{basePath}/ISteamWebAPIUtil/GetSupportedAPIList/v0001{key}")
    if(not data.ok):
        error("Error in request")
        return
    return data.json()

# INIT FUNCTIONS
# Save data but don't display information
def GetApiEndpoints(token: int, base_path: str):
    url = f"{base_path}/ISteamWebAPIUtil/GetSupportedAPIList/v0001/?key={token}"
    response = requests.get(url)

    if(not response.ok):
        error("Error loading endpoints")
        return
    
    data = response.json()
    interfaces = data['apilist']['interfaces']
    endpoints = []

    for interface in interfaces:
        intName = interface['name']
        for method in interface['methods']:
            methodName = method['name']
            version = method['version']
            # Construir la ruta del endpoint
            endpoint = f"{base_path}/{intName}/{methodName}/v{version}/"
            result = [methodName, endpoint]
        
            endpoints.append(result)
    return(endpoints)

def GetUserGames(token: int, steamId: int, appInfo:bool = True, freeGames: bool = True, SkipUnvettedApps: bool = False, language: str = "Spanish", extendedInfo: bool = True):
    fields = dictionary.Endpoints['get_user_games']
    database=Database()
    endpoint_array = database.select_from_table('endpoints', ['url'], 'name = "GetOwnedGames"')
    endpoint_url = endpoint_array[0][0]
    data = requests.get(f"{endpoint_url}?key={token}&steamid={steamId}&include_appinfo={appInfo}&include_played_free_games={freeGames}&skip_unvetted_apps={SkipUnvettedApps}&language={language}&include_extended_appinfo={extendedInfo}")
    
    if(not data.ok):
        error("Error getting user games information")
        return

    data = data.json()["response"] # we must re-think this, this field cannot exist

    response = [
        list(game.get(field, None) for field in fields) for game in data['games']
    ]

    return response

def GetFamilyGames(freeGames: bool = True):
    fields = dictionary.Endpoints['get_family_games']
    database=Database()
    endpoint_array = database.select_from_table('endpoints', ['url'], 'name = "GetSharedLibraryApps"')
    try:
        endpoint_url = endpoint_array[0][0]
        web_api_token = input("Introduce tu token temporal de la web api (Si NO deseas ver los juegos de tu familia pulsa ENTER sin escribir nada): ")

        if(web_api_token == ""):
            return
        
        data = requests.get(f"{endpoint_url}?access_token={web_api_token}&family_groupid=0&include_own=true&include_excluded=true&include_free={freeGames}&include_non_games=false")

        if(data.status_code == 401):
            error("Error getting family games information: Unauthorized")
            return

        if(not data.ok):
            error("Error getting family games information")
            return
        
        data = data.json()['response'] # we must re-think this, this field cannot exist
        response = [
            list(game.get(field, None) for field in fields) for game in data['apps']
        ]
        return response
    
    except Exception as e:
        error("Error getting family games information: "+str(e))
        return

def GetUserFriends(token: int, steamId: int):
    fields = dictionary.Endpoints['get_user_friends']
    database=Database()
    endpoint_array = database.select_from_table('endpoints', ['url'], 'name = "GetFriendList"')
    endpoint_url = endpoint_array[0][0]
    data = requests.get(f"{endpoint_url}?key={token}&steamid={steamId}")
    
    if(not data.ok):
        error("Error getting user friends")
        return
    
    data = data.json()["friendslist"] # we must re-think this, this field cannot exist

    response = [
        list(friend.get(field, None) for field in fields) for friend in data['friends']
    ]

    return response

# Games list (maybe in the future...)
# def GetGamesList(dlc: bool = False, maxResults: int = 10000):
#     token = os.environ["TOKEN"]

# Game news
# GENERAL FUNCTIONS
# Don't save data but display information

def GetNewsForApp(appId: str, count:str = "3", maxLength:str = "300", format:str = "json", displayNews:bool = True):
    endpoint_url = utils.getEndpoint("GetNewsForApp")
    data = requests.get(f"{endpoint_url}?appid={appId}&count={count}&maxlength={maxLength}&format={format}")
    if(not data.ok):
        error("Error in request")
        return
    
    appnews = data.json()["appnews"]
    newsitems = appnews["newsitems"]
    if(displayNews):
        success("Las noticias del juego son:")
        for new in newsitems:
            print(new["title"])
    return appnews

def GetPlayerSummaries(steamId: int):
    token = os.environ["TOKEN"]
    # endpoint_url =utils.getEndpoint("GetPlayerSummaries")
    database=Database()
    endpoint_array = database.select_from_table('endpoints', ['url'], 'name = "GetPlayerSummaries"')
    data = requests.get(f"{endpoint_array[0][0]}?key={token}&steamids={steamId}")
    if(not data.ok):
        error("Error getting user info")
        print(data)
        return 
    
    return data.json()["response"]

def GetAchivements(appId: int, steamId: int):
    token = os.environ["TOKEN"]
    endpoint_url =utils.getEndpoint("GetPlayerAchievements")
    data = requests.get(f"{endpoint_url}?key={token}&steamid={steamId}&appid={appId}")
    if(not data.ok):
        if(data.json()["playerstats"]):
            error(data.json()["playerstats"]["error"])
        else:
            error("Error getting user achievements")
        return 
    print(json.dumps(data.json(), indent=4))
    # return data.json()["friendslist"]