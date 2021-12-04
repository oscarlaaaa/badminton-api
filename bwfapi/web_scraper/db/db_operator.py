from decouple import config
import mysql.connector
from mysql.connector import errorcode
from queries.tables import get_tables, get_resets
from queries.database import drop_database, create_database
from queries.insert import get_insert_queries, get_default_queries
from queries.select import query_player_id_by_name

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
        except mysql.connector.Error as err:
            print(f"Failed dropping database: {err}")
            exit(1)

        print("Database dropped!")
        cursor.close()

    def drop_tables(self):
        cursor = self.connection.cursor()
        queries = self.RESETS['tables']

        cursor.execute(f"USE {config('MYSQL_DB')}")
        for query in queries:
            try:
                cursor.execute(query)
            except mysql.connector.Error as err:
                print(f"Failed dropping tables: {err}")
                exit(1)

        print("Tables dropped!")
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
                print(f"Error inserting player: {err}")

        cursor.close()

    def insert_events(self):
        cursor = self.connection.cursor()
        queries = self.DEFAULTS['event']
        for q in queries:
            try:
                cursor.execute(q)
                print("Event inserted!")
            except mysql.connector.Error as err:
                print(f"Error inserting events: {err}")
                exit(1)

        cursor.close()

    def insert_tournaments(self, tournament_list):
        cursor = self.connection.cursor()
        query = self.INSERTS['tournament']

        for tournament in tournament_list:
            try:
                tournament_data = (
                    tournament['link'], tournament['start'], tournament['end'], tournament['name'])
                cursor.execute(query, tournament_data)
                print(f"Tournament {tournament['name']} inserted!")
            except mysql.connector.Error as err:
                print(f"Error inserting tournament: {err}")
                exit(1)

        print("Finished inserting tournaments!")
        cursor.close()
    
    def search_player_by_name(self, player_name):
        cursor = self.connection.cursor()
        query = query_player_id_by_name(player_name)
        player_id = "Failed query"

        try:
            cursor.execute(query)
            player_id = cursor.fetchone()
            print(f"Player {player_name} queried for ID!")
        except mysql.connector.Error as err:
            print(f"Error querying player: {err}")
        
        cursor.close()
        return player_id




