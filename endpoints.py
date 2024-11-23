import requests
from errors import error as error

# Games list
# def GetGamesList():

# Game news
def GetNewsForApp(basePath: str, appId: str, count:str = "3", maxLength:str = "300", format:str = "json", displayNews:bool = True):
    data = requests.get(f"{basePath}/ISteamNews/GetNewsForApp/v0002/?appid={appId}&count={count}&maxlength={maxLength}&format={format}")
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
