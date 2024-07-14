# Boilerplate feature for program to function
from sys import argv
import csv
import os
from datetime import datetime
import json
import random as rand
import calendar
saveLoc = 'data/'

# Commands:
# add income category amount description ***
# add expense category amount description ***
# add category name description ***
# list categories ***
# list commands ***
# total income month year ***
# total expenses month year ***
# total profit month year ***
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
            rebase_budget()

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

        case 'total':
            try:
                type = attribute[0]

                if len(attribute) >= 2:
                    year = int(attribute[1])
                else:
                    year = datetime.today().year

                if len(attribute) >= 3:
                    month = attribute[2]
                else:
                    month = str(datetime.today().month)

                if not month.isdigit():
                    if len(month) == 3:
                        month = list(calendar.month_abbr).index(month.capitalize())
                    else:
                        month = list(calendar.month_name).index(month.capitalize())
                else:
                    month = int(month)

                if type == 'income':
                    totalIncome = total('income.bills', month, year)
                    print(f"You have earned ${totalIncome:.2f} in {calendar.month_name[month]}, {year}.")
                elif type == 'expense':
                    totalExpense = total('expense.bills', month, year)
                    print(f"You have spent ${totalExpense:.2f} in {calendar.month_name[month]}, {year}.")
                elif type == 'profit':
                    income = total('income.bills', month, year)
                    expense = total('expense.bills', month, year)
                    totalProfit = income - expense
                    print(f"You have overall earned ${totalProfit:.2f} in {calendar.month_name[month]}, {year}.")
                else:
                    print("Please choose income, expense, or profit.")
            except:
                print("Please enter valid options for type, month, and year.")
                print('Valid types are:\n\tincome\n\texpense\n\tprofit')
                        
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
        bool: True if folder had to be created. False if it already existed.
    """
    global saveLoc
    if location[-1] != '/':
        location = location + '/'
    dataSource = open('saveloc.bills', 'w')
    dataSource.write(location)
    saveLoc = location
    dataSource.close()
    newPath = False
    if not os.path.exists(location):
        os.makedirs(location)
        newPath = True
    return newPath


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

def init(save_location = None, suppress = False, force_creation = False):
    """
    Initializes the program in the current save location. Also sets save location if specified.

    Args:
        save_location (str): Path to the desired save location if desired to change.
        suppress (bool): Set True to prevent prompt from being printed to console. Will be treated as "No".
        force_creation (bool): Suppresses prompt and sets answer to "Yes". Not recommended.

    Returns:
        bool: True if successful, False if process failed.
    """
    initSuccess = False
    if save_location:
        setSave(save_location)

    openSuccess = checkInitFile()

    if openSuccess:
        question = None
        if not suppress and not force_creation:
            question = input("This program has already been initialized. Are you sure you'd like to continue? All existing data will be lost.\nType 'Yes' to confirm: ")
        if force_creation:
            question = 'Yes'
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
        print('init: Initializes this program.')
        print('check-init: Check if your program has been initialized.')
        print('set-save: Sets the save location for this program.')
        print('read-save: Prints out the current save location.')
        print('set-budget: Creates a budget file that your expenses will be checked against.')
        print('read-budget: Print out current budget.')
        print('rebase-budget: Make sure all categories in budget are valid.')
        print('add: Allows you to add income, expenses, or a new category.')
        print('list: Lists available categories or commands.')
        print('total: Provides the total income, expense, or profit for the current or specified month.')
        print('remove: Removes a line of income or expense based on the given id.')
        print('help: Provides additional details about any given command.')
    return commands

def init_budget():
    """
    Initializes budget file to initial state.

    Returns:
        str: ID of save location.
    """
    file = openFile('budget.bills', 'w')
    budgetContent = {}
    budgetContent['id'] = get_init_id()
    json.dump(budgetContent, file)
    file.close()
    return budgetContent['id']

def set_budget(budget, category, redoInit = False, suppress = False):
    """
    Sets the budget in budget.bills given an appropriate category.

    Args:
        budget (float): The budget amount.
        category (str): Which category to impliment the budget.
        redoInit (bool): Erases budget.bills and creates new one if set to true.
        suppress (bool): Prevent warnings and errors from being printed to console.

    Returns:
        bool: True if successful, False if failed.
    """
    file = openFile('categories.bills', 'r')
    categories = file.readlines()
    file.close()

    try:
        budgetContent = read_budget(True)
        initNumber = get_init_id()
        if budgetContent['id'] != initNumber and not suppress:
            print("Warning: Budget file contains invalid ID. Please run rebase-budget.")
    except:
        init_budget()

    if category + '\n' in categories:
        budgetContent[category] = budget
    else:
        if not suppress:
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
        dict: Content of budget.bills; invalid categories set to None
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
        else:
            for item in budgetContent:
                if item + '\n' not in categories:
                    budgetContent[item] = None

        return budgetContent
    except:
        if not suppress:
            print("Please set a budget.")
        return None
    
def rebase_budget(suppress = False, forceAddCats = False):
    """
    Checks if the budget file is valid for this save, and makes fixes when needed.

    Args:
        suppress (bool): Prevent user from being prompted to add new categories.
        forceAddCats (bool): Bypass prompt to add new categories and adds them if needed.

    Returns:
        bool: True if successful, False if failed.
    """
    id = get_init_id()
    categories = list_categories(True)
    budget = read_budget(True)
    invalidCategories = []

    validCategories = True
    for category in budget:
        if category + '\n' not in categories and category != 'id':
            validCategories = False
            invalidCategories.append(category)

    file = openFile('budget.bills', 'w')

    if validCategories:
        budget['id'] = id
        json.dump(budget, file)
        file.close()
        return True
    else:
        createPrompt = None
        if not suppress and not forceAddCats:
            print("The following invalid categories were detected:")
            for category in invalidCategories:
                print('\t' + category)
            print("Would you like to create them?\nType 'Yes' if so.")
            createPrompt = input("> ")
        if forceAddCats:
            createPrompt = 'Yes'
        if createPrompt == 'Yes':
            for category in invalidCategories:
                add_category(category)
            budget['id'] = id
            json.dump(budget, file)
            file.close()
            return True
        else:
            return False
        
def total(file, month, year):
    """
    Totals up data from the given csv-formatted file.

    Args:
        file (str): File to extract data from.
        month (int): Month filter.
        year (int): Year filter.

    Returns:
        float: The calculated total.
    """
    file = openFile(file, 'r')
    csvObject = csv.reader(file)
    content = []
    for i in csvObject:
        content.append(i)
    file.close()
    categories = list_categories(True)
    totalAmount = 0

    h = {
        'id':0,
        'date':1,
        'category':2,
        'amount':3,
        'description':4
    }

    validEntries = []
    for entry in content[1:]:
        category = entry[h['category']]
        eyear = int(entry[h['date']][0:4])
        emonth = int(entry[h['date']][4:6])
        amount = float(entry[h['amount']])
        if category + '\n' in categories and eyear == year and emonth == month:
            totalAmount += amount
    return totalAmount



if __name__ == '__main__':
    main()