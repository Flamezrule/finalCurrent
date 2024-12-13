import sqlite3
import os
from appl import gui


class DatabaseRef:
    def __init__(self, dbName='restaurant.db'):
        self.dbName = dbName
        self.dbPath = os.path.join(os.path.dirname(__file__), 'data', self.dbName)
        self.initDatabase()

    def _connect(self):
        return sqlite3.connect(self.dbName)

    def initDatabase(self):
        os.makedirs(os.path.dirname(self.dbPath), exist_ok=True)

        conn = self._connect()
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS tables (
                                table_ID INTEGER PRIMARY KEY,  --Unique table ID
                                max_Size INTEGER NOT NULL,     --Max number of seats at the table
                                is_Occupied INTEGER DEFAULT 0,  --Checks if a table has someone sitting there
                                current_Size INTEGER DEFAULT 0 --For reference
                )''')

        c.execute('''CREATE TABLE IF NOT EXISTS reservations (
                                reservation_ID INTEGER PRIMARY KEY AUTOINCREMENT, --Tracks entered reservations
                                party_Name TEXT NOT NULL, --Entered Name
                                party_Size INTEGER NOT NULL, --Size of party
                                party_Time TEXT NOT NULL --Entered Time, mostly flavor
                        )''')

        c.execute('''CREATE TABLE IF NOT EXISTS orders (
                                order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                order_Name TEXT NOT NULL,
                                order_Size INTEGER NOT NULL,
                                order_Time TEXT NOT NULL,
                                order_Table INTEGER NOT NULL,
                                has_ordered INTEGER DEFAULT 0,
                                is_Complete INTEGER DEFAULT 0,
                                food_Cost DOUBLE DEFAULT 0.0,
                                order_Cost DOUBLE DEFAULT 0.0
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

    def clearDatabase(self):
        conn = self._connect()
        c = conn.cursor()

        c.execute('''DELETE FROM reservations''')
        c.execute('''DELETE FROM tables''')
        c.execute('''DELETE FROM orders''')

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

    def getUnplacedReservations(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''
        SELECT * FROM reservations
        ''')
        reservations = c.fetchall()
        conn.commit()
        conn.close()
        return reservations

    def getReservationIDFromIndex(self, reservation_index):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''SELECT * FROM reservations WHERE reservation_ID = ?''', (reservation_index,))
        reservation = c.fetchone()
        conn.commit()
        conn.close()

        return reservation

    def getUnplacedTables(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''
        SELECT * FROM tables''')
        tables = c.fetchall()
        conn.commit()
        conn.close()
        return tables

    def createOrder(self, orderName, orderSize, orderTime, tableID, reservationID):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''
        INSERT INTO orders (order_Name, order_Size, order_Time, order_Table)
        VALUES (?, ?, ?, ?)
        ''', (orderName, orderSize, orderTime, tableID))

        c.execute('''
        DELETE FROM reservations WHERE reservation_ID = ?
        ''', (reservationID,))

        conn.commit()
        conn.close()

    def updateTableOccupied(self, tableID):
        conn = self._connect()
        c = conn.cursor()

        c.execute('''
                UPDATE tables
                SET is_Occupied = 1
                WHERE table_ID = ?
                ''', (tableID,))

        conn.commit()
        conn.close()

    def updateTableEmpty(self, tableID):
        conn = self._connect()
        c = conn.cursor()

        c.execute('''
                UPDATE tables
                SET is_Occupied = 0
                WHERE table_ID = ?
                ''', (tableID,))

        conn.commit()
        conn.close()

    def processOrder(self):
        pass

    def getOrderHistory(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''
        SELECT * FROM orders
        ''')
        orders = c.fetchall()
        conn.commit()
        conn.close()
        return orders