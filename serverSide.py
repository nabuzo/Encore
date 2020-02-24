
# Authors: Jaelyn Fladger, Nicole Abuzo, Kodie Philips, Joseph Ankebrant, Alejandro Huerta
# Date: November 11, 2019
# Description: A ticket purchasing program name Encore. Simple program that is vulnerable from attacks.

import socket
import hashlib
import time
import random
from datetime import date
import sqlite3
from sqlite3 import Error

#--- MESSAGES ---
menu1 = '\n1: Log In\n2: Register\n3: Quit\n\n What would you like to do? \n'
menu2 = '\n1: View Concerts\n2: User Information\n3: Log Out ' 
menu3 = '\n What type of concert are you looking for?\n\n1: Pop\n2: Rock\n3: Rap\n4: Country\n5: Indie\n6: Electronic\n7: All\n8: Back' 
invalid = '\n Please enter valid option'
concertsMenu = '\n\n1: Purchase\n2: Back'
userInfoMenu = '\n1: Order History\n2: Add Points\n3: Back'
purchaseAttempt = '\n Enter concert ID of concert you wish to purchase tickets to: '
request = 'respond'
closing = 'closing'

def UserInfoHeader(cursor, currentUser):
    header = '\n' + getFirstName(cursor, currentUser) + " " + getLastName(cursor, currentUser) + "\t\tPoints: " + str(getPoints(cursor, currentUser))
    return header
#----------------

#----------------
genres = ["Pop", "Rock", "Rap", "Country", "Indie", "Electronic"]
#----------------

#- Request Response -
def requestResponse(connection):
    time.sleep(.3)
    connection.sendall(request.encode())
    response = connection.recv(400)
    return response.decode()
#--------------------

#--- DATABASE ---
def removeAllOrders(cursor):
    sql = ''' DELETE FROM ORDERS '''
    cursor.execute(sql)
    conn.commit()   

def register(cursor, connection): # Still have to check lengths of user input before using, boo.
    while True:
        message = ("Enter first name: ")
        connection.sendall(message.encode())
        FirstName = requestResponse(connection)
        if (len(FirstName) > 26):
            message = '\n The first name entered is too long\n'
            connection.sendall(message.encode())
        elif (len(FirstName) <= 2):
            message = '\n The first name entered is not long enough\n'
            connection.sendall(message.encode())
        else:
            break
    while True:
        message = ("Enter last name: ")
        connection.sendall(message.encode())
        LastName = requestResponse(connection)
        if (len(LastName) > 26):
            message = '\n The last name entered is too long\n'
            connection.sendall(message.encode())
        elif (len(LastName) <= 2):
            message = '\n The last name entered is not long enough\n'
            connection.sendall(message.encode())
        else:
            break
    while True:
        message = ("Enter username (5-12 characters): ")
        connection.sendall(message.encode())
        username = requestResponse(connection)
        if (len(username) > 12):
            message = '\nThe username entered is too long\n'
            connection.sendall(message.encode())
        elif (len(username) <= 5):
            message = '\nThe username entered is not long enough\n'
            connection.sendall(message.encode())
        else:
            break
    while True:
        message = ("Enter password (minimum 8 characters): ")
        connection.sendall(message.encode())
        password = requestResponse(connection)
        if (len(password) > 20):
            message = '\n The password entered is too long\n'
            connection.sendall(message.encode())
        elif (len(password) < 8):
            message = '\n The password entered is not long enough\n'
            connection.sendall(message.encode())
        else:
            password = str(hashlib.sha1(password.encode()).hexdigest())
            break
    user = (FirstName, LastName, username, password) 
    try:
        sql = ''' INSERT INTO USER(FirstName, LastName, UserName, password, Points)
                    VALUES(?,?,?,?,700) '''
        cursor.execute(sql, user)
        conn.commit()
    except Error as e:
        print(e)
        message = "\n Registration failed"
        connection.sendall(message.encode())
    else:
        message = "\n Registration successful, please log in"
        connection.sendall(message.encode())
        
