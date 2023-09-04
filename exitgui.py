from datetime import datetime, timedelta
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import *
import mysql.connector

# Read MySQL connection details from text file
with open('SQL_details.txt', 'r') as file:  # Open the file in read mode
    connection_info = dict(line.strip().split('=') for line in file)  # Read the lines and split on '=' to get connection details

# Establish MySQL connection
mydb = mysql.connector.connect(**connection_info)  # Connect to MySQL using the extracted details

mycursor = mydb.cursor()  # Create a cursor object to interact with the database

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
w2Init = 5  # Initial charge for 2-Wheeler
w2Hour = 12  # Hourly charge for 2-Wheeler
w2Day = 250  # Daily charge for 2-Wheeler
w2Mon = 5000  # Monthly charge for 2-Wheeler

w4Init = 17  # Initial charge for 4-Wheeler
w4Hour = 40  # Hourly charge for 4-Wheeler
w4Day = 900  # Daily charge for 4-Wheeler
w4Mon = 25000  # Monthly charge for 4-Wheeler

tInit = 35  # Initial charge for Truck
tHour = 80  # Hourly charge for Truck
tDay = 1750  # Daily charge for Truck
tMon = 40000  # Monthly charge for Truck

# Function to get parking details based on sticker ID
def getParkingDetails(stickerID):
    mycursor.execute("SELECT * FROM parkingrecord")  # Execute SQL query to fetch parking record from the database
    result = mycursor.fetchall()  # Fetch all the rows

    userinfo = []  # List to store user information

    for x in result:  # Iterate over each row in the result
        if result[result.index(x)][5] == str(stickerID):  # Check if the sticker ID matches
            userinfo.append(x)  # Add the row to userinfo list

    numberPlate = userinfo[0][0]  # Extract the number plate from userinfo
    vehicleType = userinfo[0][1]  # Extract the vehicle type from userinfo
    isHandicapped = userinfo[0][2]  # Extract the handicapped status from userinfo
    dtEntry = userinfo[0][3]  # Extract the entry date and time from userinfo
    parkNum = userinfo[0][4]  # Extract the parking number from userinfo

    print(numberPlate)  # Print the number plate
    print(vehicleType)  # Print the vehicle type
    print(isHandicapped)  # Print the handicapped status
    print(dtEntry)  # Print the entry date and time
    print(parkNum)  # Print the parking number

    return numberPlate, vehicleType, isHandicapped, dtEntry, parkNum  # Return the extracted information

# Function to calculate parking charges
def parkingChargesCalc(dtEnt, dtEx, vehicleType, w2Init, w4Init, tInit, w2Hour, w4Hour, tHour, w2Day, w4Day, tDay, w2Mon, w4Mon, tMon):
    timeDiff = abs((dtEx.timestamp()) - (dtEnt.timestamp()))  # Calculate the time difference in seconds
    timeDiff = datetime.fromtimestamp(timeDiff) - timedelta(hours=3)  # Convert the time difference to a datetime object and adjust for timezone difference

    dayDiff = abs(dtEx.timetuple().tm_yday - dtEnt.timetuple().tm_yday)  # Calculate the day difference

    monDiff = 0  # Initialize the month difference
    if dayDiff >= 30:  # If day difference is greater than or equal to 30
        monDiff += int(dayDiff / 30)  # Calculate the month difference
        dayDiff = dayDiff % 30  # Calculate the remaining days

    hourDiff = timeDiff.hour  # Extract the hour difference

    if vehicleType == 0:  # If the vehicle type is 2-Wheeler
        initialCharge = w2Init # Calculate the initial charge
        monthlyCharge = monDiff * w2Mon  # Calculate the monthly charge
        dailyCharge = dayDiff * w2Day  # Calculate the daily charge
        hourlyCharge = hourDiff * w2Hour  # Calculate the hourly charge
    elif vehicleType == 1:  # If the vehicle type is 4-Wheeler
        initialCharge = w4Init # Calculate the initial charge
        monthlyCharge = monDiff * w4Mon  # Calculate the monthly charge
        dailyCharge = dayDiff * w4Day  # Calculate the daily charge
        hourlyCharge = hourDiff * w4Hour  # Calculate the hourly charge

    elif vehicleType == 2:  # If the vehicle type is Truck
        initialCharge = tInit # Calculate the initial charge
        monthlyCharge = monDiff * tMon  # Calculate the monthly charge
        dailyCharge = dayDiff * tDay  # Calculate the daily charge
        hourlyCharge = hourDiff * tHour  # Calculate the hourly charge

    totalCharge = monthlyCharge + dailyCharge + hourlyCharge + initialCharge  # Calculate the total charge

    durationParked = (str(monDiff) + ' months, ' + str(dayDiff) + ' days, ' + str(hourDiff) + ' hours')  # Format the duration parked

    return totalCharge, durationParked  # Return the total charge and duration parked

