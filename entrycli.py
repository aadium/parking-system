import csv
import datetime
import re
import random

vehicleType = 0
numberPlate = ""
isHandicapped = 0

durationParked = ""

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

def enterInfo(vehicleType, numberPlate, isHandicapped, w2Init, w4Init, tInit, w2Hour, w4Hour, tHour, w2Day, w4Day, tDay, w2Mon, w4Mon, tMon):

    vehicleType = int(input("Please enter the vehicle type (0 for 2-Wheeler, 1 for 4-wheeler, 2 for truck): "))

    while ((vehicleType != 0) and (vehicleType != 1) and (vehicleType != 2)):
        vehicleType = int(input("Please enter 0 for 2-Wheeler, 1 for 4-wheeler, 2 for truck: "))

    numberPlate = input("Please enter the number plate without spaces: ")
    while ((not re.match(r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$', numberPlate)) and (not re.match(r'^[A-Z]{2}\d{2}[A-Z]{2}\d{3}$', numberPlate))):
        numberPlate = input("Please enter a valid number plate without spaces: ")

    if (vehicleType != 2):
        isHandicapped = int(input("Are you handicapped? (1 for yes, 0 for no): "))

    return vehicleType, numberPlate, isHandicapped

def generateParkingSticker(vehicleType, isHandicapped, dtEnt):

    parkNum = 0
    vehicleTypeStr = ""
    if (vehicleType == 0):
        vehicleTypeStr = "2-Wheeler"
        parkNum = random.randrange(0, 9499, 1)
        if (isHandicapped == 1):
            parkNum = random.randrange(9500, 9999, 1)
    elif (vehicleType == 1):
        vehicleTypeStr = "4-Wheeler"
        parkNum = random.randrange(10000, 12799, 1)
        if (isHandicapped == 1):
            parkNum = random.randrange(12800, 12999, 1)
    elif (vehicleType == 2):
        vehicleTypeStr = "Truck"
        parkNum = random.randrange(13000, 13499, 1)

    stickerID = random.randrange(1000000000, 9999999999, 1)

    occParkList = []
    fp = open("occupiedParkings.txt", "r")
    for i in fp:
        occParkList.append(int(i))
    fp.close()

    while (parkNum in occParkList):
        if (vehicleType == 0):
            vehicleTypeStr = "2-Wheeler"
            parkNum = random.randrange(0, 9499, 1)
            if (isHandicapped == 1):
                parkNum = random.randrange(9500, 9999, 1)
        elif (vehicleType == 1):
            vehicleTypeStr = "4-Wheeler"
            parkNum = random.randrange(10000, 12799, 1)
            if (isHandicapped == 1):
                parkNum = random.randrange(12800, 12999, 1)
        elif (vehicleType == 2):
            vehicleTypeStr = "Truck"
            parkNum = random.randrange(13000, 13499, 1)

    print("===============")
    print(stickerID)
    print("---------------")
    print('Parking:', parkNum)
    Fp = open("occupiedParkings.txt", "a")
    Fp.writelines(str(parkNum) + '\n')
    Fp.close()
    print("Type:", vehicleTypeStr)
    if (isHandicapped == 1):
        print("Handicapped")
    print("===============")

    parkingData = []
    parkingData.append(stickerID)
    parkingData.append(numberPlate)
    parkingData.append(vehicleType)
    parkingData.append(isHandicapped)
    parkingData.append(dtEnt)
    parkingData.append(parkNum)

    with open('parkingRecord.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(parkingData)

dtEntry = '2000,2,25; 06:00'
dtObjectEntry = datetime.strptime(dtEntry, '%Y,%m,%d; %H:%M')

vehicleType, numberPlate, isHandicapped = enterInfo(vehicleType, numberPlate, isHandicapped, w2Init, w4Init, tInit, w2Hour, w4Hour, tHour, w2Day, w4Day, tDay, w2Mon, w4Mon, tMon)

generateParkingSticker(vehicleType, isHandicapped, dtObjectEntry)