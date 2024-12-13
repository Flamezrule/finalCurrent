from appl.gui import *
from appl.database import  DatabaseRef


import tkinter as tk

if __name__ == "__main__":
    database = DatabaseRef()
    dataCreate = database.initDatabase()
    app = restaurantApp(database)
    app.mainloop()