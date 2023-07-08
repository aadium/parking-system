from datetime import datetime, timedelta
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import *
import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Thunderbolt1@",
  database="parkingsystem"
)
mycursor = mydb.cursor()

# Create the tkinter window
window = tk.Tk()
window.title("Exit gate")

# Initialize variables
numberPlate = ''
vehicleType = 0
isHandicapped = 0
dtEntry = ''
parkNum = 0

# Constants for parking rates
w2Init = 5
w2Hour = 12
w2Day = 250
w2Mon = 5000

w4Init = 17
w4Hour = 40
w4Day = 900
w4Mon = 25000

tInit = 35
tHour = 80
tDay = 1750
tMon = 40000

# Function to get parking details based on sticker ID
def getParkingDetails(stickerID):
    mycursor.execute("select * from parkingrecord")
    result = mycursor.fetchall()

    userinfo = []

    for x in result:
        if(result[result.index(x)][5] == str(stickerID)):
            userinfo.append(x)
    
    numberPlate = userinfo[0][0]
    vehicleType = userinfo[0][1]
    isHandicapped = userinfo[0][2]
    dtEntry = userinfo[0][3]
    parkNum = userinfo[0][4]

    print(numberPlate)
    print(vehicleType)
    print(isHandicapped)
    print(dtEntry)
    print(parkNum)
    
    return numberPlate, vehicleType, isHandicapped, dtEntry, parkNum

# Function to calculate parking charges
def parkingChargesCalc(dtEnt, dtEx, vehicleType, w2Init, w4Init, tInit, w2Hour, w4Hour, tHour, w2Day, w4Day, tDay, w2Mon, w4Mon, tMon):
    timeDiff = abs((dtEx.timestamp()) - (dtEnt.timestamp()))
    timeDiff = datetime.fromtimestamp(timeDiff) - timedelta(hours=3)

    dayDiff = abs(dtEx.timetuple().tm_yday - dtEnt.timetuple().tm_yday)

    monDiff = 0
    if (dayDiff >= 30):
        monDiff += int(dayDiff / 30)
        dayDiff = dayDiff % 30

    hourDiff = timeDiff.hour

    if (vehicleType == 0):
        monthlyCharge = monDiff * w2Mon
        dailyCharge = dayDiff * w2Day
        hourlyCharge = hourDiff * w2Hour
        initialCharge = w2Init
    elif (vehicleType == 1):
        monthlyCharge = monDiff * w4Mon
        dailyCharge = dayDiff * w4Day
        hourlyCharge = hourDiff * w4Hour
        initialCharge = w4Init
    elif (vehicleType == 2):
        monthlyCharge = monDiff * tMon
        dailyCharge = dayDiff * tDay
        hourlyCharge = hourDiff * tHour
        initialCharge = tInit

    totalCharge = monthlyCharge + dailyCharge + hourlyCharge + initialCharge

    durationParked = (str(monDiff) + ' months, ' + str(dayDiff) + ' days, ' + str(hourDiff) + ' hours')
    return totalCharge, durationParked

