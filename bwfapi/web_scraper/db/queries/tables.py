TABLES = {}
TABLES['player'] = (
    'CREATE TABLE IF NOT EXISTS `Player` ('
    ' ID VARCHAR(50) NOT NULL UNIQUE,'
    ' Name VARCHAR(150) NOT NULL,'
    ' `Event` VARCHAR(5) NOT NULL,'
    ' Country VARCHAR(50),'
    ' BirthDate Date,'
    ' PlayHand VARCHAR(20),'
    ' Height int,'
    ' PRIMARY KEY (ID)'
    ');')

TABLES['tournament'] = (
    'CREATE TABLE IF NOT EXISTS `Tournament` ('
    ' ID VARCHAR(50) NOT NULL,'
    ' `StartDate` Date,'
    ' `EndDate` Date,'
    ' Name VARCHAR(100) NOT NULL,'
    ' PRIMARY KEY (ID)'
    ');')

TABLES['match'] = (
    'CREATE TABLE IF NOT EXISTS `Match` ('
    ' WinnerID VARCHAR(100) NOT NULL,'
    ' LoserID VARCHAR(100) NOT NULL,'
    ' TournamentID VARCHAR(100) NOT NULL,'
    ' `Duration` int NOT NULL,'
    ' PRIMARY KEY (WinnerID, LoserID, TournamentID),'
    ' FOREIGN KEY (WinnerID) REFERENCES Player(ID),'
    ' FOREIGN KEY (LoserID) REFERENCES Player(ID),'
    ' FOREIGN KEY (TournamentID) REFERENCES Tournament(ID)'
    ');')

TABLES['set'] = (
    'CREATE TABLE IF NOT EXISTS `Set` ('
    ' Round int NOT NULL,'
    ' WinnerID VARCHAR(100) NOT NULL,'
    ' LoserID VARCHAR(100) NOT NULL,'
    ' TournamentID VARCHAR(100) NOT NULL,'
    ' WinnerScore int NOT NULL,'
    ' LoserScore int NOT NULL,'
    ' PRIMARY KEY (Round, WinnerID, LoserID, TournamentID),'
    ' FOREIGN KEY (WinnerID) REFERENCES `Match`(WinnerID),'
    ' FOREIGN KEY (LoserID) REFERENCES `Match`(LoserID),'
    ' FOREIGN KEY (TournamentID) REFERENCES `Match`(TournamentID)'
    ');')


def get_tables():
    return TABLES


RESETS = {}
RESETS['tables'] = [
    "SET FOREIGN_KEY_CHECKS = 0;",
    "drop table if exists Player;",
    "drop table if exists Level;",
    "drop table if exists Tournament;",
    "drop table if exists `Match`;",
    "drop table if exists `Set`;",
    "SET FOREIGN_KEY_CHECKS = 1;",
]

def get_resets():
    return RESETS