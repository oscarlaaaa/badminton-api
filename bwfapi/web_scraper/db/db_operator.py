from decouple import config
import mysql.connector
from mysql.connector import errorcode
from queries.tables import get_tables, get_resets
from queries.database import drop_database, create_database
from queries.insert import get_insert_queries, get_default_queries

class DBOperator:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user=config('MYSQL_USER'),
                                                    host=config('MYSQL_HOST'),
                                                    database=config('MYSQL_DB'))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        
        self.INSERTS = get_insert_queries()
        self.DEFAULTS = get_default_queries()
        self.TABLES = get_tables()
        self.RESETS = get_resets()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def drop_database(self):
        cursor = self.connection.cursor()
        query = drop_database()
        try:
            cursor.execute(query)
            print("Database dropped!")
        except mysql.connector.Error as err:
            print("Failed dropping database: {}".format(err))
            exit(1)
        cursor.close()

    def drop_tables(self):
        cursor = self.connection.cursor()
        queries = self.RESETS['tables']

        cursor.execute(f"USE {config('MYSQL_DB')}")
        for query in queries:
            try:
                cursor.execute(query)
                print("Tables dropped!")
            except mysql.connector.Error as err:
                print("Failed dropping tables: {}".format(err))
                exit(1)
        cursor.close()

    def create_database(self):
        cursor = self.connection.cursor()    
        query = create_database()    
        try:
            cursor.execute(query)
            print("Database created!")
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cursor.close()

    def create_tables(self):
        cursor = self.connection.cursor()
        for table_name, query in self.TABLES.items():
            try:
                cursor.execute(query)
                print(f"Table {table_name} completed!")
                
            except mysql.connector.Error as err:
                print("Failed creating table: {}".format(err))
                exit(1)
        print("All tables created!")
        cursor.close()
    
    def insert_players(self, player_list):
        cursor = self.connection.cursor()
        query = self.INSERTS['player']

        for name, idnum in player_list.items():
            try:
                player_data = (idnum, name)
                cursor.execute(query, player_data)
                print(f"{name} inserted with id {idnum}!")
            except mysql.connector.Error as err:
                print("Error inserting player: {}".format(err))
                

        print("All players inserted!")
        cursor.close()
   
    def insert_events(self):
        cursor = self.connection.cursor()
        queries = self.DEFAULTS['event']
        for q in queries:
            try:
                cursor.execute(q)
                print("All events inserted!")
            except mysql.connector.Error as err:
                print("Error inserting events: {}".format(err))
                exit(1)
        
        cursor.close()

if __name__ == "__main__":

    player_list = {'oscar': 'asdf', 'ray': 'asdf'}
    

    operator = DBOperator()
    operator.drop_database()
    operator.create_database()
    operator.drop_tables()
    operator.create_tables()
    operator.insert_players(player_list)
    operator.close()