from sys import argv
import csv

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
# set-save-location
# help command
# init

try:
    dataSource = open('saveloc.bills', 'r')
    saveLoc = dataSource.read()
    dataSource.close()
except:
    dataSource = open('saveloc.bills', 'w')
    dataSource.write('data/')
    saveLoc = 'data/'
    dataSource.close()

try:
    command = argv[1]
except:
    command = None

def checkInitFile():
    try:
        initFile = open('init.bills', 'r')
        return True
    except:
        return False
    
def openFile(filename, rw):
    return open(f'{saveLoc}{filename}', rw)

def initProcess():
    categories = ['Bills\n', 'Auto\n', 'Groceries\n', 'Medical\n', 'Loans\n', 'Subscriptions\n']
    catFile = openFile('categories', 'w')
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

def init():
    openSuccess = checkInitFile()

    if openSuccess:
        question = input("This program has already been initialized. Are you sure you'd like to continue?\nType 'Yes' to confirm: ")
        if question == 'Yes':
            initProcess()
    else:
        initProcess()
        initFile = openFile('init.bills', 'w')

def add_income(category, amount, description):
    pass


match command:
    case 'init':
        init()
    case None:
        print("Please enter an argument in the command line.")
    case _:
        print("Invalid command. Use 'list commands' to see list of commands. Use 'help' to learn more about a command.")