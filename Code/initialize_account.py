import account_database
from account import Account
import csv


def use_template(csv_file):
    account_database.create_account_table()
    account_database.create_transactions_table()
    account_database.create_budget_table()
    default_accounts = []
    
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        next(reader)
        
        for row in reader:
            account_id, name, category, balance = row
            account = Account(int(account_id), name, category, float(balance))
            
            account_database.insert_account(account)
    
    print(f"Accounts from {csv_file} have been successfully loaded into the database.")
    
    
def upload_template():
    filename = input("Enter the name of the file you want to use: ")
    f = open(filename, "r")
    
    
    