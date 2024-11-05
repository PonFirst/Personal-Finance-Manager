'''
This function ask for details of a transaction and add it to the database.
The element include account id, amount, description, and date(and time).

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
        datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
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
            account_id TEXT,
            amount REAL,
            description TEXT,
            date TEXT
        )
    ''')
    cursor.execute("PRAGMA table_info(transactions);")
    columns = [column[1] for column in cursor.fetchall()]
    if 'account_id' not in columns:
        cursor.execute("ALTER TABLE transactions ADD COLUMN account_id TEXT;")
        print("Added account_id column to transactions table.")
    conn.commit()
    conn.close()

def remove_source_account_id():
    """
    Function to remove source_account_id column
    """
    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()

    # Ensure the transactions table has the correct structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT,
            amount REAL,
            description TEXT,
            date TEXT
        )
    ''')

    # Check if the transaction column exists
    cursor.execute("PRAGMA table_info(transactions);")
    columns = [column[1] for column in cursor.fetchall()]
    if 'source_account_id' in columns: # If the column exists, remove it
        # Create a new table with the correct structure
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions_new (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT,
                amount REAL,
                description TEXT,
                date TEXT
            )
        ''')

        # Copy data from the old table to the new table
        cursor.execute('''
            INSERT INTO transactions_new (transaction_id, account_id, amount, description, date)
            SELECT transaction_id, account_id, amount, description, date
            FROM transactions
        ''')

        # Drop the old table
        cursor.execute('DROP TABLE transactions')

        # Rename the new table to the original table name
        cursor.execute('ALTER TABLE transactions_new RENAME TO transactions')

    conn.commit()
    conn.close()

def add_transaction():
    '''
    Function to add a transaction to the database
    '''
    check_column()  # Ensure the account_id column is added if it doesn't exist
    remove_source_account_id()  # Ensure the source_account_id column is removed

    while True:
        account_id = input("Enter destination account id (4 digits): ")
        if valid_bank_num(account_id):
            break

        print("Invalid account id. Please enter a 4-digit number.")

    while True:
        amount = input("Enter the transaction amount: ")
        if valid_amount(amount):
            amount = float(amount)
            break

        print("Invalid amount. Please enter a positive number.")

    description = input("Enter a description for the transaction: ")

    while True:
        transaction_date = input("Enter transaction date and time (format: YYYY-MM-DD HH:MM:SS): ")
        if valid_date(transaction_date):
            break

        print("Invalid date format. Please enter a valid date and time (YYYY-MM-DD HH:MM:SS).")

    transaction = {
        "account_id": account_id,
        "amount": amount,
        "description": description,
        "date": transaction_date,
    }

    print("Want to record the following transaction? :")
    print(f"account id: {transaction['account_id']}")
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
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT,
            amount REAL,
            description TEXT,
            date TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO transactions (account_id, amount, description, date)
        VALUES (?, ?, ?, ?)
    ''', (transaction['account_id'], transaction['amount'],
          transaction['description'], transaction['date']))
    conn.commit()
    conn.close()

    print("Transaction added successfully!")
    print(transaction)

if __name__ == '__main__':
    add_transaction()