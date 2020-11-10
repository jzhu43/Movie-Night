
import os
import sqlite3
from sqlite3 import Error
   ## Include SQLite package
import random

################ Connect SQLite Database ################

db_connection = None # Define the connection parameter
#db_name = "/Users/bowma/CSE 111/Project/CSE111-Project-F20/moviesdata.db" # Specify the full path of Database file
db_name = "/Users/bowma/CSE 111/Project/CSE111-Project-F20/project.db"
#db_name = "moviesdata.db"

# def openConnection(_dbFile): 
#     print("++++++++++++++++++++++++++++++++++")
#     print("Open database: ", _dbFile)
#     conn = None
#     try:
#         conn = sqlite3.connect(_dbFile)
#         print("success")
#     except Error as e:
#         print(e)

#     print("++++++++++++++++++++++++++++++++++")

#     return conn

try:
    db_connection = sqlite3.connect(db_name)
except sqlite3.Error as err: # If database connection failed this block of code  # handles the exception
    print(err)

if db_connection:
    print(db_connection) # Printing the connection object
    print("Successfully Established connection with SQLite3")
    print("\n\n")

################ Code ################

intoBrewery = False

intoWinery = False

intoBeer = False

intoWine = False


db_cursor = db_connection.cursor()


def input_data():
    print("Im in")
    addWhere=raw_input("\nWhich of the following tables would you like to insert to? \nBrewery \nWinery \nWine \nBeer\n")
    
    if addWhere == "Brewery" or addWhere == "brewery":
        br_name=raw_input("Enter Brewery Name: ")
        br_description=raw_input("Enter a Description: ")
        br_locationkey = random.randint(1,100)
        db_cursor.execute("INSERT INTO brewery(br_name, br_locationkey, br_description) VALUES(?,?,?)",(br_name, br_locationkey, br_description))
        db_connection.commit()
        restartProgram = raw_input("\nPress r to restart || Press e to exit \n> ")
        if restartProgram == "r":
            Menu()
        elif restartProgram == "e":
            quit()

    elif addWhere == "Winery" or addWhere == "winery":
        wi_name=raw_input("Enter Winery Name: ")
        wi_description=raw_input("Enter a Description: ")
        wi_locationkey = random.randint(1,100)
        db_cursor.execute("INSERT INTO Winery(wi_name, wi_locationkey, wi_description) VALUES(?,?,?,?,?,?)",(wi_name, wi_locationkey, wi_description))
        db_connection.commit()
        restartProgram = raw_input("\nPress r to restart || Press e to exit \n> ")
        if restartProgram == "r":
            Menu()
        elif restartProgram == "e":
            quit()

    elif addWhere == "Wine" or addWhere == "wine":
        w_name=raw_input("Enter wine Name: ")
        w_ABV=float(raw_input("Enter the ABV: "))
        w_typekey=int(raw_input("Enter a key: "))
        w_year=int(raw_input("Enter the year it was made: "))
        w_description=raw_input("Enter a description: ")
        db_cursor.execute("INSERT INTO wine(w_name, w_ABV, w_typekey, w_year, w_description) VALUES(?,?,?,?,?)",(w_name, w_ABV, w_typekey, w_year, w_description))
        db_connection.commit()
        restartProgram = raw_input("\nPress r to restart || Press e to exit \n> ")
        if restartProgram == "r":
            Menu()
        elif restartProgram == "e":
            quit()

    elif addWhere == "Beer" or addWhere == "beer":
        b_name=raw_input("Enter beer Name: ")
        b_ABV=float(raw_input("Enter the ABV: "))
        b_typekey=int(raw_input("Enter a key (1 = Ale | 2 = What Ale | 3 = Pilsner | 4 = Stout | 5 = Lager): "))
        b_IBU=float(raw_input("Enter the IBU: "))
        b_description=raw_input("Enter a description: ")
        db_cursor.execute("INSERT INTO beer(b_name, b_ABV, b_typekey, b_IBU, b_description) VALUES(?,?,?,?,?)",(b_name, b_ABV, b_typekey, b_IBU, b_description))
        db_connection.commit()
        print("\nSuccessfully Inserted")
        restartProgram = raw_input("\nPress r to restart || Press e to exit \n> ")
        if restartProgram == "r":
            Menu()
        elif restartProgram == "e":
            quit()


