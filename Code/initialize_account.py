import account_database
from account import Account
import csv


def use_template(csv_file):
    account_database.create_account_table()
    account_database.create_transactions_table()
    account_database.create_budget_table()
    
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
    
    try:
        with open(filename, "r") as f:
            use_template(filename)
            reader = csv.reader(f)
            header = next(reader)
            
            required_columns = ["Account_ID", "Name", "Category", "Balance"]
            valid_columns = True
            
            if len(header) < len(required_columns):
                print("Error: Missing columns in the file header.")
                columns_valid = False
                
            else:
                if header[0] != required_columns[0]:
                    print("Error: First column must be Account_ID.")
                    columns_valid = False
                if header[1] != required_columns[1]:
                    print("Error: Second column must be Name.")
                    columns_valid = False
                if header[2] != required_columns[2]:
                    print("Error: Third column must be Category.")
                if header[3] != required_columns[3]:
                    print("Error: Fourth column must be Balance.")
                    
            if valid_columns:
                use_template(filename)
            
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Please check the file name and try again.")
        
    
    
    
    