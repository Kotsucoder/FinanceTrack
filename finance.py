# Boilerplate feature for program to function
from sys import argv
import csv
import os
from datetime import datetime
import json
import random as rand
saveLoc = 'data/'

# Commands:
# add income category amount description ***
# add expense category amount description ***
# add category name description ***
# list categories ***
# list commands ***
# total income month year
# total expenses month year
# total profit month year
# remove income id
# remove expense id
# set-budget ***
# set-save ***
# help command
# init save-location ***

def main():
    """
    Main program when run from terminal.
    """

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
        
        case 'check-init':
            if checkInitFile():
                print("Program has been initialized.")
            else:
                print("Program not ready. Please run command 'init'.")

        case 'set-save':
            if attribute[0] == None:
                print("Warning: Save location will be set to the default. Is this what you want to do? (Y/N)")
                setDefault = input("> ")
                if setDefault == "Y":
                    attribute[0] = 'data/'
                else:
                    attribute[0] = saveLoc
            setSave(attribute[0])

        case 'read-save':
            print(saveLoc)

        case 'set-budget':
            try:
                budget = attribute[0]
                category = attribute[1]
                try:
                    budget = float(budget)
                    set_budget(budget, category)
                except:
                    print("Budget must be a number.")
            except:
                print("Please set a budget amount and category.")

        case 'read-budget':
            read_budget()

        case 'init-budget':
            print("Any pre-existing budget file will be erased. Would you like to continue?")
            print("Type 'Yes' to continue")
            proceed = input("> ")
            if proceed == "Yes":
                init_budget()

        case 'rebase-budget':
            # Will check if all categories are valid, and if so, set the ID.
            # If invalid categories are detected, ask if user wants to create them.
            # If Yes, do so, and then set the id.
            # Otherwise, fail rebase.
            pass

        case 'add':
            good = True
            validTypes = ['income', 'expense', 'category']

            if good:
                try:
                    type = attribute[0]
                    category = attribute[1]
                    if type != 'category':
                        amount = attribute[2]
                        description = attribute[3]
                except:
                    print("Please enter all required attributes.")
                    print("Required Attributes:\n\tType (Income, Expense, Category)\n\tCategory\n\tAmount (Except if Category)\n\tDescription (Except if Category)")
                    good = False

            if good and type not in validTypes:
                print("Please enter a valid option for Type.\nValid options are:\n\tIncome\n\tExpense\n\tCategory")
                good = False

            if good and type != 'category':
                try:
                    amount = float(amount)
                except:
                    print("Amount must be a number.")
                    good = False

            if good:
                match type:
                    case 'income':
                        add_bill('income.bills', category, amount, description)
                    case 'expense':
                        add_bill('expense.bills', category, amount, description)
                    case 'category':
                        add_category(category)

        case 'list':
            try:
                option = attribute[0]
            except:
                print("Please choose whether to list categories or commands.")

            match option:
                case 'categories':
                    list_categories()
                case 'commands':
                    list_commands()
                        
        case None:
            print("Please enter an argument in the command line.")

        case _:
            print("Invalid command. Use 'list commands' to see list of commands. Use 'help' to learn more about a command.")






