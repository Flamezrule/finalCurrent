import tkinter as tk
from tkinter import messagebox
import sqlite3



class restaurantApp(tk.Tk):
    def __init__(self, database):
        super().__init__()

        self.database = database
        #Reservation and Order Total and Current Count for Later Testing
        self.totalReservationCount = 0
        self.currentReservationCount = 0
        self.totalOrderCount = 0
        self.currentOrderCount = 0

        self.title("Restaurant Management System")
        self.geometry("800x800")

        self.mainMenuFrame = mainMenu(self, self.database, self)
        self.mainMenuFrame.pack()

    def showFrame(self, frameClass, database=None, app=None):
        for widget in self.winfo_children():
            widget.pack_forget()

        if database is None:
            database = self.database
        #if app is None:
            #app = self.app
        print(database)
        print(app)
        frameClass(self, self.database, app).pack()

class mainMenu(tk.Frame):
    def __init__(self, master, database, app):
        super().__init__(master)
        self.database = database
        self.app = app

        self.welcomeLabel = tk.Label(self, text="Welcome to Early", font=("Arial", 16, "bold"))
        self.welcomeLabel.pack(pady=20)

        self.addReservationsButton = tk.Button(self, text="Add Reservations", command=self.addReservations)
        self.addReservationsButton.pack(pady=10)

        self.processReservationsButton = tk.Button(self, text="Process Reservations", command=self.processReservations)
        self.processReservationsButton.pack(pady=10)

        self.enterOrdersButton = tk.Button(self, text="Enter Orders", command=self.enterOrders)
        self.enterOrdersButton.pack(pady=10)

        self.completeOrdersButton = tk.Button(self, text="Complete Orders", command=self.completeOrders)
        self.completeOrdersButton.pack(pady=10)

        self.viewOrderHistoryButton = tk.Button(self, text="View Order History", command=self.viewOrderHistory)
        self.viewOrderHistoryButton.pack(pady=10)

        self.closeRestaurantButton = tk.Button(self, text="Close Restaurant", command=self.closeRestaurant)
        self.closeRestaurantButton.pack(pady=10)

        self.resTotalLabel = tk.Label(self, text=f"Total Reservations: {self.app.totalReservationCount}")
        self.resTotalLabel.pack()

        self.resCurrentLabel = tk.Label(self, text=f"Current Reservations: {self.app.currentReservationCount}")
        self.resCurrentLabel.pack()

        self.ordTotalLabel = tk.Label(self, text=f"Total Orders: {self.app.totalOrderCount}")
        self.ordTotalLabel.pack()

        self.ordCurrentLabel = tk.Label(self, text=f"Current Orders: {self.app.currentOrderCount}")
        self.ordCurrentLabel.pack()


#Moves to the menu for making a new reservation. Does not need logic check as should always be possible
    def addReservations(self):
        self.master.showFrame(addReservationFrame, self.database, self.app)

#Simple Logic check, checks if a reservation has been made or if any exist
    def processReservations(self):
        if self.app.totalReservationCount == 0:
            messagebox.showwarning("Logic Error", "No Reservations have been made, create a reservation to begin")
            return
        elif self.app.currentReservationCount == 0:
            messagebox.showwarning("Logic Error", "There are no Reservations that need to be fulfilled")
            return
        elif self.app.currentReservationCount >= 1:
            self.master.showFrame(processReservationFrame, self.database, self.app)
        else:
            messagebox.showwarning("Impossible", "No way to get this")

    def enterOrders(self):
        self.master.showFrame(enterOrdersFrame, self.database, self.app)

    def completeOrders(self):
        self.master.showFrame(completeOrdersFrame, self.database, self.app)

    def viewOrderHistory(self):
        self.master.showFrame(viewOrderHistoryFrame, self.database, self.app)

    def closeRestaurant(self):
        #Show a messsage box that tells the user goodbye, clears all data in restaurant.db, then exits the program
        result = messagebox.askyesno("Close Restaurant", "Are you sure you want to close the restaurant?")

        if result: #If yes is picked
            self.database.clearDatabase()
            messagebox.showinfo("Goodbye", "Later Skater")
            self.quit()
        else:
            return

class addReservationFrame(tk.Frame):
    def __init__(self, master, database, app):
        super().__init__(master)
        self.database = database
        self.master = master
        self.app = app

