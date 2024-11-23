import os
import requests
import utils
from errors import error as error

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
            endpoint = f"https://api.steampowered.com/{intName}/{methodName}/v{version}/"
            endpoints[methodName] = endpoint

    utils.saveJSON(endpoints, "endpoints.json")

# Games list
# def GetGamesList():

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
        print("\033[32mLas noticias del juego son:\033[0m")
        for new in newsitems:
            print(new["title"])
    return appnews

