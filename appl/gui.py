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
        self.geometry("500x500")

        self.mainMenuFrame = mainMenu(self, self.database, self)
        self.mainMenuFrame.pack()

    def showFrame(self, frameClass, database=None, app=None):
        for widget in self.winfo_children():
            widget.pack_forget()

        if database is None:
            database = self.database
        if app is None:
            app = self.app
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
            messagebox.showinfo("Goodbye", "Shutting down and Clearing database. Goodbte!")
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
                reservation_id = reservation[0]
                party_name = reservation[1]
                party_size = reservation[2]
                party_time = reservation[3]
                display_text = f"{reservation_id} Name: {party_name} (Party Size: {party_size}, Time: {party_time})"
                self.reservationNotSeated.insert(tk.END, (display_text))
        else:
            print("Error: Database for reservations not initialized")

    def checkReservationData(self):
        selected_reservation = self.reservationNotSeated.curselection()
        if not selected_reservation:
            messagebox.showwarning("Input Error", "Please select a reservation")
            return

        reservation_index = selected_reservation[0]
        selected_reservation_data = self.reservationNotSeated.get(reservation_index)

        reservation_id = selected_reservation_data[0]  # The first element is the reservation ID

        # Save the reservation_id for later use
        self.reservation_id = reservation_id
        self.selected_reservation_data = selected_reservation_data

        print(f"Selected reservation data: {selected_reservation_data}")
        print(f"Selected reservation ID: {reservation_id}")

        reservation_data = self.database.getReservationById(reservation_id)
        if reservation_data:
            print(f"Retrieved reservation data: {reservation_data}")
            party_name, party_size, party_time = reservation_data[1], reservation_data[2], reservation_data[3]
            self.loadTableData(party_size)
        else:
            messagebox.showerror("Data Error", "Reservation data could not be retrieved.")
            print(f"Error retrieving reservation data for ID: {reservation_id}")

    def loadTableData(self, party_size=None):
        self.tableListBox.delete(0, tk.END)  # Clear previous data
        if self.database:
            # Fetch available tables from the database
            availableTables = self.database.getUnplacedTables()  # This gets all tables where is_Occupied = 0
            suitable_tables_found = False  # Flag to check if any table can accommodate the party size

            for table in availableTables:
                table_id = table[0]
                table_size = table[1]

                # Filter tables based on party size
                if party_size is None or table_size >= party_size:
                    # Only show tables that are large enough to accommodate the party size
                    display_text = f"Table {table_id} (Seats: {table_size}) - Available"
                    self.tableListBox.insert(tk.END,
                                             (table_id, display_text))  # Insert a tuple (table_id, display_text)
                    suitable_tables_found = True  # Found a suitable table

            # Show a message only if no suitable tables were found
            if not suitable_tables_found:
                messagebox.showinfo("No Available Tables",
                                    "There are no open tables that can accommodate this reservation. "
                                    "Process and Complete orders to place this.")
        else:
            print("Error: Database for Tables not Initialized")

    def reservationIntoOrder(self):
        selected_reservation = self.selected_reservation_data
        if not selected_reservation:
            messagebox.showwarning("Input Error", "Please select a reservation.")
            return

        reservation_id = selected_reservation[0]  # Extract reservation ID
        reservation_data = self.database.getReservationById(reservation_id)

        if reservation_data is None:
            messagebox.showerror("Data Error", "Unable to retrieve reservation data.")
            return

        party_name, party_size, party_time = reservation_data[1], reservation_data[2], reservation_data[3]

        # Step 2: Check if a table is selected
        selected_table = self.tableListBox.curselection()
        if not selected_table:
            messagebox.showwarning("Input Error", "Please select a table.")
            return

        table_index = selected_table[0]
        selected_table_data = self.tableListBox.get(table_index)
        table_id = selected_table_data[0]  # Extract table ID

        # Step 3: Send data to `createOrder` in database.py
        self.database.createOrder(party_name, party_size, party_time, table_id, reservation_id)

        # Step 4: Update reservation and table as "Placed" and "Occupied"
        self.database.updateTableOccupied(table_id)  # Set the table as occupied
        self.database.updateReservationPlaced(reservation_id)  # Set the reservation as placed

        messagebox.showinfo("Success", f"Reservation for {party_name} has been placed at Table {table_id}.")


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

        self.orderEntryInstructions = tk.Label(self, text="Please select an Order to Begin Processing")
        self.orderEntryInstructions.pack(pady=20)

        self.tableOrderListBox = tk.Listbox(self, width=60, height=10)
        self.tableOrderListBox.pack(pady=5)

        self.loadUnplacedOrders()

        self.startOrderButton = tk.Button(self, text="Begin Order", command=self.startOrder)
        self.startOrderButton.pack(pady=10)

        self.orderCancelButton = tk.Button(self, text="Cancel", command=self.orderCancel, fg='white', bg='red')
        self.orderCancelButton.pack(pady=5)

    def loadUnplacedOrders(self):
        self.tableOrderListBox.delete(0, tk.END)  # Clear previous data
        if self.database:
            unprocessed_Orders = self.database.getOrdersNotOrdered()  # Fetch tables that are occupied but no order placed
            for order in unprocessed_Orders:
                order_id = order[0]
                table_id = order[4]  # table_ID from the orders table
                order_name = order[1]  # order_Name from the orders table
                order_size = order[2]  # order_Size from the orders table
                display_text = f"{order_id}, Table: {table_id}, Name: {order_name}, Size: {order_size}"
                self.tableOrderListBox.insert(tk.END, (display_text))
        else:
            print("Error: Database for Orders not initialized")

    def startOrder(self):
        """Start the order process by selecting food items for each person at the table."""
        selected_order = self.tableOrderListBox.curselection()
        if not selected_order:
            messagebox.showwarning("Input Error", "Please select an Order.")
            return

        order_index = selected_order[0]
        selected_order_data = self.tableOrderListBox.get(order_index)
        order_id = selected_order_data[0]  # Extract the order ID

        self.selected_order_id = order_id
        self.selected_order_data = selected_order_data

        print(f"Selected order data: {selected_order_data}")
        print(f"Selected order ID: {order_id}")

        order_data = self.database.getOrderById(order_id)
        if order_data:
            print(f"Processing Order Data: {selected_order_data}")
            party_size = order_data[2]
            table_id = order_data[4]
            self.showMenu(party_size, table_id, order_id)
        else:
            messagebox.showerror("Data Error", "Could not retrieve data")
            print(f"Error pulling order Data for Order ID: {order_id}")

    def showMenu(self, party_size, table_id, order_id):
        """Show the menu items to be selected for the order."""
        self.menuWindow = tk.Toplevel(self)
        self.menuWindow.title("Select Menu Items")

        self.menuLabel = tk.Label(self.menuWindow, text="Select a food item for each person:")
        self.menuLabel.pack(pady=10)

        # Load menu items from the database
        menu_items = self.database.getMenuItems()

        self.foodChoices = []
        for i in range(party_size):
            tk.Label(self.menuWindow, text=f"Person #{i + 1}:").pack()
            food_choice_var = tk.StringVar(self.menuWindow)
            food_choice_var.set(menu_items[0][1])  # Default selection (name of the first item)
            self.foodChoices.append(food_choice_var)

            menu_dropdown = tk.OptionMenu(self.menuWindow, food_choice_var,
                                          *[item[1] for item in menu_items])  # Only use item name
            menu_dropdown.pack()

        self.confirmOrderEntryButton = tk.Button(self.menuWindow, text="Confirm Order",
                                                 command=lambda: self.confirmOrder(party_size, order_id))
        self.confirmOrderEntryButton.pack(pady=20)

    def confirmOrder(self, party_size, order_id):
        """Confirm the order and save it to the database."""
        food_items = [food_choice.get() for food_choice in self.foodChoices]

        if not all(food_item for food_item in food_items):  # If any food choice is empty, show an error
            messagebox.showwarning("Input Error", "Please make sure every person has picked a food item.")
            return

        orderFoodCost = 0.0

        for item_name in food_items:
            item = self.database.getMenuItemByName(item_name)  # We now query using the plain food name
            if item:
                item_id, item_name, item_price = item  # Unpack all three elements
                if item_price is not None:  # Check if price is valid
                    orderFoodCost += item_price
                    self.database.addOrderItem(order_id, item_id, item_price)
                else:
                    print(f"Error: Item '{item_name}' has no price.")
            else:
                print(f"Error: Item '{item_name}' not found.")

        self.database.updateOrderCost(order_id, orderFoodCost)
        self.database.updateOrderOrdered(order_id)
        messagebox.showinfo("Success", f"Your order for {party_size} guests will be ${orderFoodCost:.2f}.")
        self.menuWindow.destroy()  # Close the menu window
        self.master.showFrame(mainMenu, self.database, self.app)

    def orderCancel(self):
        self.master.showFrame(mainMenu, self.database, self.app)

