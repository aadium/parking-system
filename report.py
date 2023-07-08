import pandas as pd
import matplotlib.pyplot as plt

totalUsers = pd.read_csv('parkingRecord.csv')
print('Total users:')
print(totalUsers.to_string())
print('======================================================================================')
print('Statitics:')
print('Vehicle type:')
print(totalUsers['vehicleType'].describe().round(decimals=2))
print('-------------------------------------')
print('Handicap:')  
print(totalUsers['isHandicapped'].describe().round(decimals=2))
print('-------------------------------------')
print('Parking number:')
print(totalUsers['parkNum'].describe().round(decimals=2))
mvv = list(totalUsers['vehicleType'])

plt.bar(x='2-wheeler', height=mvv.count(0))
plt.bar(x='4-wheeler', height=mvv.count(1))
plt.bar(x='Truck', height=mvv.count(2))
plt.title(label='Total parked vehicles')
plt.show()