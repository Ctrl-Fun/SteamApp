from modules.logging import error, success
import modules.endpoints as endpoints

class Init():
    def __init__(self):
        success("Starting App...")
        # Starting App: Loading Endpoints
        endpoints_url = endpoints.GetApiEndpoints()
        # Starting App: Loading Endpoints
        userFriends = endpoints.GetUserFriends()
        # Starting App: Loading  User Games
        userGames = endpoints.GetUserGames()
        success("Data loaded")