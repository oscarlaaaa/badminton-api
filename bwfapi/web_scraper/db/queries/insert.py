
INSERTS = {}

INSERTS['player'] = (
    'INSERT INTO Player '
    ' (id, name)'
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
    ' (`Date`, name)'
    ' VALUES (%s, %s)'
    ';'
    )

def get_insert_queries():
    return INSERTS

DEFAULT_INSERTS = {}

DEFAULT_INSERTS['event'] = [
    ('INSERT INTO Event (name)'
    ' VALUES ("MS")'
    ';'),
    ('INSERT INTO Event (name)'
    ' VALUES ("WS")'
    ';'),
]

def get_default_queries():
    return DEFAULT_INSERTS