#This information should be sent to database.py, but will be kept local for building
        self.addReservationInstructions = tk.Label(self, text="Please Enter Your Reservation Information", font=("Arial", 16))
        self.addReservationInstructions.pack(pady=20)

        self.nameLabel = tk.Label(self, text="Please Enter a Name for the Reservation")
        self.nameLabel.pack(pady=5)

        self.nameEntry = tk.Entry(self)
        self.nameEntry.pack(pady=5)

        self.partyLabel = tk.Label(self, text="Please Choose a Party Size: ")
        self.partyLabel.pack(pady=5)
        self.partySizeOptions = list(range(1, 11))
        self.partySizeEntry = tk.IntVar()
        self.partySizeEntry.set(self.partySizeOptions[0])
        self.partySizeMenu = tk.OptionMenu(self, self.partySizeEntry,*self.partySizeOptions)
        self.partySizeMenu.pack(pady=5)

        self.partyTime = tk.Label(self, text="Please enter a time for your reservation in the form of XX:XX (A/P)M")
        self.partyTime.pack(pady=5)
        self.timeEntry = tk.Entry(self)
        self.timeEntry.pack(pady=5)

        self.submitReservation = tk.Button(self, text="Submit", command=self.confirmReservation, fg='white', bg='green')
        self.submitReservation.pack(pady=5)

        self.cancelReservationButton = tk.Button(self, text="Cancel", command=self.cancelReservation, fg='white', bg='red')
        self.cancelReservationButton.pack(pady=5)

    def confirmReservation(self):
        partyName = self.nameEntry.get()
        partyTime = self.timeEntry.get()
        partySize = self.partySizeEntry.get()

        if not partyName:
            messagebox.showwarning("Input error", "Please Enter a name for the reservation")
            return

        if not partyTime:
            messagebox.showwarning("Input error", "Please Enter a time for the reservation")
            return

        self.database.addReservationData(partyName, partySize, partyTime)

        self.app.totalReservationCount += 1
        self.app.currentReservationCount += 1

        messagebox.showinfo("Reservation Confirmed", f"Reservation under {partyName} confirmed for {partyTime}.")

        self.master.showFrame(mainMenu, self.database, self.app)

    def cancelReservation(self):
        self.master.showFrame(mainMenu, self.database, self.app)

class processReservationFrame(tk.Frame):
    def __init__(self, master, database, app):
        super().__init__(master)
        self.database = database
        self.master = master
        self.app = app

        self.reservationProcessInstructions = tk.Label(self, text="Process Reservations Menu")
        self.reservationProcessInstructions.pack(pady=20)

        self.reservationListLabel = tk.Label(self, text=f"Current Reservations: {self.app.currentReservationCount}")
        self.reservationListLabel.pack(pady=10)

        self.reservationNotSeated = tk.Listbox(self, width=60, height=10)
        self.reservationNotSeated.pack()

        self.reservationCheckButton = tk.Button(self, text="Process this Reservation", command=self.checkReservationData)
        self.reservationCheckButton.pack()

        self.tableListLabel = tk.Label(self, text="Available Tables: ")
        self.tableListLabel.pack()

        self.tableListBox = tk.Listbox(self, width=60, height=10)
        self.tableListBox.pack()

        self.createOrderButton = tk.Button(self, text="Assign to selected table", command=self.reservationIntoOrder)
        self.createOrderButton.pack()

        self.loadReservationData()

        self.reservationProcessCancel = tk.Button(self, text="Cancel", command=self.cancelReservationProcess, fg='white', bg='red')
        self.reservationProcessCancel.pack(pady=5)

    def loadReservationData(self):
        self.reservationNotSeated.delete(0, tk.END)  # Clear previous data
        if self.database:
            unplacedReservations = self.database.getUnplacedReservations()
            for reservation in unplacedReservations:

                print(f"Checking reservation: {reservation[0]}")  # Debugging
                display_text = f"{reservation[1]} (Party Size: {reservation[2]}, Time: {reservation[3]})"
                self.reservationNotSeated.insert(tk.END, display_text)
        else:
            print("Error: Database for reservations not initialized")

    def checkReservationData(self):
        selected_reservation = self.reservationNotSeated.curselection()
        if not selected_reservation:
            messagebox.showwarning("Input Error", "Please select a reservation")
            return

        reservation_index = selected_reservation[0]
        selected_reservation_data = self.reservationNotSeated.get(reservation_index)
        self.selected_reservation_data = selected_reservation_data
        self.reservation_index = reservation_index
        party_size = int(selected_reservation_data.split("Party Size: ")[1].split(",")[0])
        self.loadTableData(party_size)


    def loadTableData(self, party_size=None):
        self.tableListBox.delete(0, tk.END)
        if self.database:
            availableTables = self.database.getUnplacedTables()
            for table in availableTables:
                table_id = table[0]
                table_size = table[1]

                if party_size is None or table_size >= party_size:
                    display_text = f"Table {table_id} (Seats: {table_size}) - Available"
                    self.tableListBox.insert(tk.END, display_text)
                elif table_size < party_size:
                    pass
                else:
                    messagebox.showinfo("No Available Tables", "There are no open tables that can accomidate this "
                                                           "reservation, Process and Complete orders to place this")
        else:
            print("Database for Tables not Initialized")

    def reservationIntoOrder(self):
        if not hasattr(self, 'selected_reservation_data'):
            messagebox.showwarning("Input Error", "Please select a reservation")
            return
        selected_reservation_data = self.selected_reservation_data
        reservation_index = self.reservation_index

        try:
            party_name, details = selected_reservation_data.split(" (")
            party_name = party_name.strip()  # Remove any leading/trailing whitespace

            # Step 2: Split the details by commas to extract Party Size and Time
            details = details.strip(")")  # Remove the closing parenthesis
            party_size_str, party_time_str = details.split(", ")

            # Step 3: Extract party size and party time
            party_size = int(party_size_str.split(": ")[1])  # Party Size is after "Party Size: "
            party_time = party_time_str.split(": ")[1]  # Time is after "Time: "
        except ValueError as e:
            messagebox.showerror("Parsing Error","Failed to parse reservation data: " + str(e))

        #party_name = str(selected_reservation_data.split("Party Name: ")[1].split(",")[0])
        #party_size = int(selected_reservation_data.split("Party Size: ")[2].split(",")[0])
        #party_time = str(selected_reservation_data.split("Party Time: ")[3].split(",")[0])


        selected_table = self.tableListBox.curselection()
        if not selected_table:
            messagebox.showwarning("Input Error", "Please select a table")
            return

        table_index = selected_table[0]
        selected_table_info = self.tableListBox.get(table_index)

        try:
            table_info_parts = selected_table_info.split(" (")
            table_id_str = table_info_parts[0].replace("Table ","").strip()
            table_id = int(table_id_str)
        except IndexError:
            messagebox.showerror("Table Error", "Table information is not in the expected format")
            return
        except ValueError:
            messagebox.showerror("Table Error", "Failed to extract a valid table ID")
            return


        self.database.updateTableOccupied(table_id)
        reservation_id = self.database.getReservationIDFromIndex(reservation_index)
        self.database.createOrder(party_name, party_size, party_time, table_id, reservation_id)
        #self.database.updateReservation(reservation_id)

        messagebox.showinfo("Order Created", "Reservation has been placed")

        self.app.currentReservationCount -= 1
        self.app.currentOrderCount += 1
        self.app.totalOrderCount += 1

        self.master.showFrame(mainMenu, self.database, self.app)
        #self.loadReservationData()

    def cancelReservationProcess(self):
        self.master.showFrame(mainMenu, self.database, self.app)
        #self.loadReservationData()

