
INSERTS = {}

INSERTS['player'] = (
    'INSERT INTO Player '
    ' (ID, Name, Country, BirthDate)'
    ' VALUES (%s, %s, %s, %s)'
    ';'
    )

INSERTS['tournament'] = (
    'INSERT INTO Tournament '
    ' (ID,`StartDate`, `EndDate`, name)'
    ' VALUES (%s, %s, %s, %s)'
    ';'
    )

INSERTS['match'] = (
    'INSERT INTO `Match` '
    ' (WinnerID, LoserID, TournamentID, `Event`, `Time`, `Duration`)'
    ' VALUES (%s, %s, %s, %s, %s, %s)'
    ';'
    )

INSERTS['set'] = (
    'INSERT INTO `Set` '
    ' (MatchID, WinnerScore, LoserScore, Round)'
    ' VALUES (%s, %s, %s, %s)'
    ';'
    )
def get_insert_queries():
    return INSERTS