# Function to generate a bill and process payment
def generateBill(numberPlate, vehicleType, isHandicapped, dtEnt, dtEx, durationParked, parkCharges):
    bill = []  # Create a list to store the bill information
    bill.append(numberPlate)  # Append the number plate to the bill list
    bill.append(vehicleType)  # Append the vehicle type to the bill list
    bill.append(isHandicapped)  # Append the handicapped status to the bill list
    bill.append(dtEnt)  # Append the entry date and time to the bill list
    bill.append(dtEx)  # Append the exit date and time to the bill list
    bill.append(durationParked)  # Append the duration parked to the bill list
    bill.append(parkCharges)  # Append the parking charges to the bill list

    sql = "INSERT INTO billrecord VALUES (%s, %s, %s, %s, %s, %s, %s)"  # SQL query to insert the bill record into the database
    mycursor.execute(sql, bill)  # Execute the SQL query with the bill information
    mydb.commit()  # Commit the changes to the database
    print(mycursor.rowcount, "record inserted.")  # Print the number of inserted records

    vehicleTypeStr = ""  # Initialize the vehicle type string
    if vehicleType == 0:  # If the vehicle type is 2-Wheeler
        vehicleTypeStr = "2-Wheeler"  # Set the vehicle type string as "2-Wheeler"
    elif vehicleType == 1:  # If the vehicle type is 4-Wheeler
        vehicleTypeStr = "4-Wheeler"  # Set the vehicle type string as "4-Wheeler"
    elif vehicleType == 2:  # If the vehicle type is Truck
        vehicleTypeStr = "Truck"  # Set the vehicle type string as "Truck"

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
        # Function to handle cash payment
        def cash_payment():
            # Function to handle change collection
            def change_collection():
                # Function to close the window
                def close():
                    window.destroy()
                # Create a new window to display exit message
                exit_window = tk.Toplevel(window)
                exit_window.title("Exit")
                label1 = tk.Label(exit_window, text="Have a nice day")
                label1.pack()
                # Close the exit window after 5 seconds
                exit_window.after(5000, close)
            
            cash = int(cash_entry.get())  # Get the cash entered by the user
            
            if cash < parkCharges:
                result_label.configure("Enter the correct amount of cash")  # Display an error message if the cash amount is less than the parking charges
            if cash > parkCharges:
                result_label.configure(text=str(cash) + " Rs paid.\nHere is your change of " + str(cash - parkCharges) + " Rs.")  # Display the payment amount and change if the cash amount is greater than the parking charges
                change_collect = ttk.Button(cash_window, text="Collect change", command=change_collection)
                change_collect.pack()  # Create a button to collect change
            elif cash == parkCharges:
                result_label.configure(text=str(cash) + " Rs paid")  # Display the payment amount if the cash amount is equal to the parking charges
            
        cash_window = tk.Toplevel(window)  # Create a new window for cash payment
        cash_window.title("Exit gate")
        clbl = tk.Label(cash_window, text="Enter cash here")
        clbl.pack()  # Label to prompt the user to enter cash
        cash_entry = ttk.Entry(cash_window)
        cash_entry.pack()  # Entry field for cash amount
        cash_button = ttk.Button(cash_window, text="Pay", command=cash_payment)
        cash_button.pack()  # Button to initiate cash payment
        result_label = tk.Label(cash_window, text="")
        result_label.pack()  # Label to display payment result


    def card(event):
        # Function to handle card payment
        def close():
            window.destroy()  # Function to close the window
        
        def card_payment():
            pay_amt = parkCharges  # Get the payment amount
            card_no = int(card_no_entry.get())  # Get the card number entered by the user
            card_label.configure(text=str(pay_amt) + " Rs paid from card no.: " + str(card_no))  # Display the payment amount and card number
            card_window.after(1500, close)  # Close the window after a delay of 1.5 seconds
        
        card_window = tk.Toplevel(window)  # Create a new window for card payment
        card_window.title("Exit gate")
        clbl = tk.Label(card_window, text="Card Number")
        clbl.pack()  # Label to prompt the user to enter the card number
        card_no_entry = ttk.Entry(card_window)
        card_no_entry.pack()  # Entry field for card number
        ulbl = tk.Label(card_window, text="UVC")
        ulbl.pack()  # Label to prompt the user to enter the UVC
        uvc_entry = ttk.Entry(card_window)
        uvc_entry.pack()  # Entry field for UVC
        elbl = tk.Label(card_window, text="Expiry date")
        elbl.pack()  # Label to prompt the user to enter the expiry date
        exp_entry = ttk.Entry(card_window)
        exp_entry.pack()  # Entry field for expiry date
        card_button = ttk.Button(card_window, text="Pay", command=card_payment)
        card_button.pack()  # Button to initiate card payment
        card_label = tk.Label(card_window, text="")
        card_label.pack()  # Label to display payment result


    def upi(event):
        # Function to handle UPI payment
        def close():
            window.destroy()  # Function to close the window
        
        def upi_payment():
            pay_amt = parkCharges  # Get the payment amount
            upi_id = int(upi_id_entry.get())  # Get the UPI ID entered by the user
            upi_pin = int(upi_pin_entry.get())  # Get the UPI PIN entered by the user
            upi_label.configure(text=str(pay_amt) + " Rs paid to Parking Services from ID: " + str(upi_id))  # Display the payment amount and UPI ID
            upi_window.after(1500, close)  # Close the window after a delay of 1.5 seconds
        
        upi_window = tk.Toplevel(window)  # Create a new window for UPI payment
        upi_window.title("Exit gate")
        uidlbl = tk.Label(upi_window, text="UPI ID")
        uidlbl.pack()  # Label to prompt the user to enter the UPI ID
        upi_id_entry = ttk.Entry(upi_window)
        upi_id_entry.pack()  # Entry field for UPI ID
        ulbl = tk.Label(upi_window, text="UPI PIN")
        ulbl.pack()  # Label to prompt the user to enter the UPI PIN
        upi_pin_entry = ttk.Entry(upi_window)
        upi_pin_entry.pack()  # Entry field for UPI PIN
        upi_button = ttk.Button(upi_window, text="Pay", command=upi_payment)
        upi_button.pack()  # Button to initiate UPI payment
        upi_label = tk.Label(upi_window, text="")
        upi_label.pack()  # Label to display payment result

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
    stickerID = int(entry.get())  # Get the sticker ID from the entry field
    numberPlate, vehicleType, isHandicapped, dtEntry, parkNum = getParkingDetails(stickerID)  # Get the parking details based on sticker ID

    dtObjectEntry = datetime.strptime(dtEntry, '%Y-%m-%d %H:%M:%S')  # Convert the entry date and time to a datetime object
    dtObjectExit = datetime.now()  # Get the current date and time as the exit date and time
    dtObjectExit = dtObjectExit.strftime("%Y-%m-%d %H:%M:%S")

    parkingCharges, durationParked = parkingChargesCalc(  # Calculate the parking charges and duration parked
        dtObjectEntry, dtObjectExit, vehicleType, w2Init, w4Init, tInit, w2Hour, w4Hour, tHour, w2Day, w4Day, tDay, w2Mon, w4Mon, tMon
    )

    generateBill(numberPlate, vehicleType, isHandicapped, dtObjectEntry, dtObjectExit, durationParked, parkingCharges)  # Generate the bill and process payment

    sql = "DELETE FROM occupiedparkings WHERE parkno = " + str(parkNum)  # SQL query to remove the occupied parking from the database
    mycursor.execute(sql)  # Execute the SQL query
    mydb.commit()  # Commit the changes to the database
    print(mycursor.rowcount, "parking number removed.")  # Print the number of removed parking numbers

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
