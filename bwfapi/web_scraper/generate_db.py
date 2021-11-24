from flask_mysqldb import MySQL

def set_db_login_credentials(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_DB'] = 'bwf_api'
    return MySQL(app)

def initialize_db(mysql):
    cur = mysql.connection.cursor()
    destroy_all_tables(cur)

    initialize_player(cur)
    initialize_level(cur)
    initialize_event(cur)
    initialize_tournament(cur)
    initialize_match(cur)
    
    cur.close()
    mysql.connection.commit()

def destroy_all_tables(cur):
    cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cur.execute("drop table if exists Player;")
    cur.execute("drop table if exists Level;")
    cur.execute("drop table if exists Event;")
    cur.execute("drop table if exists Tournament;")
    cur.execute("drop table if exists `Match`;")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

def initialize_player(cur):
    query = ('CREATE TABLE IF NOT EXISTS Player ('
            ' ID int NOT NULL AUTO_INCREMENT,'
            ' Name VARCHAR(150) NOT NULL,'
            ' Country VARCHAR(50),'
            ' PRIMARY KEY (ID)'
            ');')
    cur.execute(query)

def initialize_level(cur):
    query = ('CREATE TABLE IF NOT EXISTS Level ('
            ' ID int NOT NULL AUTO_INCREMENT,'
            ' Name VARCHAR(50) NOT NULL,'
            ' PRIMARY KEY (ID)'
            ');')
    cur.execute(query)

def initialize_event(cur):
    query = ('CREATE TABLE IF NOT EXISTS Event ('
            ' ID int NOT NULL AUTO_INCREMENT,'
            ' Name VARCHAR(10) NOT NULL,'
            ' PRIMARY KEY (ID)'
            ');')
    cur.execute(query)

def initialize_tournament(cur):
    query = ('CREATE TABLE IF NOT EXISTS Tournament ('
            ' ID int NOT NULL AUTO_INCREMENT,'
            ' LevelID int NOT NULL,'
            ' `Date` Date,'
            ' Name VARCHAR(10) NOT NULL,'
            ' PRIMARY KEY (ID),'
            ' FOREIGN KEY (LevelID) REFERENCES Level(ID)'
            ');')
    cur.execute(query)

def initialize_match(cur):
    query = ('CREATE TABLE IF NOT EXISTS `Match` ('
            ' ID int NOT NULL AUTO_INCREMENT,'
            ' WinnerID int NOT NULL,'
            ' LoserID int NOT NULL,'
            ' TournamentID int NOT NULL,'
            ' EventID int NOT NULL,'
            ' Time VARCHAR(50) NOT NULL,'
            ' Duration int NOT NULL,'
            ' Score VARCHAR(100) NOT NULL,'
            ' PRIMARY KEY (ID),'
            ' FOREIGN KEY (WinnerID) REFERENCES Player(ID),'
            ' FOREIGN KEY (LoserID) REFERENCES Player(ID),'
            ' FOREIGN KEY (TournamentID) REFERENCES Tournament(ID),'
            ' FOREIGN KEY (EventID) REFERENCES Event(ID)'
            ');')
    cur.execute(query)