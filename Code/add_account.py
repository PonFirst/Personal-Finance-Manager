"""
add_account.py
Function for personal finance manager to add new account to database
Add Account Create a new account that contains, Account type, Account name, Account ID
and account balance. The program will generate four digit account ID based on user account type.

For example : Income account will have ID starting with 1, the account ID is 1001 and 
if there are more this type of account the next account ID will be 1002 and so on
The program will validate the account type, account name, account ID, and account balance. 
If the data is valid, the program will add the account to the database. 
If the data is invalid, the program will raise an error message and ask user to reinput data

Created by Baipor.
"""

"""
add_account.py
Function for personal finance manager to add new account to database
Add Account Create a new account that contains, Account type, Account name, Account ID
and account balance. The program will generate four digit account ID based on user account type.

For example : Income account will have ID starting with 1, the account ID is 1001 and 
if there are more this type of account the next account ID will be 1002 and so on
The program will validate the account type, account name, account ID, and account balance. 
If the data is valid, the program will add the account to the database. 
If the data is invalid, the program will raise an error message and ask user to reinput data

Created by Baipor.
"""

import sqlite3
from account import Account

class ExitInput(Exception):
    """Custom exception to handle user exit during input"""
    pass

def validate_account_type(account_type):
    """
    function to validate account type
    """
    valid_types = {
        "1": "Income",
        "2": "Expense",
        "3": "Asset",
        "4": "Liability"
    }
    if account_type not in valid_types:
        raise ValueError("Invalid account type.")
    return valid_types[account_type]

def validate_account_name(account_name):
    """
    function to validate account name
    """
    if not account_name.strip():
        raise ValueError("Account name cannot be empty.")
    return account_name

def is_account_name_unique(account_name):
    """
    function to check if account name is unique
    """
    connection = sqlite3.connect('personal_finance.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM Accounts WHERE name = ?', (account_name,))
    account = cursor.fetchone()
    connection.close()
    if account:
        raise ValueError("Account name already exists.")
    return account_name

def get_next_account_id(account_type):
    """
    function to get next account ID
    """
    type_prefix = {
        "Income": "1",
        "Expense": "2",
        "Asset": "3",
        "Liability": "4"
    }

    connection = sqlite3.connect('personal_finance.db')
    cursor = connection.cursor()

    prefix = type_prefix[account_type]
    cursor.execute('''
        SELECT MAX(account_id) FROM Accounts 
        WHERE account_id LIKE ?
    ''', (prefix + '%',))

    max_id = cursor.fetchone()[0]
    connection.close()

    if max_id is None:
        return int(prefix + "001")
    else:
        return int(max_id) + 1

def validate_amount(balance):
    """
    function to validate account balance
    """
    try:
        balance = float(balance)
        if balance < 0:
            raise ValueError("Balance cannot be negative.")
        return balance
    except ValueError:
        raise ValueError("Balance must be a positive number.")

def get_valid_input(prompt, validation_func):
    """
    function to get valid input
    """
    while True:
        user_input = input(prompt)
        if user_input == 'cancel':
            raise ExitInput("Cancel adding account...")
        try:
            return validation_func(user_input)
        except ValueError as e:
            print(f"Error: {e} Please try again.")

def add_account():
    """
    function to add account
    """
    try:
        # Get account type with validation
        account_type = get_valid_input(
            "Enter account type (1: Income, 2: Expense, 3: Asset, 4: Liability) or 'cancel' to exit: ",
            validate_account_type
        )

        # Get account name with validation and uniqueness check
        account_name = get_valid_input(
            "Enter account name or type 'cancel' to exit: ",
            lambda name: is_account_name_unique(validate_account_name(name))
        )

        # Get balance with validation
        balance = get_valid_input(
            "Enter amount of balance or type 'cancel' to exit: ",
            validate_amount
        )

        # Generate account ID
        account_id = get_next_account_id(account_type)

        # Create an Account instance
        account = Account(account_id, account_name, account_type, balance)

        # Connect to the database and add the account
        connection = sqlite3.connect('personal_finance.db')
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO Accounts (account_id, name, category, balance)
            VALUES (?, ?, ?, ?)
        ''', (account.account_id, account.name, account.category, account.balance))

        connection.commit()
        connection.close()

        print(f"\nAccount has been added successfully!")
        print(f"Account ID: {account_id}")
        print(f"Account Name: {account_name}")
        print(f"Account Type: {account_type}")
        print(f"Balance: {balance:,.2f} Baht")

    except ExitInput as e:
        print(e)
        print("Account creation canceled.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

