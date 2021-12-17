
INSERTS = {}

INSERTS['player'] = (
    'INSERT IGNORE INTO Player '
    ' (ID, Name, Country, BirthDate, PlayHand, Height)'
    ' VALUES (%s, %s, %s, %s, %s, %s)'
    ';'
    )

INSERTS['tournament'] = (
    'INSERT IGNORE INTO Tournament '
    ' (ID,`StartDate`, `EndDate`, name)'
    ' VALUES (%s, %s, %s, %s)'
    ';'
    )

INSERTS['match'] = (
    'INSERT IGNORE INTO `Match` '
    ' (WinnerID, LoserID, TournamentID, `Event`, `Duration`)'
    ' VALUES (%s, %s, %s, %s, %s)'
    ';'
    )

INSERTS['set'] = (
    'INSERT IGNORE INTO `Set` '
    ' (Round, WinnerID, LoserID, TournamentID, WinnerScore, LoserScore)'
    ' VALUES (%s, %s, %s, %s, %s, %s)'
    ';'
    )
def get_insert_queries():
    return INSERTS
