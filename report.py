import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Thunderbolt1@",
  database="parkingsystem"
)

totalUsers = pd.read_sql("SELECT * FROM parkingrecord", con=mydb)
print('Total users:')
print(totalUsers.to_string())
print('======================================================================================')
print('Statitics:')
print('Vehicle type:')
print(totalUsers['vehicletype'].describe().round(decimals=2))
print('-------------------------------------')
print('Handicap:')  
print(totalUsers['ishandicapped'].describe().round(decimals=2))
print('-------------------------------------')
print('Parking number:')
print(totalUsers['parknum'].describe().round(decimals=2))
mvv = list(totalUsers['vehicletype'])

plt.bar(x='2-wheeler', height=mvv.count(0))
plt.bar(x='4-wheeler', height=mvv.count(1))
plt.bar(x='Truck', height=mvv.count(2))
plt.title(label='Total parked vehicles')
plt.show()