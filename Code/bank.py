# 
# App Project : Bank Management System
# Author: L Fernandez (C20305696)
# Date: 18/12/2021
#
# Program Description:
# This program should reflect a simple Bank Management System in which includes
# services such as Balance, Deposit, Transfer and Withdrawal for two types 
# of accounts - Current and Savings.
#
# The Menu (UI) should present;
# [1] Create Account
#    (Note: 
#       Make a new profile in the system in which is saved unto customers.txt 
#       and back to menu.
#
#       This should include: name(f,l), date of birth, home address, email, number
#       and most importantly, customer identification number. 
#       Account identification number will also be included to link the customer 
#       to their account information.
#        
#       When option is chosen, this will open another menu option where user is
#       asked if they want to open Current Account (Note: Must be 18+ - error 
#       checking on date of birth.) or a Savings Account where transferral and
#       withdrawl services are capped once a month.
#    )
#
# [2] View Balance and Transaction History
#    (Note: 
#       This option should allow an existing customer to view their balance and
#       transaction history. 
#
#       Once clicking this option, user is asked to enter account number twice and
#       phone number to verify account. System will search account number
#       through customers.txt and if phone number provided by user is the same
#       on profile, balance and transaction history prints to user which is found on 
#       accounts.txt and accountsTransactions.txt, respectively.
#
#       Gracefully exits and returns to Main Menu.
#    )
#       
# [3] Account Services
#    (Note:
#       User is asked to verify account as mentioned in [2] option and opens services available to user;
#           [1] - Deposit
#               (Note:
#                   Add money into verified account user. Update balance and add a transaction action into 
#                   accountsTransaction.txt
#               )   
#       
#           [2] - Withdrawal
#               (Note:
#                   Minus money from verified account user.  
#                   Update balance and add a transaction action into accountsTransaction.txt
#               )
#
#           [3] - Transfer
#               (Note:
#                   Minus money from verified account user. Add money into the 2nd verified account where ID 
#                   is provided by user.
#                   Will hold two transactions reflecting above line - add and minus.
#               )
#
#       Gracefully exits and returns to Main Menu.
#    )
#
# [4] Delete Account
#    (Note:
#       When this option is chosen, all related information to the account number
#       of the user/account holder will be deleted.
#       
#       For security measurements, verification steps will be done in the same way
#       mentioned in [2] View Balance and Transaction History - Notes. In additional,
#       a last prompt message should appear where it asks for user's confirmation
#       of the deletion of their account including a warning message that all data 
#       will be erased and unretrievable. 
#       
#       Gracefully exits and returns to Main Menu.
#    )
#
#


# Library import
import string
import random
from datetime import datetime

import os

# Print the current working directory
print("Current working directory:", os.getcwd())

# If this is not the directory where customers.txt is located, change it
os.chdir('C:\\Users\\lovel\\Downloads\\bank_oop_project\\bank_oop_project\\Code')

# Continue with the rest of your script

# Files are to open first when application starts
def openFiles():
    # opens customer.txt and inputs data into customers array which contains their data
    with open("customers.txt") as file:
        for line in file:
            data = line.split(" | ")
            customers.append(Customers(data[0], data[1], data[2], data[3], int(data[4]), data[5], data[6]))

    # opens accounts.txt and inputs data into customers array which contains their data
    with open("accounts.txt") as file:
        for line in file:
            data = line.split(" | ")
            if data[1] == 'Savings Account':
                accounts.append(savingsAccount(data[0], data[1], int(data[2])))
            else:
                accounts.append(currentAccount(data[0], data[1], int(data[2])))


# ID_GENERATOR START
def customerID():
    return 'C' + ''.join(random.choices(string.digits, k=7))


def accSavingsID():
    return 'AS' + ''.join(random.choices(string.digits, k=6))


def accCurrentID():
    return 'AC' + ''.join(random.choices(string.digits, k=6))


def transactionID():
    return 'T' + ''.join(random.choices(string.digits, k=9))


# ID_GENERATOR END

# CLASSES START 
# ref: https://www.youtube.com/watch?v=ZDa-Z5JzLYM
# ref: https://stackoverflow.com/questions/35571552/python-2-7-classes-user-input-birthdates-for-later-use
class Customers():
    # define structure
    def __init__(self, firstN, lastN, dob, address, number, customerID, accountID):
        self.firstN = firstN
        self.lastN = lastN
        self.full = self.firstN + " " + self.lastN
        self.dob = dob
        self.address = address
        self.number = number
        self.customerID = customerID
        self.accountID = accountID

    def __str__(self):
        return f"\nName: {self.firstN} {self.lastN} \nDate of Birth: {self.dob} \nAddress: {self.address} \nNumber: {self.number} \nPersonal ID: {self.customerID} \nAccount Number: {self.accountID}"


