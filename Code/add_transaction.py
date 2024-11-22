'''
This function ask for details of a transaction and add it to the database.
The element include account id, amount, description, and date.

Created by Copter
'''
import datetime
import sqlite3

# Function to validate account id
def valid_bank_num(account_id):
    return account_id.isdigit() and len(account_id) == 4

# Function to validate amount
def valid_amount(amount):
    try:
        amount = float(amount)
        return amount > 0
    except ValueError:
        return False

# Function to validate date
def valid_date(date_str):
    if len(date_str) != 10:
        return False
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to check if source account id and destination account id are the same
def id_check(source_account_id, destination_account_id):
    return source_account_id == destination_account_id

# Function to check if the account exists in the database
def account_check(account_id):
    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT category FROM Accounts WHERE account_id = ?", (account_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Function to check if the transaction between account types is allowed
def type_allow(source_account_type, destination_account_type):
    allowed_category = {
        "Expense": ["Asset", "Liability"],
        "Asset": ["Expense", "Liability"],
        "Income" : ["Asset", "Liability"],
        "Liability" : ["Asset"],
    }
    return destination_account_type in allowed_category.get(source_account_type, [])

# Function to validate description
def valid_description(description):
    return any(char.isalpha() for char in description)

#Act as a main function to add a transaction
def add_transaction():

    while True:     # Loop until a valid source account id is entered
        source_account_id = input("Enter source account id (4 digits) or 'C' to cancel: ")
        if source_account_id.upper() == 'C':
            print("Transaction cancelled.")
            return
        if valid_bank_num(source_account_id):
            source_account_type = account_check(source_account_id)
            if source_account_type:
                break
        print("Invalid account id or account does not exist. Please enter a valid 4-digit number.")

    while True:     # Loop until a valid destination account id is entered
        destination_account_id = input("Enter destination account id (4 digits) or 'C' to cancel: ")
        if destination_account_id.upper() == 'C':
            print("Transaction cancelled.")
            return
        if valid_bank_num(destination_account_id):
            if not id_check(source_account_id, destination_account_id):
                destination_account_type = account_check(destination_account_id)
                if destination_account_type:
                    if type_allow(source_account_type, destination_account_type):
                        break
                    else:
                        print(f"Transaction from {source_account_type} to {destination_account_type} is not allowed.")
                else:
                    print("Destination account does not exist.")
            else:
                print("Source account id and destination account id cannot be the same.")
        else:
            print("Invalid account id. Please enter a 4-digit number.")

    while True:     # Loop until a valid amount is entered
        amount = input("Enter the transaction amount or 'C' to cancel: ")
        if amount.upper() == 'C':
            print("Transaction cancelled.")
            return
        if valid_amount(amount):
            amount = float(amount)
            break

        print("Invalid amount. Please enter a positive number.")

    while True:     # Loop until a valid description is entered
        description = input("Enter a description for the transaction or 'C' to cancel: ")
        if description.upper() == 'C':
            print("Transaction cancelled.")
            return
        if valid_description(description):
            break

        print("Invalid description. Please enter at least one letter.")

    while True:     # Loop until a valid date is entered
        transaction_date = input("Enter transaction date (format: YYYY-MM-DD) or 'C' to cancel: ")
        if transaction_date.upper() == 'C':
            print("Transaction cancelled.")
            return
        if valid_date(transaction_date):
            break

        print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")

    transaction = {     # Create a dictionary to store the transaction details
        "source_account_id": source_account_id,
        "destination_account_id": destination_account_id,
        "amount": amount,
        "description": description,
        "date": transaction_date,
    }

    # Ensure the user
    print("Want to record the following transaction? :")
    print(f"Source account id: {transaction['source_account_id']}")
    print(f"Destination account id: {transaction['destination_account_id']}")
    print(f"Amount: {transaction['amount']}")
    print(f"Description: {transaction['description']}")
    print(f"Date: {transaction['date']}")
    confirmation = input(" Y for Yes, N for No: ").upper()
    if confirmation == 'N':
        print("Transaction cancelled.")
        return

    print("Transaction confirmed.")

    # Connect to the SQLite database
    conn = sqlite3.connect('personal_finance.db')       
    cursor = conn.cursor()

    # Execute a query to insert the transaction into the database
    cursor.execute('''
            INSERT INTO Transactions (source_account_id, destination_account_id, amount, description, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (transaction['source_account_id'], transaction['destination_account_id'], transaction['amount'],
              transaction['description'], transaction['date']))
    conn.commit()
    conn.close()

    print("Transaction added successfully!")
    print(transaction)
