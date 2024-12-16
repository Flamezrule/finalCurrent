import sqlite3
import os
from appl import gui


class DatabaseRef:
    def __init__(self, dbName='restaurantinfo.db'):
        if os.path.exists(dbName):
            os.remove(dbName)
            print(f"{dbName} has been deleted.")
        else:
            print(f"{dbName} does not exist.")
        self.dbName = dbName
        abs_path = os.path.abspath(self.dbName)
        print(f"Database is being created at: {abs_path}")
        self.conn = sqlite3.connect(dbName)
        self.initDatabase()

    def _connect(self):
        return sqlite3.connect(self.dbName)

    def enableForeignKeys(self):
        # Enable foreign key constraints in SQLite
        conn = self._connect()
        conn.execute("PRAGMA foreign_keys = 1")
        conn.close()

    def initDatabase(self):

        conn = self._connect()
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS tables (
                                table_ID INTEGER PRIMARY KEY,  --Unique table ID
                                max_Size INTEGER NOT NULL,     --Max number of seats at the table
                                is_Occupied INTEGER DEFAULT 0,  --Checks if a table has someone sitting there
                                current_Size INTEGER DEFAULT 0 --For reference
                )''')

        c.execute('''CREATE TABLE IF NOT EXISTS menu_items (
                                item_ID INTEGER PRIMARY KEY,
                                item_Name TEXT NOT NULL,
                                item_Price DOUBLE NOT NULL
                )''')

        c.execute('''CREATE TABLE IF NOT EXISTS reservations (
                                reservation_ID INTEGER PRIMARY KEY AUTOINCREMENT, --Tracks entered reservations
                                party_Name TEXT NOT NULL, --Entered Name
                                party_Size INTEGER NOT NULL, --Size of party
                                party_Time TEXT NOT NULL, --Entered Time, mostly flavor
                                is_Placed INTEGER DEFAULT 0 --Checks if placed
                        )''')

        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS orders ( 
                                order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                order_Name TEXT NOT NULL,
                                order_Size INTEGER NOT NULL,
                                order_Time TEXT NOT NULL,
                                order_Table INTEGER,
                                has_ordered INTEGER DEFAULT 0,
                                is_Complete INTEGER DEFAULT 0,
                                food_Cost DOUBLE DEFAULT 0.0,
                                order_Cost DOUBLE DEFAULT 0.0,
                                FOREIGN KEY(order_Table) REFERENCES tables(table_ID)
                        )''')

        c.execute('''CREATE TABLE IF NOT EXISTS order_choices (
                                customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                order_ID INTEGER,
                                item_ID INTEGER,
                                item_Cost DOUBLE,
                                FOREIGN KEY(order_ID) REFERENCES orders(order_ID),
                                FOREIGN KEY(item_ID) REFERENCES menu_items(item_ID),
                                FOREIGN KEY(item_Cost) REFERENCES menu_items(item_Cost)
                        )''')

        conn.commit()

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

        c.executemany('''
        INSERT OR IGNORE INTO menu_items (item_ID, item_Name, item_Price) VALUES (?, ?, ?)
        ''', [
            (1, "Burger", 11.99),
            (2, "Pasta", 8.99),
            (3, "Fish", 10.99),
            (4, "BLT", 14.99),
            (5, "Chicken", 12.99),
            (6, "Steak", 15.99),
            (7, "Taco", 7.99),
            (8, "Burrito", 9.99),
            (9, "Sausage", 8.99),
            (10, "Toast", 4.99)
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
        SELECT * FROM reservations WHERE is_Placed = 0
        ''')
        reservations = c.fetchall()
        conn.commit()
        conn.close()
        return reservations

    def getReservationById(self, reservation_id):
        conn = self._connect()
        c = conn.cursor()

        # Query to fetch reservation details by ID
        c.execute('''
        SELECT * FROM reservations WHERE reservation_ID = ?
        ''', (reservation_id,))
        reservation_data = c.fetchone()

        conn.close()
        conn.close()
        return reservation_data

    def getUnplacedTables(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''
        SELECT * FROM tables WHERE is_Occupied = 0''')
        tables = c.fetchall()
        conn.commit()
        conn.close()
        return tables

    def createOrder(self, orderName, orderSize, orderTime, tableID, reservationID):
        print(f"Checking reservation: {reservationID}")  # Check if reservationID is correct
        conn = self._connect()
        c = conn.cursor()

        c.execute('''
            SELECT reservation_ID FROM reservations WHERE reservation_ID = ?
            ''', (reservationID,))
        existing_reservation = c.fetchone()

        if existing_reservation is None:
            print(f"Reservation ID {reservationID} does not exist.")
            conn.close()
            return  # Exit if reservation doesn't exist

        print(f"Reservation ID {reservationID} found.")

        c.execute('''
        INSERT INTO orders (order_Name, order_Size, order_Time, order_Table)
        VALUES (?, ?, ?, ?)
        ''', (orderName, orderSize, orderTime, tableID))

        conn.commit()

        print(f"Reservation ID {reservationID} has been assigned to Table {tableID}.")  # Debugging statement
        conn.close()

    def updateReservationPlaced(self, reservationID):
        conn = self._connect()
        c = conn.cursor()

        c.execute('''
                UPDATE reservations
                SET is_Placed = 1
                WHERE reservation_ID = ?
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

    def getOrdersNotOrdered(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''SELECT * FROM orders WHERE has_Ordered = 0''')
        unordered_Orders = c.fetchall()
        conn.commit()
        conn.close()
        return unordered_Orders

    def getMenuItems(self):
        """Retrieve the available menu items."""
        conn = self._connect()
        c = conn.cursor()
        c.execute('SELECT * FROM menu_items')
        menu_items = c.fetchall()
        conn.close()
        return menu_items

    def getMenuItemByName(self, item_name):
        """Get a menu item by its name."""
        conn = self._connect()
        c = conn.cursor()
        c.execute('SELECT item_ID, item_Name, item_Price FROM menu_items WHERE item_Name = ?', (item_name,))
        item = c.fetchone()
        print(f"Item found: {item}")
        conn.close()
        return item

    def updateOrderCost(self, order_id, total_cost):
        """Update the total cost for the order."""
        conn = self._connect()
        c = conn.cursor()

        c.execute('''
        UPDATE orders
        SET order_Cost = ?
        WHERE order_ID = ?
        ''', (total_cost, order_id))

        conn.commit()
        conn.close()

    def addOrderItem(self, order_id, item_id, item_price):
        """Add a food item to the order."""
        conn = self._connect()
        c = conn.cursor()
        c.execute('''
               INSERT INTO order_choices (order_ID, item_ID, item_Cost)
               VALUES (?, ?, ?)
           ''', (order_id, item_id, item_price))
        conn.commit()
        conn.close()

    def updateOrderOrdered(self, order_id):
        """Mark the order as placed by setting is_Placed to 1."""
        conn = self._connect()
        c = conn.cursor()

        c.execute('''
        UPDATE orders
        SET has_Ordered = 1
        WHERE order_ID = ?
        ''', (order_id,))

        conn.commit()
        conn.close()

    def getUnpaidOrders(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''SELECT * FROM orders WHERE is_Complete = 0''')
        unpaid_Orders = c.fetchall()
        conn.commit()
        conn.close()
        return unpaid_Orders

    def completeOrder(self, orderID):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''
                UPDATE orders SET is_Complete = 1 WHERE order_ID = ?''', (orderID,))
        conn.commit()
        conn.close()

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

    def getOrderById(self, orderID):
        conn = self._connect()
        c = conn.cursor()

        # Query to fetch reservation details by ID
        c.execute('''
              SELECT * FROM orders WHERE order_ID = ?
              ''', (orderID,))
        order_data = c.fetchone()

        conn.close()
        conn.close()
        return order_data

    def getFullOrderById(self, orderID):
        conn = self._connect()
        c = conn.cursor()

        c.execute('''
            SELECT menu_items.item_Name, order_choices.item_Cost, orders.order_Name 
            FROM order_choices
            JOIN menu_items ON order_choices.item_ID = menu_items.item_ID
            JOIN orders ON order_choices.order_ID = orders.order_ID
            WHERE order_choices.order_ID = ?
            ''', (orderID,))

        order_items = c.fetchall()
        conn.close()
        return order_items
