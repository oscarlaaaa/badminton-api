DATABASE = {}

DATABASE['drop'] = (
    'DROP DATABASE IF EXISTS bwf_api;'
)

DATABASE['create'] = (
    'CREATE DATABASE IF NOT EXISTS bwf_api;'
)

def drop_database():
    return DATABASE['drop']
    
def create_database():
    return DATABASE['create']
