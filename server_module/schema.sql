CREATE TABLE IF NOT EXISTS players (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
    Login TEXT NOT NULL UNIQUE ,
    Password BLOB NOT NULL ,
    Wins INTEGER DEFAULT 0
);

