import requests
from errors import error as error

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