# ref: https://www.youtube.com/watch?v=RSl87lqOXDE
class Account:
    def __init__(self, accountID, type_):
        self.accountID = accountID
        self.type_ = type_

    # Add amount deposited into balance and print new balance
    def deposit(self):

        amount = int(input("\nEnter Deposit Amount: "))
        self.balance += amount
        print(f"Your new balance is: {self.balance}")
        updateAccs()
        current = [datetime.now().month, datetime.now().year]

        with open('accountsTransactions.txt', 'a') as file:
            file.write(self.accountID + ' | ' + 'DEPOSIT' + ' | ' + str(amount) + ' | ' + transactionID() + ' | ' + str(
                current[0]) + '-' + str(current[1]) + '\n')

    # Minus amount withdrawed from balance and print new balance
    def withdrawal(self):

        # limits Savings account from withdrawing once per month
        current = str(datetime.now().month) + '-' + str(datetime.now().year)
        with open('accountsTransactions.txt') as file:
            for line in file:
                data = line.split(' | ')
                if data[0] == self.accountID and data[0][1] == 'S':
                    if data[4].rstrip('\n') == current and data[1] == 'WITHDRAWAL':
                        print(f"You have hit your withdrawal limit for this month.")
                        return menu()

        amount = int(input("\nEnter Withdrawal Amount: "))

        # If Current Account reaches credit limit of 500, do not allow any further withdrawals.
        # If Savings is <= 0, no withdrawals allowed.
        if (self.balance - amount) <= 0:
            if self.type_ == 'Current Account':
                if (self.balance - amount < -500):
                    print("\nYou have hit your credit limit")
                    return menu()
            else:
                print(
                    "\nNot enough sufficient funds, you have reached your credit limit of 500. \nReturning to Main Menu")
                return menu()

        self.balance -= amount

        print(f"Your new balance is: {self.balance}")
        updateAccs()

        with open('accountsTransactions.txt', 'a') as file:
            file.write(self.accountID + ' | ' + 'WITHDRAWAL' + ' | ' + str(
                amount) + ' | ' + transactionID() + ' | ' + current + '\n')

    # Transfers money to another account within the system (deposit and withdrawal)
    def transfer(self):
        # Another limit for Savings account - once per month
        current = str(datetime.now().month) + '-' + str(datetime.now().year)
        with open('accountsTransactions.txt') as file:
            for line in file:
                data = line.split(' | ')
                if data[0] == self.accountID and data[0][1] == 'S':
                    if data[4].rstrip('\n') == current and data[1] == 'TRANSFER':
                        print(f"You have hit your transfer limit for this month.")
                        return menu()

        sendTo = input("\nEnter the account number to send to: ")
        exists = False
        with open('accounts.txt') as file:
            for line in file:
                data = line.split(' | ')
                if data[0] == sendTo:
                    exists = True
                    break
                else:
                    print("Unable to find the account. Please Try again. \nReturning to Main Menu")

                    return menu()

        if exists == True:
            j = 0
            for j in range(0, len(accounts)):
                if accounts[j].accountID == sendTo:
                    break

            amount = int(input(f"Enter the amount to transfer to {sendTo}: "))

            # Transferral Process
            self.balance -= amount
            accounts[j].balance += amount

            updateAccs()

            with open('accountsTransactions.txt', 'a') as file:
                file.write(self.accountID + ' | ' + 'TRANSFER' + ' | ' + str(
                    amount) + ' | ' + transactionID() + ' | ' + current + '\n')
        else:
            print("\nAccount not found. \nReturning to Main Menu")
            return menu()


# Sub classes of Account Class
class savingsAccount(Account):
    type_ = "Savings"

    def __init__(self, accountID, type_, balance):
        super().__init__(accountID, type_)  # Inherits instances from parent: Account
        self.balance = balance

    def __str__(self):
        return f"\nAccount ID: {self.accountID} \nAccount Type: {self.type_} \nAccount Balance: {self.balance}"


# Sub classes of Account Class
class currentAccount(Account):
    type_ = "Current"

    def __init__(self, accountID, type_, balance):
        super().__init__(accountID, type_)  # Inherits instances from parent: Account
        self.balance = balance

    def __str__(self):
        return f"\nAccount ID: {self.accountID} \nAccount Type: {self.type_} \nAccount Balance: {self.balance}"


# CLASSES END

# FUNCTIONS
# Checks if user is over the age of 14 to create Savings Account
def ageSavLimit(birth_year):
    current = datetime.now().year
    age = current - int(birth_year)

    if age >= 14:
        return True
    else:
        return False


# Checks if user is over the age of 18 to create Current Account
def ageCurrLimit(birth_year):
    current = datetime.now().year
    age = current - int(birth_year)

    if age >= 18:
        return True
    else:
        return False


