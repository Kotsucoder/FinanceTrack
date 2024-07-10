# Boilerplate feature for program to function
from sys import argv
import csv
import json
import os
saveLoc = 'data/'

# Commands:
# add income category amount description
# add expense category amount description
# add category name description
# list categories
# list commands
# total income
# total expenses
# total profit
# remove income id
# remove expense id
# set-budget
# set-save ***
# help command
# init save-location ***

def setSave(location = 'data/'):
    """
    Sets the current save location. Creates directory if it does not yet exist.

    Args:
        location (str: 'data/'): Path to the desired save location. Defaults to 'data/' if not set.

    Returns:
        None
    """
    global saveLoc
    if location[-1] != '/':
        location = location + '/'
    dataSource = open('saveloc.bills', 'w')
    dataSource.write(location)
    saveLoc = location
    dataSource.close()
    if not os.path.exists(location):
        os.makedirs(location)


def openFile(filename, rw):
    """
    Opens the given file at the current save location.

    Requirement:
        Global variable saveLoc must be set.

    Args:
        filename (str): Name of the file to open.
        rw (str): Mode to open the file. Supports all modes supported by open() function.

    Returns:
        I/O Datastream for opened file.
    """
    return open(f'{saveLoc}{filename}', rw)

def checkInitFile():
    """
    Checks for the init.bills file in current location.

    Returns:
        bool: True if file exists, False if file does not exist.
    """
    try:
        initFile = openFile('init.bills', 'r')
        return True
    except:
        return False

def initProcess():
    """
    Prepares the main files that FinanceTrack operates with.

    Files Created:
        categories.bills (txt): Contains categories that can be used for income and expenses.  
        income.bills (csv): Contains all income data. Initialized with headers.  
        expense.bills (csv): Contains all expense data. Initialized with headers.  

    Returns:
        bool: True if successful, False if process failed.
    """
    try:
        categories = ['Bills\n', 'Auto\n', 'Groceries\n', 'Medical\n', 'Loans\n', 'Subscriptions\n']
        catFile = openFile('categories.bills', 'w')
        catFile.writelines(categories)
        catFile.close()
    except:
        return False

    try:
        incomeFile = openFile('income.bills', 'w')
        incomeWriter = csv.writer(incomeFile)
        incomeWriter.writerow(["id", "date", "category", "amount", "description"])
        incomeFile.close()
    except:
        return False

    try:
        expenseFile = openFile('expense.bills', 'w')
        expenseWriter = csv.writer(expenseFile)
        expenseWriter.writerow(["id", "date", "category", "amount", "description"])
        expenseFile.close()
    except:
        return False

    return True

def init(save_location = None):
    """
    Initializes the program in the current save location. Also sets save location if specified.

    Args:
        save_location (str): Path to the desired save location. Optional.

    Returns:
        bool: True if successful, False if process failed.
    """
    initSuccess = False
    if save_location:
        setSave(save_location)

    openSuccess = checkInitFile()

    if openSuccess:
        question = input("This program has already been initialized. Are you sure you'd like to continue? All existing data will be lost.\nType 'Yes' to confirm: ")
        if question == 'Yes':
            initSuccess = initProcess()
        else:
            initSuccess = True
    else:
        initSuccess = initProcess()
        initFile = openFile('init.bills', 'w')
        initFile.close()

    return initSuccess

def add_income(category, amount, description):
    pass

def add_expense(category, amount, description):
    pass

def add_category(category, description):
    pass

if __name__ == '__main__':
    # Determines the current save location, sets to default if saveloc.bills doesn't exist.
    try:
        dataSource = open('saveloc.bills', 'r')
        saveLoc = dataSource.read()
        dataSource.close()
    except:
        setSave()

    # Grabs the current command.
    try:
        command = argv[1]
    except:
        command = None

    # Grabs any command attribute.
    try:
        testArgv = argv[2]
        attribute = argv[2:]
    except:
        attribute = [None]


    # Runs the command
    match command:
        case 'init':
            init(attribute[0])

        case 'set-save':
            if attribute[0] == None:
                print("Warning: Save location will be set to the default. Is this what you want to do? (Y/N)")
                setDefault = input("> ")
                if setDefault == "Y":
                    attribute[0] = 'data/'
                else:
                    attribute[0] = saveLoc
            setSave(attribute[0])

        case 'add':
            good = True
            validTypes = ['income', 'expense', 'category']

            if good:
                try:
                    type = attribute[0]
                    category = attribute[1]
                    description = attribute[3]
                except:
                    print("Please enter all required attributes.")
                    print("Required Attributes:\n\tType (Income, Expense, Category)\n\tCategory\n\tAmount (Except if adding Category)\n\tDescription")
                    good = False

            if good and type not in validTypes:
                print("Please enter a valid option for Type.\nValid options are:\n\tIncome\n\tExpense\n\tCategory")
                good = False

            if good and type is not 'category':
                try:
                    amount = float(attribute[2])
                except:
                    print("Amount must be a number.")
                    good = False

            if good:
                match type:
                    case 'income':
                        add_income(category, amount, description)
                    case 'expense':
                        add_expense(category, amount, description)
                    case 'category':
                        add_category(category, description)
                        
        case None:
            print("Please enter an argument in the command line.")

        case _:
            print("Invalid command. Use 'list commands' to see list of commands. Use 'help' to learn more about a command.")