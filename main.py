import os 
import endpoints

token = os.environ["TOKEN"]
base_path = os.environ["BASE_PATH"]
app_id = 578080

endpoints.GetNewsForApp(basePath=base_path, appId=app_id)