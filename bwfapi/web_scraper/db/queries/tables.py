TABLES = {}
TABLES['player'] = (
    'CREATE TABLE IF NOT EXISTS `Player` ('
    ' ID VARCHAR(50) NOT NULL UNIQUE,'
    ' Name VARCHAR(150) NOT NULL,'
    ' Country VARCHAR(50),'
    ' PRIMARY KEY (ID)'
    ');')

TABLES['event'] = (
    'CREATE TABLE IF NOT EXISTS `Event` ('
    ' ID int NOT NULL AUTO_INCREMENT,'
    ' Name VARCHAR(10) NOT NULL,'
    ' PRIMARY KEY (ID)'
    ');')

TABLES['tournament'] = (
    'CREATE TABLE IF NOT EXISTS `Tournament` ('
    ' ID VARCHAR(50) NOT NULL,'
    ' `Date` Date,'
    ' Name VARCHAR(10) NOT NULL,'
    ' PRIMARY KEY (ID)'
    ');')

TABLES['match'] = (
    'CREATE TABLE IF NOT EXISTS `Match` ('
    ' ID int NOT NULL AUTO_INCREMENT,'
    ' WinnerID VARCHAR(50) NOT NULL,'
    ' LoserID VARCHAR(50) NOT NULL,'
    ' TournamentID VARCHAR(50) NOT NULL,'
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

TABLES['set'] = (
    'CREATE TABLE IF NOT EXISTS `Set` ('
    ' ID int NOT NULL AUTO_INCREMENT,'
    ' MatchID int NOT NULL,'
    ' WinnerScore int NOT NULL,'
    ' LoserScore int NOT NULL,'
    ' Round int NOT NULL,'
    ' PRIMARY KEY (ID),'
    ' FOREIGN KEY (MatchID) REFERENCES `Match`(ID)'
    ');')


def get_tables():
    return TABLES


RESETS = {}
RESETS['tables'] = [
    "SET FOREIGN_KEY_CHECKS = 0;",
    "drop table if exists Player;",
    "drop table if exists Level;",
    "drop table if exists Event;",
    "drop table if exists Tournament;",
    "drop table if exists `Match`;",
    "drop table if exists `Set`;",
    "SET FOREIGN_KEY_CHECKS = 1;",
]

def get_resets():
    return RESETS