class completeOrdersFrame(tk.Frame):
    def __init__(self, master, database, app):
        super().__init__(master)
        self.database = database
        self.master = master
        self.app = app

        self.orderProcessInstructions = tk.Label(self, text="Select an unpaid order to complete")
        self.orderProcessInstructions.pack(pady=20)

        self.orderNotPaidListBox = tk.Listbox(self, width=60, height=10)
        self.orderNotPaidListBox.pack(pady=10)

        self.loadUnpaidOrders()  # Load unpaid orders into the list box

        self.completeOrderButton = tk.Button(self, text="Complete Order", command=self.completeOrder)
        self.completeOrderButton.pack(pady=10)

        self.orderProcessCancel = tk.Button(self, text="Cancel", command=self.cancelOrderProcess, fg='white', bg='red')
        self.orderProcessCancel.pack(pady=5)

    def loadUnpaidOrders(self):
        """Load orders that haven't been paid into the Listbox."""
        self.orderNotPaidListBox.delete(0, tk.END)  # Clear previous data
        if self.database:
            unpaidOrders = self.database.getUnpaidOrders()  # Fetch orders that haven't been paid
            for order in unpaidOrders:
                order_id = order[0]
                table_id = order[4]  # table_ID from the orders table
                order_name = order[1]  # order_Name from the orders table
                order_size = order[2]  # order_Size from the orders table
                display_text = f"Order ID: {order_id}, Table: {table_id}, Name: {order_name}, Size: {order_size}"
                self.orderNotPaidListBox.insert(tk.END, (order_id, display_text))  # Insert a tuple with order_id and display text
        else:
            print("Error: Database for unpaid orders not initialized")

    def completeOrder(self):
        """Mark the selected order as completed and set the table as unoccupied."""
        selected_order = self.orderNotPaidListBox.curselection()
        if not selected_order:
            messagebox.showwarning("Input Error", "Please select an order to complete.")
            return

        order_index = selected_order[0]
        selected_order_data = self.orderNotPaidListBox.get(order_index)
        order_id = selected_order_data[0]  # Extract order ID

        order_data = self.database.getOrderById(order_id)
        if not order_data:
            messagebox.showerror("Data Error", "Unable to retrieve order data.")
            return

        # Step 1: Mark the order as completed (paid or finished)
        self.database.completeOrder(order_id)

        # Step 2: Update the table to unoccupied
        table_id = order_data[4]  # Get table ID from the order data
        self.database.updateTableEmpty(table_id)  # Set the table as unoccupied

        # Update application data
        self.app.currentOrderCount -= 1

        messagebox.showinfo("Order Completed", f"Order {order_id} has been completed and the table is now unoccupied.")

        self.master.showFrame(mainMenu, self.database, self.app)

    def cancelOrderProcess(self):
        self.master.showFrame(mainMenu, self.database, self.app)