class enterOrdersFrame(tk.Frame):
    def __init__(self, master, database, app):
        super().__init__(master)
        self.database = database
        self.master = master
        self.app = app

        self.orderEntryInstructions = tk.Label(self, text="Please select a table begin an order")
        self.orderEntryInstructions.pack(pady=20)

        self.removeOrderButton = tk.Button(self, text="Remove Order", command=self.removeOrderTest, fg='white',bg='red')
        self.removeOrderButton.pack(pady=5)

        self.orderCancelButton = tk.Button(self, text="Cancel", command=self.orderCancel, fg='white', bg='red')
        self.orderCancelButton.pack(pady=5)

    def removeOrderTest(self):
        self.app.currentReservationCount -= 1

    def orderCancel(self):
        self.master.showFrame(mainMenu, self.database, self.app)

class completeOrdersFrame(tk.Frame):
    def __init__(self, master, database, app):
        super().__init__(master)
        self.database = database
        self.master = master
        self.app = app

        self.orderProcessInstructions = tk.Label(self, text="Menu for paying our orders")
        self.orderProcessInstructions.pack(pady=20)

        self.orderProcessCancel = tk.Button(self, text="Cancel", command=self.cancelOrderProcess, fg='white', bg='red')
        self.orderProcessCancel.pack(pady=5)

    def cancelOrderProcess(self):
        self.master.showFrame(mainMenu, self.database, self.app)

class viewOrderHistoryFrame(tk.Frame):
    def __init__(self, master, database, app):
        super().__init__(master)
        self.database = database
        self.master = master
        self.app = app

        self.orderHistoryInstructions = tk.Label(self, text="Menu to see order history")
        self.orderHistoryInstructions.pack(pady=20)

        self.orderHistoryListBox = tk.Listbox(self, width=60, height=10)
        self.orderHistoryListBox.pack(pady=10)

        self.orderHistoryReturnButton = tk.Button(self, text="Return", command=self.orderHistoryReturn, fg='white', bg='red')
        self.orderHistoryReturnButton.pack(pady=5)

        self.loadOrderHistory()

    def loadOrderHistory(self):
        self.orderHistoryListBox.delete(0, tk.END)
        if self.database:
            finishedOrders = self.database.getOrderHistory()
            for order in finishedOrders:
                display_text = f"(ID: {order[0]}) (Order Name: {order[1]}) (Party Size: {order[2]}) (Order Time: {order[3]}) (Table sat at: {order[4]})"
                self.orderHistoryListBox.insert(tk.END, display_text)
        else:
            print("Error: Database for Orders not Initialized")

    def orderHistoryReturn(self):
        self.master.showFrame(mainMenu, self.database, self.app)