def query2():
    brewOrBlend=raw_input("What do you feel like drinking tonight? Enter beer or wine: ")
    
    if brewOrBlend == "beer" or brewOrBlend == "Beer":
        print("\n")
        style=raw_input("What style of beer would you like? \nEnter from the following: \nAle \nWheat Ale \nPilsner \nStout \nLager \n> ")
        print("\nBeers(Beer name, ABV level, IBU level) you might like: ")
        db_cursor.execute("SELECT b_name, b_ABV, b_IBU FROM beer, TypesOfAlcohol WHERE a_beertypename = \"" + style + "\" AND a_typekey = b_typekey GROUP BY b_name, b_ABV, b_IBU, b_description;")
        
        db_connection.commit()
        result = db_cursor.fetchall()
        for row in result:
            print (row[0], row[1], row[2])
    
        print("\n")
        drinkToFind = raw_input("If you would like to find locations where you can find a drink, please type in the drink name: \n> ")
        db_cursor.execute("SELECT l_name, l_address, l_phonenumber FROM location, foundat WHERE l_locationkey = f_locationkey AND f_beername LIKE'" + drinkToFind + "%';")
        print("\n")
        db_connection.commit()
        result = db_cursor.fetchall()
        print("Location:")
        for row in result:
            print (row[0], row[1], row[2])
        restartProgram = raw_input("\nPress r to restart || Press e to exit \n> ")
        if restartProgram == "r":
            Menu()
        elif restartProgram == "e":
            quit()

    elif brewOrBlend == "wine" or breworBlend == "Wine":
        print("\n")
        style = raw_input("What style of wine would you like? \nEnter from the following: \nPinot Noir \nSyrah \nCabernet Sauvigon \nRed Blend \nChardonnay \nZinfandel \nRose \n> ")
        print("\nWines(Wine Name, ABV level) you might like: ")
        db_cursor.execute("Select w_name, w_ABV FROM wine, TypesOfAlcohol WHERE a_winetypename = \"" + style + "\" AND a_typekey = w_typekey GROUP BY w_name;")
        
        db_connection.commit()
        result = db_cursor.fetchall()
        
        for row in result:
            print (row[0], row[1])
        
        print("\n")
        drinkToFind = raw_input("If you would like to find locations where you can find a drink, please type in the drink name \n> ")
        db_cursor.execute("SELECT l_name, l_address, l_phonenumber FROM location, foundat WHERE l_locationkey = f_locationkey AND f_winename LIKE '" + drinkToFind + "%';")
        print("\n")
        db_connection.commit()
        result = db_cursor.fetchall()
        print("Location:")
        for row in result:
            print (row[0], row[1], row[2])
        restartProgram = raw_input("\nPress r to restart || Press e to exit \n> ")
        if restartProgram == "r":
            Menu()
        elif restartProgram == "e":
            quit()

def query3():
    breweryOrWinery=raw_input("Brewery or Winery? \n>")
    
    if breweryOrWinery == "brewery" or breweryOrWinery == "Brewery":
        print("\n")
        db_cursor.execute("SELECT br_name FROM brewery;")
        db_connection.commit()
        result = db_cursor.fetchall()
        for row in result:
            print (row[0])
        
        userBrewery=raw_input("\nType in a brewery from the list above: ")
        print("\nBeers(Beer Name, ABV level, IBU level) you might like: ")
        db_cursor.execute("SELECT b_name, b_ABV, b_IBU FROM beer, brewery, foundat WHERE br_name LIKE '" + userBrewery + "%' AND b_name = f_beername AND br_locationkey = f_locationkey GROUP BY b_name;")
        
        db_connection.commit()
        result = db_cursor.fetchall()
        for row in result:
            print (row[0], row[1], row[2])

        drinkToFind = raw_input("\nIf you would like to find locations where you can find a drink, please type in the drink name \n> ")
        db_cursor.execute("SELECT l_name, l_address, l_phonenumber FROM location, foundat WHERE l_locationkey = f_locationkey AND f_beername LIKE '" + drinkToFind + "%';")
        print("\n")
        db_connection.commit()
        result = db_cursor.fetchall()
        print("Location:")
        for row in result:
            print (row[0], row[1], row[2])

        restartProgram = raw_input("\nPress r to restart || Press e to exit \n> ")
        if restartProgram == "r":
            Menu()
        elif restartProgram == "e":
            quit()

    elif breweryOrWinery == "Winery" or breweryOrWinery == "winery":
        print("\n")
        db_cursor.execute("SELECT wi_name FROM winery;")
        db_connection.commit()
        result = db_cursor.fetchall()
        for row in result:
            print (row[0])
        
        userWinery=raw_input("\nType in a winery from the list above: \n")
        print("\nWines(Wine Name, ABV level) you might like: ")
        db_cursor.execute("SELECT w_name, w_ABV FROM wine, winery, foundat WHERE wi_name LIKE '" + userWinery + "%' AND w_name = f_winename AND wi_locationkey = f_locationkey GROUP BY w_name;")
        
        db_connection.commit()
        result = db_cursor.fetchall()
        for row in result:
            print (row[0], row[1])

        drinkToFind = raw_input("\nIf you would like to find locations where you can find a drink, please type in the drink name \n> ")
        db_cursor.execute("SELECT l_name, l_address, l_phonenumber FROM location, foundat WHERE l_locationkey = f_locationkey AND f_winename LIKE '" + drinkToFind + "%';")
        print("\n")
        db_connection.commit()
        result = db_cursor.fetchall()
        print("Location:")
        for row in result:
            print (row[0], row[1], row[2])

        restartProgram = raw_input("\nPress r to restart || Press e to exit \n> ")
        if restartProgram == "r":
            Menu()
        elif restartProgram == "e":
            quit()


def Menu():
    intoBrewery = False
    intoBeer = False
    intoWinery = False
    intoWine = False
    
    addOrSearch=raw_input("Choose from the following commands: \nAdd(Enter 1) \nSearch by Types of Alcohol(Enter 2) \nSearch by Brewery or Winery(Enter 3) \n>")
    
    if addOrSearch == "1" :
        input_data()

    
    elif addOrSearch == "2" :
        query2()

    elif addOrSearch == "3" :
        query3()


Menu()
#input_data()
#db_cursor.execute(input1)

#result = db_cursor.fetchall()

#print("returned is a: ", type(result))

#print("############# Result ###############")
#for row in result:
#    print(row)

db_cursor.close()
db_connection.close()