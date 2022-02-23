# Copyright © 2022 Oscar La
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this 
# software and associated documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to the following 
# conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies 
# or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

from decouple import config
import mysql.connector
from mysql.connector import errorcode
from bwfapi.web_scraper.db.queries.tables import get_tables, get_resets
from bwfapi.web_scraper.db.queries.database import drop_database, create_database
from bwfapi.web_scraper.db.queries.insert import get_insert_queries
from bwfapi.web_scraper.db.queries.select import query_player_id_by_name


class DBOperator:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user=config('MYSQL_USER'),
                                                      host=config('MYSQL_HOST'), 
                                                      password=config('MYSQL_PASS'),
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
        self.RESETS = get_resets()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def drop_database(self):
        cursor = self.connection.cursor()
        query = drop_database()
        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            print(f"Failed dropping database: {err}")
            exit(1)

        print("Database dropped!")
        self.connection.commit()
        cursor.close()

    def drop_tables(self):
        cursor = self.connection.cursor()
        queries = self.RESETS['tables']

        for query in queries:
            try:
                cursor.execute(query)
            except mysql.connector.Error as err:
                print(f"Failed dropping tables: {err}")
                exit(1)

        print("Tables dropped!")
        self.connection.commit()
        cursor.close()

    def create_database(self):
        cursor = self.connection.cursor()
        query = create_database()
        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

        print("Database created!")
        cursor.execute(f"USE {config('MYSQL_DB')}")
        self.connection.commit()
        cursor.close()

    def create_tables(self):
        cursor = self.connection.cursor()
        for table_name, query in self.TABLES.items():
            try:
                cursor.execute(query)
                print(f"Table {table_name} completed!")
            except mysql.connector.Error as err:
                print(f"Failed creating table: {err}")
                exit(1)

        print("All tables created!")
        self.connection.commit()
        cursor.close()

    def reset_database(self):
        self.drop_database()
        self.create_database()
        self.create_tables()

    def insert_players(self, player_list):
        cursor = self.connection.cursor()
        query = self.INSERTS['player']
        for name in player_list:
            details = player_list[name]
            try:
                player_data = (
                    details['id'], name, details['event'], details['country'], details['date of birth'], details['play r or l'], details['height'])
                cursor.execute(query, player_data)
            except mysql.connector.Error as err:
                print(f"Error inserting player: {err}")

        print("Finished inserting players!")
        self.connection.commit()
        cursor.close()

    def insert_tournaments(self, tournament_list):
        cursor = self.connection.cursor()
        query = self.INSERTS['tournament']

        for tournament in tournament_list:
            try:
                tournament_data = (
                    tournament['link'], tournament['start'], tournament['end'], tournament['name'])
                cursor.execute(query, tournament_data)
            except mysql.connector.Error as err:
                print(f"Error inserting tournament: {err}")

        print("Finished inserting tournaments!")
        self.connection.commit()
        cursor.close()

    def search_player_by_name(self, player_name):
        cursor = self.connection.cursor()
        query = query_player_id_by_name(player_name)
        player_id = "Failed query"

        try:
            cursor.execute(query)
            player_id = cursor.fetchone()
            print(f"Player {player_name} queried for ID {player_id}!")
        except mysql.connector.Error as err:
            print(f"Error querying player: {err}")

        cursor.close()
        return player_id

    def insert_match_and_sets(self, match_list):
        cursor = self.connection.cursor()
        for match in match_list:
            sets = match.get_sets()
            match_query = self.INSERTS['match']
            set_query = self.INSERTS['set']

            try:
                cursor.execute(match_query, match.get_formatted_data())
                for match_set in sets:
                    cursor.execute(
                        set_query, match_set.get_formatted_data())

            except mysql.connector.Error as err:
                print(f"Error inserting match: {err}")

        print("Finished inserting matches and sets!")
        self.connection.commit()
        cursor.close()
