from datetime import datetime, timedelta
import csv
import re
import random

numberPlate = ''
vehicleType = 0
isHandicapped = 0
dtEntry = ''
parkNum = 0
durationParked = 0

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

def getParkingDetails(numberPlate, vehicleType, isHandicapped, dtEntry, parkNum):
    with open("parkingRecord.csv", "r") as f:
        lines = csv.reader(f)
        lines = list(lines)
        lines.pop(0)
        for row in lines:
            if (int(row[0]) == stickerID):
                numberPlate = row[1]
                vehicleType = int(row[2])
                isHandicapped = int(row[3])
                dtEntry = row[4]
                parkNum = int(row[5])
    
    return numberPlate, vehicleType, isHandicapped, dtEntry, parkNum

def parkingChargesCalc(dtEnt, dtEx, durationParked, vehicleType, w2Init, w4Init, tInit, w2Hour, w4Hour, tHour, w2Day, w4Day, tDay, w2Mon, w4Mon, tMon):

    timeDiff = abs((dtEx.timestamp()) - (dtEnt.timestamp()))
    timeDiff = datetime.fromtimestamp(timeDiff) - timedelta(hours=3)

    dayDiff = abs(dtEx.timetuple().tm_yday - dtEnt.timetuple().tm_yday)

    monDiff = 0
    if (dayDiff >= 30):
        monDiff += int(dayDiff/30);
        dayDiff = dayDiff%30;

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

def generateBill(numberPlate, vehicleType, isHandicapped, dtEnt, dtEx, durationParked, parkCharges, parkNum):

    bill = []
    bill.append(numberPlate)
    bill.append(vehicleType)
    bill.append(isHandicapped)
    bill.append(dtEnt)
    bill.append(dtEx)
    bill.append(durationParked)
    bill.append(parkCharges)

    vehicleTypeStr = ""
    if (vehicleType == 0):
        vehicleTypeStr = "2-Wheeler"
    elif (vehicleType == 1):
        vehicleTypeStr = "4-Wheeler"
    elif (vehicleType == 2):
        vehicleTypeStr = "Truck"

    print('=======================================')
    print('Vehicle type:', vehicleTypeStr)
    print('Entry time:', dtEnt)
    print('Exit time:', dtEx)
    print('Duration:', durationParked)
    print('Parking charges:', parkCharges, 'Rs')
    print('=======================================')

    with open('billRecords.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(bill)
    
    with open("occupiedParkings.txt", "r") as f:
        lines = f.readlines()
    with open("occupiedParkings.txt", "w") as f:
        for line in lines:
            if int(line.strip("\n")) != parkNum:
                f.write(line)

def chargesPayment(parkCharges):

    paymentMethod = int(input("Enter the mode of payment (0 for cash, 1 for card, 2 for UPI): "))

    if (paymentMethod == 0):
        cash = int(input("Give cash: "))
        while (cash < parkCharges):
            cash = int(input("Enter the correct amount of cash: "))
        print(cash, 'Rs paid')
        if (cash > parkCharges):
            change = cash - parkCharges
            print("Collect change:", change, 'Rs')
            input('Press any key to collect: ')
    elif (paymentMethod == 1):
        payAmt = parkCharges
        cardNo = int(input("Enter card no.: "))
        accNo = int(input("Enter account no.: "))
        print(payAmt, 'Rs paid from account no.:', accNo, ', card no.:', cardNo)
    elif (paymentMethod == 2):
        payAmt = parkCharges
        upiPin = int(input("Enter UPI PIN: "))
        print(payAmt, 'Rs paid to Parking Services')

    print('Have a nice day')

dtExit = '2000,2,25; 23:00' 
dtObjectExit = datetime.strptime(dtExit, '%Y,%m,%d; %H:%M')

stickerID = int(input('Enter sticker ID: '))
numberPlate, vehicleType, isHandicapped, dtEntry, parkNum = getParkingDetails(numberPlate, vehicleType, isHandicapped, dtEntry, parkNum)

dtObjectEntry = datetime.strptime(dtEntry, '%Y-%m-%d %H:%M:%S')

parkingCharges, durationParked =  parkingChargesCalc(dtObjectEntry, dtObjectExit, durationParked, vehicleType, w2Init, w4Init, tInit, w2Hour, w4Hour, tHour, w2Day, w4Day, tDay, w2Mon, w4Mon, tMon)

generateBill(numberPlate, vehicleType, isHandicapped, dtObjectEntry, dtObjectExit, durationParked, parkingCharges, parkNum)

chargesPayment(parkingCharges)