class viewOrderHistoryFrame(tk.Frame):
    def __init__(self, master, database, app):
        super().__init__(master)
        self.database = database
        self.master = master
        self.app = app

        self.orderHistoryInstructions = tk.Label(self, text="Completed Order History Today")
        self.orderHistoryInstructions.pack(pady=20)

        self.orderHistoryListBox = tk.Listbox(self, width=60, height=10)
        self.orderHistoryListBox.pack(pady=10)

        self.orderDeepButton = tk.Button(self, text="See more about this order", command=self.checkOrderHistory)
        self.orderDeepButton.pack(pady=10)

        self.orderDeepHistoryListBox = tk.Listbox(self, width=60, height=10)
        self.orderDeepHistoryListBox.pack(pady=10)


        self.orderHistoryReturnButton = tk.Button(self, text="Return", command=self.orderHistoryReturn, fg='white', bg='red')
        self.orderHistoryReturnButton.pack(pady=5)

        self.loadOrderHistory()

    def loadOrderHistory(self):
        self.orderHistoryListBox.delete(0, tk.END)
        if self.database:
            finishedOrders = self.database.getOrderHistory()
            for order in finishedOrders:
                display_text = f"{order[0]} (Order Name: {order[1]}) (Party Size: {order[2]}) (Order Time: {order[3]}) (Table sat at: {order[4]})"
                self.orderHistoryListBox.insert(tk.END, display_text)
        else:
            print("Error: Database for Orders not Initialized")

    def checkOrderHistory(self):
        selectedOrder = self.orderHistoryListBox.curselection()
        if not selectedOrder:
            messagebox.showwarning("Input Error", "Please Select an Order to see more about")
        orderIndex = selectedOrder[0]
        selected_order_data = self.orderHistoryListBox.get(orderIndex)

        order_ID = selected_order_data[0]

        self.order_ID = order_ID
        self.selected_order_data = selected_order_data

        order_data = self.database.getFullOrderById(order_ID)

        if not order_data:
            messagebox.showwarning("Order Error", "The selected order is invalid or doesn't exist.")
            return

            # If valid, proceed to load the deep history
        self.loadDeepHistory(order_ID)


    def loadDeepHistory(self, order_ID):
        order_items = self.database.getOrderItemsByOrderId(order_ID)
        total_cost = 0.0
        customer_order_data = []  # List to hold the display data for the customers
        for item in order_items:
            item_name = item[0]  # Item name from order_choices
            item_price = item[1]  # Item cost from order_choices
            total_cost += item_price
            customer_order_data.append(f"{item_name} - ${item_price:.2f}")

            # Display the details in the deep history list box
        self.orderDeepHistoryListBox.delete(0, tk.END)  # Clear any previous data
        self.orderDeepHistoryListBox.insert(tk.END, f"Total Cost: ${total_cost:.2f}")
        for data in customer_order_data:
            self.orderDeepHistoryListBox.insert(tk.END, data)





    def orderHistoryReturn(self):
        self.master.showFrame(mainMenu, self.database, self.app)