# Tests for DB Operations
if __name__ == "__main__":

    player_list = {'Oscar La': 'asdf', 'Raymond Wong': 'asdfghjkl'}

    tournament_list = [{'name': 'PROTON MALAYSIA OPEN SUPER SERIES 2008', 'start': '2008-1-15', 'end': '2008-1-20', 'link': 'DB1CB027-CC31-4B3A-99E5-9C1D55A18208'},
                       {'name': 'YONEX KOREA SUPER SERIES 2008', 'start': '2008-1-22',
                           'end': '2008-1-27', 'link': 'B15BB4E0-1447-42F7-9150-E217DD9FD0A4'},
                       {'name': "2008 Oceania Teams Event 'Robson Shield'", 'start': '2008-2-3',
                           'end': '2008-2-4', 'link': '63456522-CD1A-49E8-8C2C-8D4CC1F6E61F'},
                       {'name': 'Oceania Championships 2008', 'start': '2008-2-5',
                        'end': '2008-2-7', 'link': '94646034-3486-42AD-8D5B-5CE3FB08D3D2'},
                       {'name': 'Oceania Individual Championships 2008', 'start': '2008-2-5',
                        'end': '2008-2-9', 'link': 'CC31FCF8-9F81-4067-BBB3-B3D89D2A8452'},
                       {'name': "European Men's & Women's Team Championships 2008", 'start': '2008-2-12',
                        'end': '2008-2-17', 'link': '8AAFD55F-0CF2-417A-A765-73D3D86667EC'},
                       {'name': 'Thomas & Uber Cups Preliminaries Asia Zone 2008', 'start': '2008-2-19',
                        'end': '2008-2-24', 'link': '0B0B25A2-1963-46F2-B6FD-7A71FE1E0F79'},
                       {'name': 'Yonex All England Open Super Series 2008', 'start': '2008-3-4',
                        'end': '2008-3-9', 'link': '53FCA2F0-C6F5-4D0F-8F9B-2799C9A44784'},
                       {'name': 'WILSON SWISS SUPER SERIES 2008', 'start': '2008-3-11',
                        'end': '2008-3-16', 'link': '3E9A655F-C9C2-41BE-B47D-48B7196662AB'},
                       {'name': 'European Mixed Team Championships 2008', 'start': '2008-4-12',
                        'end': '2008-4-15', 'link': '118338FF-D037-4186-85DC-78BA708BCB63'},
                       {'name': 'Yonex-Sunrise Badminton Asia Championships 2008', 'start': '2008-4-15',
                        'end': '2008-4-20', 'link': '6359DD71-4109-4AA5-9AD9-B72BE53E20C0'},
                       {'name': 'European Championships 2008', 'start': '2008-4-16',
                        'end': '2008-4-20', 'link': 'FF96EE38-116D-43C5-9836-65253BCA48CB'},
                       {'name': 'WUBC - World University Badminton Championship 2008', 'start': '2008-5-8',
                        'end': '2008-5-10', 'link': 'E1493EDA-2E88-474B-800E-F78F5A5D4557'},
                       {'name': 'AVIVA SINGAPORE SUPER SERIES 2008', 'start': '2008-6-10',
                        'end': '2008-6-15', 'link': 'FB58F063-9DA8-46B8-8249-4B7DE6F6A791'},
                       {'name': 'DJARUM INDONESIA SUPER SERIES 2008', 'start': '2008-6-17',
                        'end': '2008-6-22', 'link': '7DD8D97A-23EA-42DE-A1FE-0BD6A6C30369'},
                       {'name': 'SCG THAILAND GRAND PRIX GOLD 2008', 'start': '2008-6-24',
                        'end': '2008-6-29', 'link': 'B49F1276-D220-4CD8-BE2B-F54C8964F916'},
                       {'name': '2008 Yonex OCBC US Open Grand Prix', 'start': '2008-7-8',
                        'end': '2008-7-12', 'link': '7238B61B-295A-475E-B4BA-C8504E3D1CEE'},
                       {'name': '2008 KLRC Australian International & Australian Junior International',
                        'start': '2008-7-24', 'end': '2008-7-27', 'link': '6E61CDB5-0321-48E6-BA8E-44B006C8DEFF'},
                       {'name': 'Chinese Taipei Grand Prix Gold 2008', 'start': '2008-9-9',
                        'end': '2008-9-14', 'link': 'AF08DFAC-B741-4DB2-88E6-1A131DF8A207'},
                       {'name': 'Yonex Japan Super Series 2008', 'start': '2008-9-16',
                        'end': '2008-9-21', 'link': 'F6BCB9E0-00AA-43BF-9184-8FD217E9FA17'},
                       {'name': 'CHINA MASTERS SUPER SERIES 2008', 'start': '2008-9-23',
                        'end': '2008-9-28', 'link': 'DCB4AAB3-505B-4A85-8561-FB1DF531A4DE'},
                       {'name': 'Bitburger Open 2008', 'start': '2008-9-30',
                        'end': '2008-10-5', 'link': '0987CA38-932F-457C-9637-511F470B8240'},
                       {'name': 'MACAU GRAND PRIX GOLD 2008', 'start': '2008-9-30',
                        'end': '2008-10-5', 'link': '148CA517-9DAB-4E04-A76D-F2F262E80EE2'},
                       {'name': 'XIV Pan Am Championships 2008', 'start': '2008-10-1',
                        'end': '2008-10-2', 'link': '50D9DBC4-4F5C-4485-8AB7-9E385B93E87A'},
                       {'name': 'XIV Pan Am Championships Individual Events 2008', 'start': '2008-10-3',
                        'end': '2008-10-5', 'link': '88150F04-2B0B-4983-AEE7-F18AD7ED308C'},
                       {'name': 'KLRC BULGARIAN GRAND PRIX 2008', 'start': '2008-10-7',
                        'end': '2008-10-12', 'link': '5784990F-D666-4E58-B538-CE50667541BB'},
                       {'name': 'Yonex Dutch Open 2008', 'start': '2008-10-14',
                        'end': '2008-10-19', 'link': '9B75EE6A-AF3D-454F-A7FA-E12019D30943'},
                       {'name': 'Denmark Open Super Series 2008', 'start': '2008-10-21',
                        'end': '2008-10-26', 'link': 'FF81151B-1F7F-4F01-8786-0AA238D0746E'},
                       {'name': 'FRENCH SUPER SERIES 2008', 'start': '2008-10-28',
                        'end': '2008-11-2', 'link': 'A6F9CFAE-7534-4B54-9FF7-F9A59738843C'},
                       {'name': 'RUSSIAN GRAND PRIX 2008', 'start': '2008-11-4',
                        'end': '2008-11-9', 'link': '0C7023F1-3188-42BD-AAA5-9AC0C7EBC9A1'},
                       {'name': '2008 KLRC New Zealand Open', 'start': '2008-11-11',
                        'end': '2008-11-15', 'link': '63DAA64B-0E16-4D74-A2A7-A71C803BF46C'},
                       {'name': 'LI NING CHINA OPEN SUPER SERIES 08', 'start': '2008-11-18',
                        'end': '2008-11-23', 'link': '5A908D09-C452-42EC-943B-1429C859B483'},
                       {'name': 'YONEX SUNRISE HONG KONG SUPER SERIES 2008', 'start': '2008-11-24',
                        'end': '2008-11-30', 'link': '5C4B3017-19B3-49E0-937F-5E1B32F9687F'},
                       {'name': 'Vietnam GP 2008', 'start': '2008-12-2', 'end': '2008-12-7',
                        'link': 'EB7C0698-52B7-4AF8-9F06-D9FE9C18E0D0'},
                       {'name': 'World Super Series Masters Finals 2008', 'start': '2008-12-18', 'end': '2008-12-21', 'link': 'BF4ABA67-593E-496C-A81D-879B85E23D37'}]

    operator = DBOperator()
    operator.drop_database()  # works
    operator.create_database()  # works
    operator.drop_tables()  # works
    operator.create_tables()  # works

    operator.insert_events() #works

    operator.insert_players(player_list) #works

    # operator.insert_tournaments(tournament_list) #works

    xd = operator.search_player_by_name("Oscar La")
    print(str(xd))

    operator.close()
