import os 
import endpoints
from utils import *

token = os.environ["TOKEN"]
# base_path = os.environ["BASE_PATH"]
base_path = "http://api.steampowered.com"
app_id = 578080

# endpoints.GetNewsForApp(basePath=base_path, appId=app_id)
response = endpoints.GetApiList(basePath=base_path, token=token)
response_public = endpoints.GetApiList(basePath=base_path)

saveJSON(response)
saveJSON(response_public, "dataPublic.json")
# print(response)

ApiMethodsList(publicFilePath="src/dataPublic.json" , privateFilePath="src/data.json")