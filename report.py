import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Read MySQL connection details from text file
with open('SQL_details.txt', 'r') as file:
    connection_info = dict(line.strip().split('=') for line in file)

# Establish MySQL connection
mydb = mysql.connector.connect(**connection_info)

totalUsers = pd.read_sql("SELECT * FROM parkingrecord", con=mydb)

# Calculate the count of each vehicle type
vehicle_type_counts = totalUsers['vehicletype'].value_counts()

# Calculate percentage of vehicle types
vehicle_type_percentage = vehicle_type_counts / vehicle_type_counts.sum() * 100

handicap_counts = totalUsers['ishandicapped'].value_counts()

# Calculate percentage of handicapped users
handicap_percentage = (totalUsers['ishandicapped'].sum() / totalUsers.shape[0]) * 100

# Create a figure with subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 4))

# Bar graph for vehicle types
labels = ['2-wheeler', '4-wheeler', 'Truck']
axs[0][0].bar(labels, vehicle_type_counts.values)
axs[0][0].set_title('Vehicle Types')
axs[0][0].set_xlabel('Vehicle Type')
axs[0][0].set_ylabel('Count')

# Pie chart for vehicle type distribution
labels = ['2-wheeler', '4-wheeler', 'Truck']
axs[0][1].pie(vehicle_type_percentage, labels=labels, autopct='%1.1f%%')
axs[0][1].set_title('Vehicle Type Percentages')

# Bar graph for handicap count
labels = ['Non-Handicapped', 'Handicapped']
axs[1][0].bar(labels, handicap_counts.values)
axs[1][0].set_title('Handicapped User Count')
axs[1][0].set_xlabel('Is user handicapped')
axs[1][0].set_ylabel('Count')

# Pie chart for handicapped users
labels = ['Non-Handicapped', 'Handicapped']
axs[1][1].pie([100 - handicap_percentage, handicap_percentage], labels=labels, autopct='%1.1f%%')
axs[1][1].set_title('Percentage of Handicapped Users')

# Adjust spacing between subplots
plt.tight_layout()

# Display the plot
plt.show()