def setSave(location = 'data/'):
    """
    Sets the current save location. Creates directory if it does not yet exist.

    Args:
        location (str): Path to the desired save location. Defaults to 'data/' if not set.

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
        categories.bills: Contains categories that can be used for income and expenses.  
        income.bills: Contains all income data. Initialized with headers.  
        expense.bills: Contains all expense data. Initialized with headers.  

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
            initFile = openFile('init.bills', 'w')
            initFile.write(str(rand.randint(0,999999999)))
            initFile.close()
        else:
            initSuccess = True
    else:
        initSuccess = initProcess()
        initFile = openFile('init.bills', 'w')
        initFile.write(str(rand.randint(0,999999999)))
        initFile.close()

    return initSuccess

def get_init_id():
    """
    Reads the contents of the init file.

    Returns:
        str: Program Save ID
    """
    file = openFile('init.bills', 'r')
    id = file.read()
    file.close()
    return id

def add_bill(filename, category, amount, description):
    """
    Adds bill content to file.

    Args:
        filename (str): Name of file to modify with new bill data.
        category (str): Category of bill. Must be present in categories.bills.
        amount (float): Amount of the bill.
        description (str): What the bill was for.
    
    Returns:
        list: Formatted bill data if arguments filled in correctly. Otherwise returns None.
    """
    file = openFile(filename, 'r')
    csvObject = csv.reader(file)
    content = []
    for i in csvObject:
        content.append(i)
    file.close()

    categories = list_categories(True)

    if category + '\n' in categories:
        toAdd = [len(content), datetime.today().strftime('%Y%m%d'), category, amount, description]
        content.append(toAdd)

        file = openFile(filename, 'w')
        billWriter = csv.writer(file)
        for item in content:
            billWriter.writerow(item)
        file.close()

        return toAdd
    else:
        print("Please use a valid category.")
        return None

def add_category(category):
    """
    Adds category to categories.bills file.

    Args:
        category (str): The category to add to file.

    Returns:
        str: Repeats the given category.
    """
    categories = list_categories(True)

    categories.append(category + '\n')

    file = openFile('categories.bills', 'w')
    file.writelines(categories)
    file.close()

    return category

def list_categories(suppress = False):
    """
    Lists all the categories listed in categories.bills.

    Args:
        suppress (bool): Does not print categories if set to True.

    Returns:
        list: Content of categories.bills file.
    """
    file = openFile('categories.bills', 'r')
    categories = file.readlines()
    file.close()

    if not suppress:
        for category in categories:
            print(category[:-1])

    return categories

def list_commands(suppress = False):
    """
    Lists all the commands in this module with a description of what they do.

    Args:
        suppress (bool): Does not print commands and description if set to True.

    Returns:
        list: List of commands.
    """
    commands = ['add', 'list', 'total', 'remove', 'set-budget', 'set-save', 'help', 'init']

    if not suppress:
        print('add: Allows you to add income, expenses, or a new category.')
        print('list: Lists available categories or commands.')
        print('total: Provides the total income, expense, or profit for the current or specified month.')
        print('remove: Removes a line of income or expense based on the given id.')
        print('set-budget: Creates a budget file that your expenses will be checked against.')
        print('set-save: Sets the save location for this program.')
        print('help: Provides additional details about any given command.')
        print('init: Initializes this program.')
    return commands

def init_budget():
    """
    Initializes budget file to initial state.

    Returns:
        str: ID of save location.
    """
    file = openFile('budget.bills', 'w')
    budgetContent = {}
    file.close()
    budgetContent['id'] = get_init_id()
    return budgetContent['id']

def set_budget(budget, category, redoInit = False):
    """
    Sets the budget in budget.bills given an appropriate category.

    Args:
        budget (float): The budget amount.
        category (str): Which category to impliment the budget.
        redoInit (bool): Erases budget.bills and creates new one if set to true.

    Returns:
        bool: True if successful, False if failed.
    """
    file = openFile('categories.bills', 'r')
    categories = file.readlines()
    file.close()

    try:
        budgetContent = read_budget(True)
        initNumber = get_init_id()
        if budgetContent['id'] != initNumber:
            print("Warning: Budget file contains invalid ID. Please run rebase-budget.")
    except:
        init_budget()

    if category + '\n' in categories:
        budgetContent[category] = budget
    else:
        print("Please select a valid category.")
        return False

    file = openFile('budget.bills', 'w')
    json.dump(budgetContent, file)
    file.close()
    return True

def read_budget(suppress = False):
    """
    Provides the contents of budget file.

    Args:
        suppress (bool): Does not print content to terminal if set to True.

    Returns:
        dict: Content of budget.bills
    """
    try:
        file = openFile('budget.bills', 'r')
        budgetContent = json.load(file)
        file.close()
        file = openFile('categories.bills', 'r')
        categories = file.readlines()
        file.close()

        if not suppress:
            for item in budgetContent:
                if item + '\n' in categories:
                    print(f"{item}: ${budgetContent[item]:.2f}")
                else:
                    if item != 'id':
                        print(f"Warning: Invalid category {item} detected. Please run rebase-budget.")

        return budgetContent
    except:
        if not suppress:
            print("Please set a budget.")
        return None
    
def rebase_budget():
    pass


    
if __name__ == '__main__':
    main()