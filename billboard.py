import tkinter as tk  # Import the tkinter module for GUI
import mysql.connector  # Import the mysql.connector module for MySQL database connection

# Read MySQL connection details from text file
with open('SQL_details.txt', 'r') as file:
    connection_info = dict(line.strip().split('=') for line in file)
    # Read the lines from the text file and create a dictionary with key-value pairs

# Establish MySQL connection
mydb = mysql.connector.connect(**connection_info)
# Connect to the MySQL database using the connection details

mycursor = mydb.cursor()  # Create a cursor object to execute SQL queries
mycursor.execute("select * from occupiedparkings")  # Execute SQL query to select all occupied parkings
occparks = mycursor.fetchall()  # Fetch all the results from the executed query
lines = []  # Create an empty list to store the parking numbers
for park in occparks:
    lines.append(park[0])  # Append each parking number to the list

w2_occupied_parkings = 0  # Variable to store the count of occupied 2-wheeler parkings
w4_occupied_parkings = 0  # Variable to store the count of occupied 4-wheeler parkings
t_occupied_parkings = 0  # Variable to store the count of occupied truck parkings

# Iterate through each parking number in the list and count the occupied parkings based on their type
for line in lines:
    if int(line) < 10000:
        w2_occupied_parkings += 1
    elif 10000 <= int(line) < 13000:
        w4_occupied_parkings += 1
    elif int(line) >= 13000:
        t_occupied_parkings += 1

Billboard = tk.Tk()  # Create the main tkinter window

frm_v = tk.Frame(padx=30, pady=30)  # Create a frame for vertical alignment
lbl_main1 = tk.Label(master=Billboard, font=("Consolas", 45), text='Available', padx=10, pady=5)
lbl_main2 = tk.Label(master=Billboard, font=("Consolas", 45), text='Parkings', padx=10, pady=5)
# Create labels for the main title of available parkings
lbl_w2 = tk.Label(master=frm_v, font=("Consolas", 20), text=('2-Wheelers:', 10000 - w2_occupied_parkings))
# Create a label for displaying the count of available 2-wheeler parkings
lbl_w4 = tk.Label(master=frm_v, font=("Consolas", 20), text=('4-Wheelers:', 3000 - w4_occupied_parkings))
# Create a label for displaying the count of available 4-wheeler parkings
lbl_t = tk.Label(master=frm_v, font=("Consolas", 20), text=('Trucks:', 500 - t_occupied_parkings))
# Create a label for displaying the count of available truck parkings

# Pack the labels
lbl_main1.pack()
lbl_main2.pack() 
frm_v.pack()
lbl_w2.pack()
lbl_w4.pack()
lbl_t.pack()

Billboard.mainloop()  # Start the tkinter event loop to display the GUI and handle user interactions
