import os 
from modules.logging import error as error
from dotenv import load_dotenv
import modules.endpoints as endpoints
import modules.colors as colors
from modules.utils import *
from modules.database import Database
from modules.init import Init

### STARTING APP

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN")
BASE_PATH = os.getenv("BASE_PATH")
STEAM_ID = os.getenv("STEAM_ID")


database=Database()

# Get and Save All Endpoints Info
table_name = "endpoints"
table_data = [
    ["name", "VARCHAR(255)"],
    ["url", "TEXT"]
]

tableExist = database.table_exists(table_name)
if(not tableExist):
    database.create_table(table_name, table_data)

rows_count = database.is_table_filled(table_name)
if(rows_count == 0):
    table_content = endpoints.GetApiEndpoints(TOKEN, BASE_PATH)
    database.fill_table(table_name, table_data, table_content)

# Get and Save all User Games Info
# table_name = "user_games"
# table_data = [
#     ["appid", "INTEGER"],
#     ["name", "VARCHAR(255)"],
#     ["playtime_forever", "INTEGER"],
#     ["img_icon_url", "VARCHAR(255)"],
#     ["has_community_visible_stats", "BOOLEAN"],
#     ["playtime_windows_forever", "INTEGER"],
#     ["playtime_mac_forever", "INTEGER"],
#     ["playtime_linux_forever", "INTEGER"],
#     ["playtime_deck_forever", "INTEGER"],
#     ["rtime_last_played", "INTEGER"],
#     ["capsule_filename", "VARCHAR(255)"],
#     ["has_workshop", "BOOLEAN"],
#     ["has_market", "BOOLEAN"],
#     ["has_dlc", "BOOLEAN"],
#     ["content_descriptorids", "TEXT"],  # Se almacena como JSON o un array en formato de texto
#     ["playtime_disconnected", "INTEGER"]
# ]
# tableExist = database.table_exists(table_name)
# if(not tableExist):
#     database.create_table(table_name, table_data)

# rows_count = database.is_table_filled(table_name)
# if(rows_count == 0):
#     table_content = endpoints.GetUserGames(token=TOKEN,steamId=STEAM_ID)
#     database.fill_table(table_name, table_data, table_content)


# print(table_content)
# database.fill_table(table_name, table_data, table_content)



user_games_endpoint = database.select_from_table('endpoints', ['url'], 'name = "GetOwnedGames"')
print(user_games_endpoint)

# table_content = endpoints.GetUserGames(token=TOKEN, steamId=STEAM_ID)
# print(table_content)

# table_content = endpoints.GetApiEndpoints(TOKEN, BASE_PATH)
# print(table_content)