import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Thunderbolt1@",
  database="parkingsystem"
)

mycursor = mydb.cursor()

mycursor.execute("select * from occupiedparkings")
occupied_parkings = mycursor.fetchall()

print(occupied_parkings)