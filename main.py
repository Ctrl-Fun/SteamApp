import os 
import endpoints
from utils import *

token = os.environ["TOKEN"]
base_path = os.environ["BASE_PATH"]
app_id = 578080

# Starting App: Loading Endpoints
endpoints_url = endpoints.GetApiEndpoints()

# Get and Save All Api Info
response = endpoints.GetApiList(basePath=base_path, token=token)
response_public = endpoints.GetApiList(basePath=base_path)
saveJSON(response)
saveJSON(response_public, "dataPublic.json")
ApiMethodsList(publicFilePath="src/dataPublic.json" , privateFilePath="src/data.json")

# Testing GetNewsForApp
endpoints.GetNewsForApp(appId=app_id)