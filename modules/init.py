from modules.logging import error, success
import modules.endpoints as endpoints
from modules.database import Database

class Init():
    def __init__(self):
        success("Starting App...")
        # Starting App: Loading Endpoints
        db = Database()
        table_name = "endpoints"
        table_data = [
            ["name", "VARCHAR(255)"],
            ["url", "TEXT"]
        ]
        table_content = endpoints.GetApiEndpoints()
        db.fillTable(tableName=table_name, tableData=table_data, data=table_content)

        # Starting App: Loading Endpoints
        # userFriends = endpoints.GetUserFriends()
        # Starting App: Loading  User Games
        # userGames = endpoints.GetUserGames()
        success("Data loaded")