# Function to generate a bill and process payment
def generateBill(numberPlate, vehicleType, isHandicapped, dtEnt, dtEx, durationParked, parkCharges):
    bill = []
    bill.append(numberPlate)
    bill.append(vehicleType)
    bill.append(isHandicapped)
    bill.append(dtEnt)
    bill.append(dtEx)
    bill.append(durationParked)
    bill.append(parkCharges)

    sql = "INSERT INTO billrecord VALUES (%s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, bill)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

    vehicleTypeStr = ""
    if (vehicleType == 0):
        vehicleTypeStr = "2-Wheeler"
    elif (vehicleType == 1):
        vehicleTypeStr = "4-Wheeler"
    elif (vehicleType == 2):
        vehicleTypeStr = "Truck"

    # Create a new window for the bill
    bill_window = tk.Toplevel(window)
    bill_window.title("Exit gate")

    # Label to display vehicle type
    label1 = tk.Label(bill_window, text="Vehicle type: " + vehicleTypeStr)
    label1.pack()

    # Label to display entry time
    label2 = tk.Label(bill_window, text="Entry time: " + str(dtEnt))
    label2.pack()

    # Label to display exit time
    label3 = tk.Label(bill_window, text="Exit time: " + str(dtEx))
    label3.pack()

    # Label to display duration parked
    label4 = tk.Label(bill_window, text="Duration: " + str(durationParked))
    label4.pack()

    # Label to display parking charges
    label5 = tk.Label(bill_window, text="Parking charges: " + str(parkCharges) + " Rs")
    label5.pack()

    def cash(event):
        def cash_payment():
            def change_collection():
                # Function to collect change and close the window
                def close():
                    window.destroy()
                # Create a new window to display exit message
                exit_window = tk.Toplevel(window)
                exit_window.title("Exit")
                label1 = tk.Label(exit_window, text="Have a nice day")
                label1.pack()
                # Close the exit window after 5 seconds
                exit_window.after(5000, close)
            # Get the cash entered by the user
            cash = int(cash_entry.get())
            if(cash < parkCharges):
                result_label.configure("Enter the correct amount of cash")
            if(cash > parkCharges):
                result_label.configure(text=str(cash) + " Rs paid.\nHere is your change of " + str(cash - parkCharges) + " Rs.")
                change_collect = ttk.Button(cash_window, text="Collect change", command=change_collection)
                change_collect.pack()
            elif(cash == parkCharges):
                result_label.configure(text=str(cash) + " Rs paid")
        # Create a new window for cash payment
        cash_window = tk.Toplevel(window)
        cash_window.title("Exit gate")
        clbl = tk.Label(cash_window, text="Enter cash here")
        clbl.pack()
        cash_entry = ttk.Entry(cash_window)
        cash_entry.pack()
        cash_button = ttk.Button(cash_window, text="Pay", command=cash_payment)
        cash_button.pack()
        result_label = tk.Label(cash_window, text="")
        result_label.pack()
    
    def card(event):
        def close():
            window.destroy()
        def card_payment():
            pay_amt = parkCharges
            card_no = int(card_no_entry.get())
            card_label.configure(text=str(pay_amt) + " Rs paid from card no.: " + str(card_no))
            card_window.after(1500, close)
        # Create a new window for card payment
        card_window = tk.Toplevel(window)
        card_window.title("Exit gate")
        clbl = tk.Label(card_window, text="Card Number")
        clbl.pack()
        card_no_entry = ttk.Entry(card_window)
        card_no_entry.pack()
        ulbl = tk.Label(card_window, text="UVC")
        ulbl.pack()
        uvc_entry = ttk.Entry(card_window)
        uvc_entry.pack()
        elbl = tk.Label(card_window, text="Expiry date")
        elbl.pack()
        exp_entry = ttk.Entry(card_window)
        exp_entry.pack()
        card_button = ttk.Button(card_window, text="Pay", command=card_payment)
        card_button.pack()
        card_label = tk.Label(card_window, text="")
        card_label.pack()
    
    def upi():
        def close():
            window.destroy()
        def upi_payment():
            pay_amt = parkCharges
            upi_pin = int(upi_pin_entry.get())
            upi_label.configure(text=str(pay_amt) + " Rs paid to Parking Services")
            upi_window.after(1500, close)
        # Create a new window for UPI payment
        upi_window = tk.Toplevel(window)
        upi_window.title("Exit gate")
        uidlbl = tk.Label(upi_window, text="UPI ID")
        uidlbl.pack()
        upi_id_entry = ttk.Entry(upi_window)
        upi_id_entry.pack()
        ulbl = tk.Label(upi_window, text="UPI PIN")
        ulbl.pack()
        upi_pin_entry = ttk.Entry(upi_window)
        upi_pin_entry.pack()
        upi_button = ttk.Button(upi_window, text="Pay", command=upi_payment)
        upi_button.pack()
        upi_label = tk.Label(upi_window, text="")
        upi_label.pack()
    
    # Create buttons for different payment methods
    cashbtn = tk.Button(bill_window, text="Cash")
    cashbtn.pack()
    cashbtn.bind("<Button-1>", cash)
    cardbtn = tk.Button(bill_window, text="Card")
    cardbtn.pack()
    cardbtn.bind("<Button-1>", card)
    upibtn = tk.Button(bill_window, text="UPI")
    upibtn.pack()
    upibtn.bind("<Button-1>", upi)

# Function to process exit gate operations
def exitGateProcess():
    stickerID = int(entry.get())
    numberPlate, vehicleType, isHandicapped, dtEntry, parkNum = getParkingDetails(stickerID)

    # Convert entry and exit times to datetime objects
    dtObjectEntry = datetime.strptime(dtEntry, '%Y-%m-%d %H:%M:%S')
    dtExit = '2000,2,28; 14:35'  # Temporary exit time for testing
    dtObjectExit = datetime.strptime(dtExit, '%Y,%m,%d; %H:%M')

    # Calculate parking charges and duration parked
    parkingCharges, durationParked = parkingChargesCalc(
        dtObjectEntry, dtObjectExit, vehicleType, w2Init, w4Init, tInit, w2Hour, w4Hour, tHour, w2Day, w4Day, tDay, w2Mon, w4Mon, tMon
    )

    # Generate bill and process payment
    generateBill(numberPlate, vehicleType, isHandicapped, dtObjectEntry, dtObjectExit, durationParked, parkingCharges)

    # Remove occupied parking from the database
    sql = "DELETE FROM occupiedparkings WHERE parkno = " + str(parkNum)
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "parking number removed.")

# Label and entry for entering sticker ID
label = tk.Label(window, text="Enter sticker ID:")
label.pack()
entry = ttk.Entry(window)
entry.pack()

# Button to initiate exit gate process
button = ttk.Button(window, text="Exit", command=exitGateProcess)
button.pack()

# Run the tkinter main loop
window.mainloop()