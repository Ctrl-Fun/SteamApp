from modules.database import Database
from modules.logging import success
import modules.endpoints as endpoints
from datetime import datetime, timezone

# Display most played games by user
# Solo trae los juegos más jugados por el usuario que son propiedad suya (no juegos de amigos, etc.)
def top_games():
    database=Database()
    most_played_games = database.select_from_table('user_games', ['name', 'playtime_forever'], where_clause=None, order_by='playtime_forever DESC', limit=10)
    success("Top 10 Games Played By The User:")
    
    for game in most_played_games:
        minutos = game[1]
        horas = minutos // 60  # División entera para obtener las horas completas
        minutos_restantes = minutos % 60
        game_time = f"{horas}:{minutos_restantes} h"
        print(f"{game[0]:<30}: {game_time}")

# Display user friends
def user_friends():
    database=Database()
    user_friends = database.select_from_table('user_friends', ['steamid', 'relationship', 'friend_since'])
    success("User Friends:")

    for friend in user_friends:
        friend_summaries = endpoints.GetPlayerSummaries(friend[0])
        friend_name = friend_summaries['players'][0]['personaname']
        friend_since = datetime.fromtimestamp(friend[2], tz=timezone.utc).strftime('%Y-%m-%d')
        # friend_since = datetime.utcfromtimestamp(friend[2]).strftime('%Y-%m-%d')
        print(f"{friend_name:<20} {friend[1]:<10} {friend_since:<10}")