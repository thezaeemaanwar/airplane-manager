# pythons built in csv library
import csv
import sys

# existing aircrafts
aircraft = [{'type': 'medium narrow body', 'cost': 8, 'max_range': 2650, 'standard_seats': 180, 'first_class': 8},
            {'type': 'large narrow body', 'cost': 7, 'max_range': 5600,
                'standard_seats': 220, 'first_class': 10},
            {'type': 'medium wide body', 'cost': 5, 'max_range': 4050, 'standard_seats': 406, 'first_class': 14}]

# to store the details of flight


class Flight:
    type = ''
    fClassSeats = 0
    UKairport = ''
    overSeasAirport = ''
    fClassPrice = 0
    sClassPrice = 0

# function to get index from list of dict using key


def find(list, key, value):
    for i, dic in enumerate(list):
        if dic[key] == value:
            return i
    return -1

# returns List of airports read by file


def airportList():
    myList = []
    with open('airports.txt', mode='r') as csv_file:
        myList = [{key: val for key, val in row.items()}
                  for row in csv.DictReader(csv_file, skipinitialspace=True)]
    return myList


# list of all airports from airports.txt file
airports = airportList()

# returns the number of standard class seats


def standardClassSeats(flight):
    index = find(aircraft, 'type', flight.type)
    return aircraft[index]['standard_seats'] - flight.fClassSeats*2

# returns the cost per seat


def costPerSeat(flight):
    ind = find(aircraft, 'type', flight.type)
    ukind = ''
    oind = find(airports, 'Overseas airport name', flight.overSeasAirport)
    if flight.UKairport == 'Liverpool John Lennon':
        ukind = 'Distance from Liverpool John Lennon'
    elif flight.UKairport == 'Bournemouth International':
        ukind = 'Distance from Bournemouth International'
    return float(aircraft[ind]['cost'])*float(airports[oind][ukind])/100.00

# find the cost of flight


def flightCost(flight):
    return costPerSeat(flight)*(flight.fClassSeats+standardClassSeats(flight))

# returns the income of flight


def flightIncome(flight):
    fClassIncome = flight.fClassSeats*flight.fClassPrice
    sClassIncome = standardClassSeats(flight)*flight.sClassPrice
    return fClassIncome+sClassIncome

# returns the profit of flight


def flightProfit(flight):
    return flightIncome(flight)-flightCost(flight)


# flight object to be used further
f1 = Flight()

# Main Menu


def menu():
    print("1. Enter Airport Details")
    print("2. Enter Flight Details")
    print("3. Enter price plan and calculate profit")
    print("4. Clear data")
    print("5. Quit")
    i = input("Enter your choice : ")

    # Airport Details
    if i == 1:
        ukair = raw_input(
            "Enter the three-letter airport code for the UK airport : ")
        if ukair not in ['LPL', 'BOH']:
            print("invalid UK airport code.")
            menu()
        else:
            f1.UKairport = 'Liverpool John Lennon' if ukair == 'LPL' else 'Bournemouth International'

        overseas = raw_input(
            "Enter the three-letter airport code for the overseas airport : ")
        n = False
        for i in range(len(airports)):
            if airports[i]['Overseas airport code'] == overseas:
                f1.overSeasAirport = airports[i]['Overseas airport name']
                print(f1.overSeasAirport)
                n = True
        if n == False:
            print("Invalid airport code. ")
        menu()

    # Flight Details
    elif i == 2:
        print("1. " + aircraft[0]['type'])
        print("2. "+aircraft[1]['type'])
        print("3. "+aircraft[2]['type'])
        craft = 0
        ch = input("Enter your choice : ")
        if ch == 1:
            f1.type = aircraft[0]['type']
            craft = 0
        elif ch == 2:
            f1.type = aircraft[1]['type']
            craft = 1
        elif ch == 3:
            f1.type = aircraft[2]['type']
            craft = 2
        else:
            print("Invalid Choice.")
            menu()
        print("Type : "+aircraft[craft]['type'])
        print("Running cost per seat per 100 kilometres  : ",
              aircraft[craft]['cost'])
        print("Maximum flight range : ", aircraft[craft]['max_range'])
        print("Max Standard Class Seats : ", aircraft[craft]['standard_seats'])
        print("Min First Class Seats : ", aircraft[craft]['first_class'])

        fClass = input("Enter the number of first-class seats : ")
        if fClass < aircraft[craft]['first_class']:
            print(
                "First class seats are lesser than min first class seats for this type.")
            menu()
        elif fClass > aircraft[craft]['standard_seats']:
            print("Seat number exceeds max seat limit.")
            menu()
        else:
            f1.fClassSeats = fClass
        print("Standard class seats : ", standardClassSeats(f1))
        menu()

    # Price plan and profit menu
    elif i == 3:

        if f1.UKairport == '' or f1.overSeasAirport == '':
            print("Airports not entered")
            menu()
        if f1.type == '':
            print("Plane type not entered")
            menu()
        if f1.fClassSeats == 0:
            print("First class seats not entered")
            menu()

        sprice = input("Enter the price of a standard-class seat : ")
        f1.sClassPrice = sprice
        fprice = input("Enter the price of a first-class seat : ")
        f1.fClassPrice = fprice

        print("Flight Cost per seat : ", costPerSeat(f1))
        print("Flight Cost : ", flightCost(f1))
        print("Flight Income : ", flightIncome(f1))
        print("Flight Profit : ", flightProfit(f1))

        menu()

    # Clear all data
    elif i == 4:
        f1.fClassPrice = 0
        f1.fClassSeats = 0
        f1.sClassPrice = 0
        f1.fClassSeats = 0
        f1.overSeasAirport = ''
        f1.type = ''
        f1.UKairport = ''
        print("All data cleared")
        menu()

    # Quit Program
    elif i == 5:
        print("Exiting..")
        sys.exit()

    # if the choice entered by user is other than 1-5
    else:
        print("Invalid choice. Enter from the choices given")
        menu()


menu()
