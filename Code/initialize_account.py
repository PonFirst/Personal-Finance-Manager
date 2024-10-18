import account_database
from account import Account


def use_template():
    account_database.create_account_table()
    account_database.create_transactions_table()
    account_database.create_budget_table()
    default_accounts = [
        Account(1000, "Account 1", "Income", 0),
        Account(2000, "Account 2", "Expense", 0),
        Account(3000, "Account 3", "Asset", 0),
        Account(4000, "Account 4", "Liability", 0)
    ]
    
    
def upload_template():
    filename = input("Enter the name of the file you want to use: ")
    f = open(filename, "r")
    
    