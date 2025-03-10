import sys
from modules.logging import error, success
import modules.endpoints as endpoints
from modules.database import Database
import modules.dictionary as dictionary
import os
from dotenv import load_dotenv
from modules.returndata import ReturnData



class Init():
    def __init__(self):
        success("Starting App...")
        # Starting App: Loading Endpoints
        # Load environment variables
        load_dotenv()

        TOKEN = os.getenv("TOKEN")
        BASE_PATH = os.getenv("BASE_PATH")
        STEAM_ID = os.getenv("STEAM_ID")
        database=Database()

        # Get and Save All Endpoints Info
        self.load_endpoints(database, TOKEN, BASE_PATH)

        # Get and Save all User Games Info
        self.load_user_games(database, TOKEN, STEAM_ID)

        # Get and Save all User Friends Info
        self.load_user_friends(database, TOKEN, STEAM_ID)

        success("Data loaded successfully")

    @staticmethod
    def load_endpoints(database : Database, TOKEN: str, BASE_PATH: str):
        try:
            table_name = "endpoints"
            table_structure = dictionary.Database['endpoints']
            tableExist = database.table_exists(table_name)
            if(not tableExist):
                # regular endpoints
                database.create_table(table_name, table_structure)
                table_content = endpoints.GetApiEndpoints(TOKEN, BASE_PATH)
                database.fill_table(table_name, table_content)
                # external endpoint
                familyGamesEndpoint = [["GetSharedLibraryApps","https://api.steampowered.com/IFamilyGroupsService/GetSharedLibraryApps/v1/"]]
                database.fill_table(table_name, familyGamesEndpoint)
            else:
                filled_table = database.is_table_filled(table_name)
                if(not filled_table):
                    table_content = endpoints.GetApiEndpoints(TOKEN, BASE_PATH)
                    database.fill_table(table_name, table_content)
                    familyGamesEndpoint = [["GetSharedLibraryApps","https://api.steampowered.com/IFamilyGroupsService/GetSharedLibraryApps/v1/"]]
                    database.fill_table(table_name, familyGamesEndpoint)
        except Exception as e:
            error(f"Error crítico: str({e})")
            sys.exit()

    @staticmethod
    def load_user_games(database : Database, TOKEN: str, STEAM_ID: str):
        # table_content = endpoints.GetFamilyGames()
        table_content = None # Bypass family games, endpoint not official suported by steam
        if(table_content != None):
            # print("family games")
            table_name = "family_games"
            table_data = dictionary.Database['family_games']
            tableExist = database.table_exists(table_name)
            if(not tableExist):
                database.create_table(table_name, table_data)
            rows_count = database.is_table_filled(table_name)
            if(rows_count == 0):
                database.fill_table(table_name, table_content)
        else:
            # print("user games")
            table_name = "user_games"
            table_data = dictionary.Database['user_games']
            tableExist = database.table_exists(table_name)
            if(not tableExist):
                database.create_table(table_name, table_data)

            rows_count = database.is_table_filled(table_name)
            if(not rows_count):
                table_content = endpoints.GetUserGames(token=TOKEN,steamId=STEAM_ID)
                database.fill_table(table_name, table_content)

    @staticmethod
    def load_user_friends(database : Database, TOKEN: str, STEAM_ID: str):
        table_name = "user_friends"
        table_data = dictionary.Database['user_friends']
        tableExist = database.table_exists(table_name)
        if(not tableExist):
            database.create_table(table_name, table_data)

        rows_count = database.is_table_filled(table_name)
        if(not rows_count):
            table_content = endpoints.GetUserFriends(token=TOKEN,steamId=STEAM_ID)
            database.fill_table(table_name, table_content)