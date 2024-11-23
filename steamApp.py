import os
import requests

token = os.environ["TOKEN"]
base_path = " http://api.steampowered.com"
app_id = 578080


def GetNewsForApp(basePath: str, appId: str, count:str = "3", maxlength:str = "300", format:str = "json"):
    data = requests.get(f"{basePath}/ISteamNews/GetNewsForApp/v0002/?appid={appId}&count={count}&maxlength={maxlength}&format={format}")
    if(not data.ok):
        # print("Error in news request")
        return
    print(data.json())
    return data.json()


GetNewsForApp(basePath=base_path, appId=app_id)