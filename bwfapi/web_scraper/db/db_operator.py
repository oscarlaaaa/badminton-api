from decouple import config
import mysql.connector
from mysql.connector import errorcode
from queries.tables import get_tables
from queries.database import drop_database, create_database
from queries.insert import get_insert_queries

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
        self.TABLES = get_tables()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def drop_database(self):
        cursor = self.connection.cursor()
        cursor.execute(drop_database())
        cursor.close()

    def drop_tables(self):
        cursor = self.connection.cursor()
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("drop table if exists Player;")
        cursor.execute("drop table if exists Level;")
        cursor.execute("drop table if exists Event;")
        cursor.execute("drop table if exists Tournament;")
        cursor.execute("drop table if exists `Match`;")
        cursor.execute("drop table if exists `Set`;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        cursor.close()

    def create_database(self):
        cursor = self.connection.cursor()
        cursor.execute(create_database())
        cursor.close()

    def create_tables(self):
        cursor = self.connection.cursor()

        try:
            for table_name in self.TABLES:
                table_description = self.TABLES[table_name]
                cursor.execute(table_description)
            print("All tables completed!")

        except mysql.connector.Error as err:
            print("Failed creating table: {}".format(err))
            exit(1)

        cursor.close()
    
    def insert_players(self, player_list):
        cursor = self.connection.cursor()
        query = self.INSERTS['player']

        try:
            for player in player_list:
                player_data = (player['name'], player['country'])
                cursor.execute(query, player_data)
        except mysql.connector.Error as err:
            print("Error inserting player: {}".format(err))
            exit(1)

        print("All players inserted!")
        cursor.close()
   
if __name__ == "__main__":

    player_list = [{'name': 'oscar', 'country': 'canada'},
        {'name': 'raymond', 'country': 'hong kong'}
    ]

    operator = DBOperator()
    # operator.drop_database()
    # operator.create_database()
    # operator.drop_tables()
    # operator.create_tables()
    operator.insert_players(player_list)
    operator.close()