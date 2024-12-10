import sqlite3
from appl import gui

class DatabaseRef:
    def __init__(self, dbName='restaurant.db'):
        self.dbName = dbName
        self.create_database()
        #self.cursor = self.connection.cursor()

    def _connect(self):
        return sqlite3.connect(self.dbName)

    def initDatabase(self):
        conn = self._connect()
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS tables (
                                table_ID INTEGER PRIMARY KEY,  --Unique table ID
                                max_Size INTEGER NOT NULL,     --Max number of seats at the table
                                is_Occupied INTEGER DEFAULT 0  --0 means not occupied, 1 means occupied
                                current_Size INTEGER DEFAULT 0 --For reference
                )''')

        c.execute('''CREATE TABLE IF NOT EXISTS reservations (
                                reservation_ID INTEGER PRIMARY KEY AUTOINCREMENT, --Tracks entered reservations
                                party_Name TEXT NOT NULL, --Entered Name
                                party_Size INTEGER NOT NULL, --Size of party
                                party_Time TEXT NOT NULL, --Entered Time, mostly flavor
                                is_Placed INTERGER DEFAULT 0 --0
                        )''')

        c.executemany('''
        INSERT OR IGNORE INTO tables (table_ID, max_Size) VALUES (?, ?)
        ''', [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 4),
            (6, 4),
            (7, 4),
            (8, 4),
            (9, 4),
            (10, 6),
            (11, 6),
            (12, 8),
            (13, 8),
            (14, 10),
            (15, 10)
        ])

        conn.commit()
        conn.close()

    def addReservationData(self, partyName, partySize, partyTime):
        conn = self._connect()
        c = conn.cursor()

        c.execute('''
        INSERT INTO reservations (party_Name, party_Size, party_Time) VALUES (?, ?, ?)
        ''', (partyName, partySize, partyTime))

        conn.commit()
        conn.close()