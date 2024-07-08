# Boilerplate feature for program to function
from sys import argv
import csv
import os
saveLoc = 'data/'

# Commands:
# add-income category amount description
# add-expense category amount description
# add-category name description
# list categories
# list commands
# total income
# total expenses
# total profit
# set-budget
# set-save ***
# help command
# init save-location ***

#----------------------------------------------------------------------------------------
# This portion collects the current save location, commands, and attributes.

def setSave(location = 'data/'):
    """
    User command to set the current save location.\n
    Will set to the default 'data/' if location attribute is not set.\n
    This function sets Global Variable saveLoc.
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
    print(argv[2])
    attribute = argv[2:]
except:
    attribute = [None]

#----------------------------------------------------------------------------------------

# Opens file in the current save location.
def openFile(filename, rw):
    """
    Opens the given file in the current save location.\n
    Requires the filename and rw attribute.\n
    rw attribute supports all the same modes as open(), but must be explicitly defined.\n
    Global Variable saveLoc must be set.
    """
    return open(f'{saveLoc}{filename}', rw)

def checkInitFile():
    """
    This function checks if the init file exists in the current save location.\n
    Returns true if the file exists, returns false if the file does not exist.\n
    Global Variable saveLoc must be set.
    """
    try:
        initFile = openFile('init.bills', 'r')
        return True
    except:
        return False

def initProcess():
    """
    This function prepares the main files that FinanceTrack operates with.\n
    This includes:\n
    categories.bills - Contains categories that can be used for income and expenses.\n
    income.bills - Contains all income data. Initialized with headers.\n
    expense.bills - Contains all epense data. Initialized with headers.\n
    \n
    This function does not create budget.bills.
    """
    categories = ['Bills\n', 'Auto\n', 'Groceries\n', 'Medical\n', 'Loans\n', 'Subscriptions\n']
    catFile = openFile('categories.bills', 'w')
    catFile.writelines(categories)
    catFile.close()

    incomeFile = openFile('income.bills', 'w')
    incomeWriter = csv.writer(incomeFile)
    incomeWriter.writerow(["date", "category", "amount", "description"])
    incomeFile.close()

    expenseFile = openFile('expense.bills', 'w')
    expenseWriter = csv.writer(expenseFile)
    expenseWriter.writerow(["date", "category", "amount", "description"])
    expenseFile.close()

def init(save_location = None):
    """
    This is the user-ran init function.\n
    save_location is an optional attribute. It does nothing if not set.\n
    setSave() will be ran if save_location is set.\n
    This function will run checkInitFile() to see if the program has previously been initialized.
    If the init file exists, user will be asked if they want to proceed with initialization, this will erase all existing data.\n
    Initialization is performed by initProcess().
    """
    if save_location:
        setSave(save_location)

    openSuccess = checkInitFile()

    if openSuccess:
        question = input("This program has already been initialized. Are you sure you'd like to continue? All existing data will be lost.\nType 'Yes' to confirm: ")
        if question == 'Yes':
            initProcess()
    else:
        initProcess()
        initFile = openFile('init.bills', 'w')

def add_income(category, amount, description):
    pass


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
    case None:
        print("Please enter an argument in the command line.")
    case _:
        print("Invalid command. Use 'list commands' to see list of commands. Use 'help' to learn more about a command.")