# Verification of user's account information in order to user services
def logIn():
    account_1 = input("\nEnter Account ID: ")
    account_2 = input("Re-enter Account ID: ")

    # Compare if both inputs are correct
    if account_1 == account_2:
        # Initialise variables
        found = False
        i = 0

        # loop through customers and find matching account ID
        for i in customers:
            if i.accountID.rstrip('\n') == account_1:
                found = True
                break

        if found == False:
            print("\nAccount not found, returning to Main Menu.")
            return menu()

        phone = int(input("\nVerification neeeded \nEnter Phone Number: "))

        # Initialise variables and puts found back to False
        found = False
        j = 0
      
        for j in customers:
            if j.number == phone:
                found = True
                break

        if found == False:
            print("\nPhone number incorrect, unable to verify account. \nReturning to Menu.")
            return menu()
        else:
            print("\nAccount Verified.")
            return i.accountID

    else:
        print("\nAccount ID incorrect, returning to Menu.")
        return menu()


# Updates the database(texts) from any amendmends within the system
def updateAccs():
    with open('accounts.txt', 'w') as file:
        for i in accounts:
            Write = i.accountID + ' | ' + i.type_ + ' | ' + str(i.balance) + '\n'
            file.write(Write)


# FUNCTIONS END

# OPERATIONS MENU START
# Create account by asking user relevent info as structed in Customers Class
# Save data into customers.txt after confirming details with user
def createAcc():
    while True:
        # Customer Name
        while True:
            print("\nPlease enter your full name.")
            first = input("First Name: ")
            last = input("Last Name: ")

            check = int(input(f"\nYou have entered '{first} {last}', is this correct? \n[1] Yes \n[2] No\n"))

            if check == 1:
                break
            else:
                print("\nInformation not saved. Please try again.")

        # Customer Date of Birth
        while True:
            print("\nPlease enter your date of birth. (DD/MM/YYYY)")
            day = input('DD: ')
            month = input('MM: ')
            year = input('YYYY: ')

            check = int(input(f"\nYou have entered '{day}-{month}-{year}', is this correct? \n[1] Yes \n[2] No\n"))

            if check == 1:
                break
            else:
                print("\nInformation not saved. Please try again.")

        # Customer Address
        while True:
            print("\nPlease enter your address.")
            address = input()

            check = int(input(f"\nYou have entered '{address}', is this correct? \n[1] Yes \n[2] No\n"))

            if check == 1:
                break
            else:
                print("\nInformation not saved. Please try again.")

        # Customer Number
        while True:
            print("\nPlease enter your phone number.")
            number = input()

            check = int(input(f"\nYou have entered '{number}', is this correct? \n[1] Yes \n[2] No\n"))

            if check == 1:
                break
            else:
                print("\nInformation not saved. Please try again.")

        # Reconfirming details with user
        print("\nPlease check if all your details are correct")
        print(
            f"Name: {first} {last} \nDate of Birth: {day}-{month}-{year} \nAddress: {address} \nPhone number: {number}")
        check = int(input("\nIs this correct? \n[1] Yes \n[2] No \n[Any Key] Return to Main Menu\n"))

        if check == 1:
            break
        elif check == 2:
            print("\nInformation not saved. Please try again.")
        else:
            return menu()

    # Generate ID for customer
    custID = customerID()

    while True:
        while True:
            # Account Type Choice
            print("\nWould you like to create a Current Account or Savings Account?")
            check = int(input("\n[1] Current Account \n[2] Savings Account\n"))

            # Generate ID for Account
            if check == 1:
                # Check if customer is above 18
                ageCheck = ageCurrLimit(year)
                if ageCheck == True:
                    choice = 'Current Account'
                    accID = accCurrentID()
                    break
                else:
                    print("\nUnable to make Current Account. \nMust be over 18 years of age. \nReturning to Main Menu.")
                    return menu()

            elif check == 2:
                # Check if customer is above 14
                ageCheck = ageSavLimit(year)
                if ageCheck == True:
                    choice = 'Savings Account'
                    accID = accSavingsID()
                    break
                else:
                    print("\nUnable to make Savings Account. \nMust be over 14 years of age. \nReturning to Main Menu.")
                    return menu()

            else:
                print("\nPlease try again.")

        check = int(input(f"\nYou have entered '{choice}', is this correct? \n[1] Yes \n[2] No\n"))

        if check == 1:
            break
        else:
            print("\nInformation not saved. Please try again.")

    # Making data into string to save into txt files (customers and accounts)
    custData = first + ' | ' + last + ' | ' + day + '-' + month + '-' + year + ' | ' + address + ' | ' + number + ' | ' + custID + ' | ' + accID + '\n'
    accData = accID + ' | ' + choice + ' | ' + '0' + '\n'

    # Open file and append information in the txt files (customers and accounts)
    with open('customers.txt', 'a') as file1, open('accounts.txt', 'a') as file2:
        file1.write(custData)
        file2.write(accData)

    # Let Customer know account has been created
    print("\n**Account has been created**")
    print(f"Name: {first} {last} \nAccount Number: {accID}")

    # Updates text files when account is created
    customers.append(Customers(first, last, day + '-' + month + '-' + year, address, number, custID, accID))

    # Choice of which account to create
    if choice == 'Savings Account':
        accounts.append(savingsAccount(accID, choice, 0))
    else:
        accounts.append(currentAccount(accID, choice, 0))

    return menu()


