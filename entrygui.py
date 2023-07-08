from datetime import datetime
import mysql.connector
from roboflow import Roboflow
import csv
import random
import tkinter as tk
from tkinter import *
import cv2

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
window.title("Entry gate")

# Variables
vehicleType = tk.IntVar()
numberPlate = tk.StringVar()
isHandicapped = tk.IntVar()

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

# Function to capture an image using OpenCV
def captureImage():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)
    return image_path

# Function to autofill the number plate using the Roboflow API
def autofillNumPlate():
    rf = Roboflow(api_key="2vPtNoQmzOKODr6Yy5A1")
    project = rf.workspace("adam-toth-b7suq").project("license-plate-characters-7qltj")
    model = project.version("1").model
    imagePath = 'testImages/testPlate5.jpg'
    pred_array = (model.predict(imagePath, confidence=50, overlap=30))
    class_array = []
    x_array = []
    i = 0
    while i < len(pred_array):
        class_array.append(pred_array[i]["class"])
        x_array.append(pred_array[i]["x"])
        i+=1
    for i in range(len(x_array)):
        for j in range(len(x_array) - i - 1):
            if x_array[j] > x_array[j + 1]:
                temp_x = x_array[j]
                x_array[j] = x_array[j + 1]
                x_array[j + 1] = temp_x

                temp_class = class_array[j]
                class_array[j] = class_array[j + 1]
                class_array[j + 1] = temp_class
    numPlate = ''.join(class_array)
    return numPlate

# Function to enter vehicle information
def enterInfo():
    def validate_info():
        # Declare the variables as global
        global vehicleType, numberPlate, isHandicapped

        # Get the input values
        vehicle_type = vehicleType.get()
        number_plate = numberPlate.get()
        is_handicapped = isHandicapped.get()

        # Update the global variables
        vehicleType = vehicle_type
        numberPlate = number_plate
        isHandicapped = is_handicapped

        # Close the info window
        info_window.destroy()

        # Generate the parking sticker
        generateParkingSticker()

    # Create a new window for entering info
    info_window = tk.Toplevel(window)
    info_window.geometry('700x420')
    info_window.title("Entry gate")

    # Vehicle Type Label and Radiobuttons
    vehicle_type_label = tk.Label(info_window, font=('Consolas', 20), text="Vehicle Type:")
    vehicle_type_label.pack()

    vehicle_type_frame = tk.Frame(info_window)
    vehicle_type_frame.pack()

    vehicle_type_2w = tk.Radiobutton(vehicle_type_frame, font=('Consolas', 13), text="2-Wheeler", variable=vehicleType, value=0, indicatoron=False, height=3, width=10)
    vehicle_type_2w.pack(side="left")
    vehicle_type_4w = tk.Radiobutton(vehicle_type_frame, font=('Consolas', 13), text="4-Wheeler", variable=vehicleType, value=1, indicatoron=False, height=3, width=10)
    vehicle_type_4w.pack(side="left")
    vehicle_type_truck = tk.Radiobutton(vehicle_type_frame, font=('Consolas', 13), text="Truck", variable=vehicleType, value=2, indicatoron=False, height=3, width=10)
    vehicle_type_truck.pack(side="left")

    lbl_blanc = tk.Label(info_window, text=' ')
    lbl_blanc.pack()

    # Number Plate Label and Entry
    number_plate_label = tk.Label(info_window, font=('Consolas', 20), text="Number Plate:")
    number_plate_label.pack()

    try:
        # Autofill the number plate using image recognition
        number_plate = autofillNumPlate()
        print('Number plate detected')
    except:
        number_plate = ''
    number_plate_entry = tk.Entry(info_window, font=('Consolas', 25), textvariable=numberPlate)
    number_plate_entry.insert(0, number_plate)
    number_plate_entry.pack()

    lbl_blanc2 = tk.Label(info_window, text=' ')
    lbl_blanc2.pack()

    # Handicapped Label and Checkbutton
    handicapped_check = tk.Checkbutton(info_window, text="Handicapped?\nPress to select", variable=isHandicapped, 
                                  font=('Consolas', 15), indicatoron=False, 
                                  selectcolor='dark grey', fg='black')
    handicapped_check.pack()

    lbl_blanc3 = tk.Label(info_window, text=' ')
    lbl_blanc3.pack()

    # Submit Button
    submit_button = tk.Button(info_window, font=('Consolas', 20), text="Submit", command=validate_info)
    submit_button.pack()

    # Error Label
    error_label = tk.Label(info_window, font=15, padx=5, pady=5, fg="red")
    error_label.pack()

# Function to generate the parking sticker
def generateParkingSticker():
    def check_available_parking():
        occupied_parkings = []
        mycursor.execute("select * from occupiedparkings")
        occupied_parkings = mycursor.fetchall()

        while True:
            if vehicleType == 0:
                vehicle_type_str = "2-Wheeler"
                park_num = random.randrange(0, 9499, 1)
                if isHandicapped == 1:
                    park_num = random.randrange(9500, 9999, 1)
            elif vehicleType == 1:
                vehicle_type_str = "4-Wheeler"
                park_num = random.randrange(10000, 12799, 1)
                if isHandicapped == 1:
                    park_num = random.randrange(12800, 12999, 1)
            elif vehicleType == 2:
                vehicle_type_str = "Truck"
                park_num = random.randrange(13000, 13499, 1)

            if park_num not in occupied_parkings:
                break

            else:
                print('No parking space available.')

        sticker_id = random.randrange(1000000000, 9999999999)
        # Insert the occupied parking into the database
        sql = "INSERT INTO occupiedparkings VALUES (" + str(park_num) + ")"
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "parking number inserted.")

        # Display the sticker details
        sticker_label.config(font=15, text="===============\n" +
                                   str(sticker_id) + "\n" +
                                   "---------------\n" +
                                   "Parking: " + str(park_num) + "\n" +
                                   "Type: " + vehicle_type_str + "\n" +
                                   ("Handicapped\n" if isHandicapped == 1 else "") +
                                   "===============")

        # Store the parking record in the database
        parking_data_sql = [numberPlate, vehicleType, isHandicapped, dtObjectEntry, park_num, sticker_id]
        sql = "INSERT INTO parkingrecord VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, parking_data_sql)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

    def collect(event):
        # Close the sticker window
        window.destroy()
    
    # Create a new window for displaying the parking sticker
    sticker_window = tk.Toplevel(window)
    sticker_window.title("Parking Sticker")

    # Sticker Label
    sticker_label = tk.Label(sticker_window, text="")
    sticker_label.pack()

    # Check available parking and display the sticker
    check_available_parking()

    # Sticker Collect Button
    sticker_collect_btn = tk.Button(sticker_window, text='Collect sticker')
    sticker_collect_btn.pack()
    sticker_collect_btn.bind("<Button-1>", collect)

# Entry Date and Time
dtEntry = '2000,2,25; 06:00'

# Convert entry date and time to datetime object
dtObjectEntry = datetime.strptime(dtEntry, '%Y,%m,%d; %H:%M')

# Entry Info Button
info_button = tk.Button(window, height=2, width=7, font=("Consolas", 35), text="Push", command=enterInfo)
info_button.pack()

# Run the tkinter main loop
window.mainloop()
