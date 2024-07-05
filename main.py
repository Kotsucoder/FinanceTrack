from sys import argv

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
# help command
# init

try:
    command = argv[1]
except:
    print("Please enter an argument in the command line.")

def init():
    # TODO: Check if program already initialized

    categories = ['Bills\n', 'Auto\n', 'Groceries\n', 'Medical\n', 'Loans\n', 'Subscriptions\n']
    file = open('categories.bills', 'w')
    file.writelines(categories)

    # TODO: Initialize income and expenses

def add_income(category, amount, description):
    pass


match command:
    case 'init':
        init()
    case _:
        print("Invalid command. Use 'list commands' to see list of commands. Use 'help' to learn more about a command.")