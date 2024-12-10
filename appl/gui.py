import tkinter as tk
from tkinter import messagebox
import sqlite3



class restaurantApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Restaurant Management System")
        self.geometry("1820x880")

        self.mainMenuFrame = mainMenu(self)
        self.mainMenuFrame.pack()

    def showFrame(self, frameClass):
        for widget in self.winfo_children():
            widget.pack_forget()

        frameClass(self).pack()

class mainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

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

#Moves to the menu for making a new reservation. Does not need logic check as should always be possible
    def addReservations(self):
        self.master.showFrame(addReservationFrame)

    def processReservations(self):
        pass

    def enterOrders(self):
        pass

    def completeOrders(self):
        pass

    def viewOrderHistory(self):
        pass

    def closeRestaurant(self):
        pass

class addReservationFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

#This information should be sent to database.py, but will be kept local for building
        self.mainInstructions = tk.Label(self, text="Please Enter Your Reservation Information", font=("Arial", 16))
        self.mainInstructions.pack(pady=20)

        self.nameLabel = tk.Label(self, text="Name for the party: ")
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

        self.partyTime = tk.Label(self, text="Please Enter a time for your reservation: ")
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

        messagebox.showinfo("Reservation Confirmed", f"Reservation for")

        #try:



        self.master.showFrame(mainMenu)

    def cancelReservation(self):
        self.master.showFrame(mainMenu)