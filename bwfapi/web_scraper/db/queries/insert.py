
INSERTS = {}

INSERTS['player'] = (
    'INSERT INTO Player '
    ' (name, country)'
    ' VALUES (%s, %s)'
    ';'
    )

INSERTS['event'] = (
    'INSERT INTO Event '
    ' (name)'
    ' VALUES (%s)'
    ';'
    )
    
INSERTS['tournament'] = (
    'INSERT INTO Tournament '
    ' (`Date`, Name)'
    ' VALUES (%s, %s)'
    ';'
    )

def get_insert_queries():
    return INSERTS