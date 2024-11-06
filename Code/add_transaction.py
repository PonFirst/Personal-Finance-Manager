'''
This function ask for details of a transaction and add it to the database.
The element include account id, amount, description, and date.

Created by Copter
'''
import datetime
import sqlite3

def valid_bank_num(account_id):
    """
    Function to validate account id
    """
    return account_id.isdigit() and len(account_id) == 4

def valid_amount(amount):
    """
    Function to validate amount
    """
    try:
        amount = float(amount)
        return amount > 0
    except ValueError:
        return False

def valid_date(date_str):
    """
    Function to validate date
    """
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def check_column():
    """
    Function to check if the column exists in the database
    """
    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_account_id TEXT,
            destination_account_id TEXT NOT NULL,
            account_id TEXT,
            amount REAL,
            description TEXT,
            date TEXT
        )
    ''')
    cursor.execute("PRAGMA table_info(transactions);")
    columns = [column[1] for column in cursor.fetchall()]
    if 'source_account_id' not in columns:
        cursor.execute("ALTER TABLE transactions ADD COLUMN source_account_id TEXT;")
        print("Added source_account_id column to transactions table.")
    if 'account_id' not in columns:
        cursor.execute("ALTER TABLE transactions ADD COLUMN account_id TEXT;")
        print("Added account_id column to transactions table.")
    conn.commit()
    conn.close()

def id_check(source_account_id, account_id):
    """
    Function to check if source account id and destination account id are the same
    """
    return source_account_id == account_id

def add_transaction():
    '''
    Function to add a transaction to the database
    '''
    check_column()  # Ensure the necessary columns are added if they don't exist

    while True:
        source_account_id = input("Enter source account id (4 digits): ")
        if valid_bank_num(source_account_id):
            break

        print("Invalid account id. Please enter a 4-digit number.")

    while True:
        account_id = input("Enter destination account id (4 digits): ")
        if valid_bank_num(account_id):
            if not id_check(source_account_id, account_id):
                break
            else:
                print("Source account id and destination account id cannot be the same.")
        else:
            print("Invalid account id. Please enter a 4-digit number.")

    while True:
        amount = input("Enter the transaction amount: ")
        if valid_amount(amount):
            amount = float(amount)
            break

        print("Invalid amount. Please enter a positive number.")

    description = input("Enter a description for the transaction: ")

    while True:
        transaction_date = input("Enter transaction date (format: YYYY-MM-DD): ")
        if valid_date(transaction_date):
            break

        print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")

    transaction = {
        "source_account_id": source_account_id,
        "account_id": account_id,
        "amount": amount,
        "description": description,
        "date": transaction_date,
    }

    print("Want to record the following transaction? :")
    print(f"Source account id: {transaction['source_account_id']}")
    print(f"Destination account id: {transaction['account_id']}")
    print(f"Amount: {transaction['amount']}")
    print(f"Description: {transaction['description']}")
    print(f"Date: {transaction['date']}")
    confirmation = input(" Y for Yes, N for No: ").upper()
    if confirmation == 'N':
        print("Transaction cancelled.")
        return

    print("Transaction confirmed.")

    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO transactions (source_account_id, destination_account_id, account_id, amount, description, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (transaction['source_account_id'], transaction['account_id'], transaction['account_id'],
          transaction['amount'], transaction['description'], transaction['date']))
    conn.commit()
    conn.close()

    print("Transaction added successfully!")
    print(transaction)
