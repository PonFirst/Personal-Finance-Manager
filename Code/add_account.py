"""Add account function for personal finance manager to add new account to database
Add Account Create a new account that contains 
- Account type
- Account name
- Account ID
- Amount of money"""

import sqlite3
from account import Account
from account_database import create_account_table


# Note the validation functions are defined here but I will move them to a separate file in the next step
# Validate account type
def validate_account_type(account_type):
    valid_types = ["Income", "Expense", "Asset", "Liability"]
    account_type = account_type.title() # allow lowercase input
    if account_type not in valid_types:
        raise ValueError("Invalid account type.")

# Validate account name
def validate_account_name(account_name):
    if not account_name:
        raise ValueError("Account name cannot be empty.")
    
# Validate account ID uniqueness
def account_unique_id(account_id):
    connection = sqlite3.connect('personal_finance.db')
    cursor = connection.cursor()
    cursor.execute('SELECT account_id FROM accounts WHERE account_id = ?', (account_id,))
    account = cursor.fetchone()
    connection.close()
    return account is None

# Validate account ID
def validate_account_id(account_id):
    if not account_id:
        raise ValueError("Account ID cannot be empty.")
    if not account_id.isdigit():
        raise ValueError("Account ID must be a number.")
    if not account_unique_id(account_id):
        raise ValueError("Account ID already exists.")

# Validate amount
def validate_amount(amount):
    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a number.")
    return amount


# Add account function
def add_account():
    try:

        account_type = str(input("Enter account type (Income, Expense, Asset, Liability): "))
        validate_account_type(account_type)
        
        account_name = str(input("Enter account name: "))
        validate_account_name(account_name)
        
        account_id = str(input("Enter account ID: "))
        validate_account_id(account_id)
        
        amount = input("Enter amount of money: ")
        amount = validate_amount(amount)
        
        # Create an Account instance to validate the data
        account = Account(account_id, account_name, account_type, amount)
        
        # Connect to the database and add(insert) the account
        connection = sqlite3.connect('personal_finance.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO accounts (account_id, name, category, amount)
            VALUES (?, ?, ?, ?)
        ''', (account.account_id, account.name, account.category, account.amount))
        
        connection.commit()
        connection.close()
        
        print("Account has been added")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Initialize the database table
    create_account_table()
    # Add account
    add_account()

if __name__ == "__main__":
    main()