# Display transaction history with balance
def viewBalTrans():
    accID = logIn()
    j = 0
    for j in range(0, len(accounts)):
        if accounts[j].accountID == accID.rstrip('\n'):
            break

    print(f"\nYour balance is: €{accounts[j].balance}")
    print("And your transaction history is:")

    with open('accountsTransactions.txt') as file:
        for line in file:
            data = line.split(' | ')
            if data[0] == accID.rstrip('\n'):
                print(line)

    return menu()


# Open options of services, Deposit, Withdrawal and Transfer
def accServices():
    accLocation = logIn()
    j = 0
    for j in range(0, len(accounts)):
        if accounts[j].accountID == accLocation.rstrip('\n'):
            break

    # Loop Menu.
    while True:
        # resets user_input to catch any errors that may enter menu
        user_input = 0

        # Ask user for input - save into user_input variable.
        print("\n - - - - - - - - - - - - - - - - - - - - - \n")
        user_input = input(
            "<< Account Services >> \n[1] Deposit \n[2] Withdrawal \n[3] Transfer \n[4] Return to Main Menu\n\n")

        # Error Checking: If input was not valid - may be lesser/greater input or a character.
        try:
            if int(user_input) >= 1 and int(user_input) <= 4:

                # lists menu options in an array following menu format and run function that has been called.
                # Operations listed in Account Class methods
                ver_operations = [accounts[j].deposit, accounts[j].withdrawal, accounts[j].transfer, menu]
                ver_operations[int(user_input) - 1]()

                break;
            else:
                print("Invalid Option, try again.")
        except ValueError:
            print("Invalid Option, try again.")

    return menu()


# Deletes all data but transaction history of anything relating to the account
def deleteAcc():
    # log in verification
    verify = logIn()

    print("\nWARNING: Deletion of account will erase all data and will not be retrievable.")

    account = input("\nConfirm the Account ID to be deleted: ")

    if verify.rstrip('\n') == account:
        print("\nAccount has been successfuly deleted.")

        j = 0
        for j in range(0, len(accounts)):
            if accounts[j].accountID == verify.rstrip('\n'):
                break

        i = 0
        for i in range(0, len(customers)):
            if customers[i].accountID == verify:
                break

        # Update the text files to remove account
        with open('customers.txt', 'r') as file:
            lines = file.readlines()
        with open('customers.txt', 'w') as file:
            for line in lines:
                data = line.split(' | ')
                if data[6] != verify:
                    file.write(line)

        with open('accounts.txt', 'r') as file:
            lines = file.readlines()
        with open('accounts.txt', 'w') as file:
            for line in lines:
                data = line.split(' | ')
                if data[0] != verify.rstrip('\n'):
                    file.write(line)

        # Remove the element from location i/j within the array
        accounts.pop(j)
        customers.pop(i)

    else:
        print("\nUnable to delete account, please try again. \nReturning to Main Menu.")

    return menu()


# OPERATIONS MENU END

# MENU START: [1] to [4] options mentioned in description.
def menu():
    # Loop Menu.
    while True:
        # resets user_input to catch any errors that may enter menu
        user_input = 0

        # Ask user for input - save into user_input variable.
        print("\n - - - - - - - - - - - - - - - - - - - - - \n")
        user_input = input(
            "<< Main Menu >> \n[1] Create Account \n[2] View Balance and Transaction History \n[3] Account Services \n[4] Delete Account\n\n")

        # Error Checking: If input was not valid - may be lesser/greater input or a character.
        try:
            if int(user_input) >= 1 and int(user_input) <= 4:
                # print("It works, you pressed " + user_input)

                # lists menu options in an array following menu format and run function that has been called.
                # Refer to # OPERATIONS section
                menu_operations = [createAcc, viewBalTrans, accServices, deleteAcc]
                menu_operations[int(user_input) - 1]()

                break;
            else:
                print("\nInvalid Option, try again.")
        except ValueError:
            print("\nTry again.")


# MENU END

# PROGRAM START
# Local Variables
customers = []
accounts = []

openFiles()  # open files
menu()  # displays menu

# PROGRAM END