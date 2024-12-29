from modules.database import Database
from modules.logging import success

# Display most played games by user
# Solo trae los juegos más jugados por el usuario que son propiedad suya (no juegos de amigos, etc.)
def top_games():
    database=Database()
    most_played_games = database.select_from_table('user_games', ['name', 'playtime_forever'], where_clause=None, order_by='playtime_forever DESC', limit=10)
    success("Top 10 Games Played By The User:")

    max_name_length = max(len(game[0]) for game in most_played_games)
    
    for game in most_played_games:
        minutos = game[1]
        horas = minutos // 60  # División entera para obtener las horas completas
        minutos_restantes = minutos % 60
        game_time = f"{horas}:{minutos_restantes} h"
        print(f"{game[0].ljust(max_name_length)}: {game_time} minutes")
    # print(most_played_games)