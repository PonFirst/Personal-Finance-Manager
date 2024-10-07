"""Add account function for personal finance manager to add new account to database
Add Account Create a new account that contains 
- Account type
- Account name
- Account ID
- Amount of money"""

import sqlite3
from account import Account

# Initialize the database function
def initialize_database():
    
    connection = sqlite3.connect('account_database.db')
    cursor = connection.cursor()
    
    # Create the accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    connection.commit()
    connection.close()

# add account function
def add_account():
    
    try:
        # Get account type
        account_type = str(input("Enter account type (Income, Expense, Asset, Liability): "))
        
        # Get account name
        account_name = str(input("Enter account name: "))
        
        # Get account ID
        account_id = str(input("Enter account ID: "))
        
        # Get amount of money
        amount = float(input("Enter amount of money: "))
        
        # Create an Account instance to validate the data
        account = Account(account_id, account_name, account_type, amount)
        
        # Connect to the database and insert the account
        connection = sqlite3.connect('account_database.db')
        cursor = connection.cursor()
        
        cursor.execute('''
            INSERT INTO accounts (account_id, name, category, amount)
            VALUES (?, ?, ?, ?)
        ''', (account.account_id, account.name, account.category, account.amount))
        
        connection.commit()
        connection.close()
        
        print("Account has been added")
        
    except ValueError as e:
        print(f"Error: {e}")
    except sqlite3.IntegrityError:
        print("Error: Account ID already exists.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Initialize the database 
    initialize_database()
    # Add account
    add_account()

if __name__ == "__main__":
    main()



# Add account to the account database (csv file)
"""import os
import csv

def add_account():
    
    account_type = input("Enter account type(Income, Expense, Asset, Liability): ") 
    
    account_name = input("Enter account name: ")
   
    account_id = input("Enter account ID: ")
  
    amount = input("Enter amount of money: ")
    
    # Open the csv file to write
    with open("account_database.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([account_type, account_name, account_id, amount])
        
    print("Account has been added")



def main():
    add_account()


if __name__ == "__main__":
    main()"""