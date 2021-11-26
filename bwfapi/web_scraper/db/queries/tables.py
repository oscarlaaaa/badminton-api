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
    ' ID int NOT NULL AUTO_INCREMENT,'
    ' `Date` Date,'
    ' Name VARCHAR(10) NOT NULL,'
    ' PRIMARY KEY (ID),'
    ' FOREIGN KEY (LevelID) REFERENCES Level(ID)'
    ');')

TABLES['match'] = (
    'CREATE TABLE IF NOT EXISTS `Match` ('
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