def logIn(cursor, connection):
    message = ("Enter username: ")
    connection.sendall(message.encode())
    username = requestResponse(connection)
    message = ("Enter password: ")
    connection.sendall(message.encode())
    password = requestResponse(connection)
    password = str(hashlib.sha1(password.encode()).hexdigest())
    login = (username, password)
    try:
        sql = ''' SELECT EXISTS(SELECT 1 FROM USER WHERE username=? and password=?) '''
        
        cursor.execute(sql, login)
        user_exists, = cursor.fetchone()
        if (user_exists == 1):
            print ("login accepted")                                
        else:
            print ("login denied")
            username = None 
        return username
    except Error as e:
        username = None


def displayAllConcerts(cursor, connection):
    #return all_concerts that have at least 1 ticket avaliable 
    cursor.execute("SELECT * FROM CONCERT WHERE NOT TicketAvaliable=0")
    all_concerts = cursor.fetchall()
    message = '\nID\tCONCERT\t\tARTIST\t\tDATE\t\tPRICE\tLOCATION\tAVALIABILITY\tGENRE'
    connection.sendall(message.encode())
    message = ""
    for row in all_concerts:
        message += ('\n{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t\t{7}\n'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        message += ('-----------------------------------------------------------------------------------------------------------')
    return message
        
def displayGenre(cursor, genre, connection):
    sql = ''' SELECT ConcertID,ConcertName,ConcertArtist,ConcertDate,ConcertPrice,ConcertLocation,TicketAvaliable FROM CONCERT WHERE Genre=? '''
    cursor.execute(sql, (genre,))
    concerts = cursor.fetchall()
    message = '\nID\tCONCERT\t\tARTIST\t\tDATE\t\tPRICE\tLOCATION\tAVALIABILITY'
    connection.sendall(message.encode())
    message = ""
    for row in concerts:
        message += ('\n{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        message += ('--------------------------------------------------------------------------------------------')
    return message

def purchase(cursor, currentUser, connection):  
    while True:
        connection.sendall(purchaseAttempt.encode())
        concertID = requestResponse(connection)
        if concertID.isdigit() != True:
            connection.sendall(invalid.encode())  
        else:       
            # Select Tickets Avaliable 
            sql = ''' SELECT TicketAvaliable FROM CONCERT WHERE ConcertID=? '''
            cursor.execute(sql, (concertID,))
            tickets = cursor.fetchall()
            for row in tickets:
                tickets = row[0]
            if str(tickets) == '[]': # make sure concert exists
                message = ("\n Concert not found.")
                connection.sendall(message.encode())
            elif tickets == 0:
                message = "\n This show is sold out!"
                connection.sendall(message.encode())
            else:
                while True:
                    message = "\n How many tickets would you like to purchase?" #VULNERABILITY: Does not check that an integer is entered
                    connection.sendall(message.encode())
                    numTickets = int(requestResponse(connection))
                    if (tickets - numTickets < 0):                 
                        message = "\n There aren't enough tickets for you to buy this many!"
                        connection.sendall(message.encode())
                    else:
                        break
                if (numTickets > 0): 
                    # Select price
                    sql = ''' SELECT ConcertPrice FROM CONCERT WHERE ConcertID=? '''
                    cursor.execute(sql, (concertID,))
                    concertPrice = cursor.fetchall()
                    for row in concertPrice:
                        concertPrice = row[0]
                    concertPrice = concertPrice * numTickets
                    # Select user's points
                    sql = ''' SELECT Points FROM USER WHERE username=? '''
                    cursor.execute(sql, (currentUser,))
                    userPoints = cursor.fetchall()
                    for row in userPoints:
                        userPoints = row[0]        
                    # create new order if user can afford     
                    newUserPoints = userPoints - concertPrice
                    if (newUserPoints >= 0):
                        subPoints(cursor, concertPrice, currentUser)    
                        addOrder(cursor, (currentUser, concertID, 1, concertPrice, date.today().strftime("%m/%d/%Y")))
                        # Decrease number of tickets avaliable for concert
                        sql = ''' SELECT TicketAvaliable FROM CONCERT WHERE ConcertID=? '''
                        cursor.execute(sql, (concertID,))
                        message = '\n Purchase successfull'
                        connection.sendall(message.encode()) 
                        ticketsAvaliable = cursor.fetchall()
                        for row in ticketsAvaliable:
                            ticketsAvaliable = row[0]
                            ticketsAvaliable = ticketsAvaliable - 1  
                            update = (ticketsAvaliable, concertID)
                            sql = ''' UPDATE CONCERT SET TicketAvaliable=? WHERE ConcertID=? '''
                            cursor.execute(sql, update)
                            conn.commit()
                    else:
                        message = "\n You cannot afford this!"         #*Should also let them know if purchase successful*
                        connection.sendall(message.encode())
                break

def addPoints(cursor, pointsToAdd, currentUser):         
        test = (currentUser,)
        sql = ''' SELECT Points From USER WHERE username=? ''' 
        cursor.execute(sql, test)
        currentPoints = cursor.fetchall()
        for row in currentPoints:
            currentPoints = row[0]
        newPoints = currentPoints + pointsToAdd    
        updatePoints(cursor, newPoints, currentUser)
        
def subPoints(cursor, pointsToSub, currentUser):
        test = (currentUser,)
        sql = ''' SELECT Points FROM USER WHERE username=? '''
        cursor.execute(sql, test)
        currentPoints = cursor.fetchall()
        for row in currentPoints:
            currentPoints = row[0]
        updatedPoints = currentPoints - pointsToSub
        updatePoints(cursor, updatedPoints, currentUser)

def updatePoints(cursor, points, currentUser): 
        updateInfo = (points, currentUser)
        sql = ''' UPDATE USER SET points=? WHERE username=? '''
        cursor.execute(sql, updateInfo)
        conn.commit()

def getPoints(cursor, currentUser):
    sql = ''' SELECT Points From USER WHERE username=? ''' 
    cursor.execute(sql, (currentUser,))
    currentPoints = cursor.fetchall()
    for row in currentPoints:
        currentPoints = row[0]
    return currentPoints

def getFirstName(cursor, currentUser):
    sql = ''' SELECT FirstName From USER WHERE username=? '''
    cursor.execute(sql, (currentUser,))
    firstName = cursor.fetchall()
    for row in firstName:
        firstName = row[0]
    return firstName

def getLastName(cursor, currentUser):
    sql = ''' SELECT LastName From USER WHERE username=? '''
    cursor.execute(sql, (currentUser,))
    lastName = cursor.fetchall()
    for row in lastName:
        lastName = row[0]
    return lastName

def addOrder(cursor, order):
    try:
        sql = ''' INSERT INTO ORDERS(username,ConcertID,Quantity,Price,OrderDate)
                    VALUES(?,?,?,?,?) '''
        cursor.execute(sql, order)
        conn.commit()
    except Error as e:
        message = 'An error has occured.'
        connection.sendall(message.encode())
        print(e, '')

def orderHistory(cursor, currentUser):
    sql = ''' SELECT OrderID, ConcertID, Quantity, Price, OrderDate FROM ORDERS WHERE username=? '''
    cursor.execute(sql, (currentUser,))
    row = cursor.fetchall()
    message = "\nORDER ID\tCONCERT ID\tQUANTITY\tPRICE\tDATE PUCHASED\n"
    for row in row:
        message += ('{0}\t\t{1}\t\t{2}\t\t{3}\t{4}\n'.format(row[0],row[1],row[2],row[3],row[4]))
    return message
#----------------
def mathProblem(connection):
    rand_value1 = random.randint(0,100)
    rand_value2 = random.randint(0,100)
    total_value = rand_value1 + rand_value2
    while True:
        message = (str(rand_value1) +"+" + str(rand_value2) + "\n What's the sum of the two numbers?")
        connection.sendall(message.encode())
        userInput = requestResponse(connection)
        if userInput.isdigit():
            userInput = int(userInput)
            break;
        else:
            message = "\n Please enter an integer"
            connection.sendall(message.encode())   
    if userInput != total_value:
         message = ("\n Wrong answer\n No points added")
         connection.sendall(message.encode())
    if userInput == total_value:        
         addPoints(cursor, 50, currentUser)
         message = ("\n Congrats!\n Points have been added!")
         connection.sendall(message.encode())
#----------------


#--- Start -------------------------------------------------

#-- Database Connection --        
sqlite_file = "project2.sqlite"
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()
#-------------------------

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10001)                   
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Wait for a connection
connection, client_address = sock.accept()

message = 'Welcome to Encore!\n'
connection.sendall(message.encode())

userInput = "start"
#--- Send Menu1 ----
while userInput != '3':
    connection.sendall(menu1.encode())
    userInput = requestResponse(connection)

    if userInput == '1':    #LOGIN
        currentUser = logIn(cursor, connection)
        if currentUser != None: 
            message = "\n log in successfull\n"
            connection.sendall(message.encode())
            #--- Send Menu2 ---->    (Concerts/UserInfo/LogOut)         
            userInput2 = "start"
            while userInput2 != '3':
                connection.sendall(menu2.encode())
                userInput2 = requestResponse(connection)
                if userInput2 == '1': 
                    #--- Send Menu3 ---->   (Genres/Back)                  
                    userInput3 = 'start'
                    while userInput3 != '8':
                        connection.sendall(menu3.encode())
                        userInput3 = requestResponse(connection)
                        if userInput3.isdigit():
                            choice = int(userInput3)
                            if choice <= 7 and choice > 0:  #Display genre selected                                                
                                if choice == 7:
                                    message = displayAllConcerts(cursor, connection)
                                else:                       #Display all conerts
                                    message = displayGenre(cursor, genres[choice-1], connection)
                                connection.sendall(message.encode())
                                #--- Send ConcertsMenu ----> (Purchase/Back)
                                userInput4 = "start"
                                while userInput != '2':
                                    connection.sendall(concertsMenu.encode())
                                    userInput4 = requestResponse(connection)
                                    if userInput4 == '1':   #Purchase Attempt
                                        purchase(cursor, currentUser, connection)
                                        break
                                    if userInput4 == '2':   #Back -> to Menu3
                                        break;
                                    else:
                                        connection.sendall(invalid.encode())
                            elif userInput3 == '8':         #Back -> to Menu2
                                break                                                                                                                          
                        else:
                            connection.sendall(invalid.encode())
                        
                elif userInput2 == '2':
                    #--- Send User Info Menu -> (Order History/Add Points)
                    userInput5 = 'start'
                    while userInput5 != '3':
                        message = UserInfoHeader(cursor,currentUser)
                        connection.sendall(message.encode()) 
                        connection.sendall(userInfoMenu.encode())
                        userInput5 = requestResponse(connection)
                        if userInput5 == '1':   #Order History
                            message = orderHistory(cursor, currentUser)
                            connection.sendall(message.encode())
                        elif userInput5 == '2': #Add Points 
                            message = mathProblem(connection)
                        elif userInput5 == '3': #Back -> to Menu2
                            break
                        else:
                            connection.sendall(invalid.encode())
                            
                elif userInput2 == '3':   #Back -> to Menu1
                    currentUser = None
                    break
                else:
                    connection.sendall(invalid.encode())
        else:
            message = "\n log in denied\n"
            connection.sendall(message.encode())
    elif userInput == '2': # Registration 
        register(cursor, connection)
    elif userInput == '3': # Close Connection, program ends.
        connection.sendall(closing.encode())
        connection.close()
    else:
        connection.sendall(invalid.encode())        
