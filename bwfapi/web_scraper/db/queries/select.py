
def query_player_id_by_name(player_name):
    return f"SELECT `ID` FROM `Player` where `Name` = '{player_name}';"