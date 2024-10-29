'''
This function ask for details of a transaction and add it to the database.
The element include bank number, amount, description, and date(and time).
'''

import datetime
import sqlite3

def valid_bank_num(bank_number):
    """
    Function to validate bank number
    """
    return bank_number.isdigit() and len(bank_number) == 4

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
            bank_number TEXT,
            amount REAL,
            description TEXT,
            date TEXT
        )
    ''')
    cursor.execute("PRAGMA table_info(transactions);")
    columns = [column[1] for column in cursor.fetchall()]
    if 'bank_number' not in columns:
        cursor.execute("ALTER TABLE transactions ADD COLUMN bank_number TEXT;")
        print("Added bank_number column to transactions table.")
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
            bank_number TEXT,
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
                bank_number TEXT,
                amount REAL,
                description TEXT,
                date TEXT
            )
        ''')

        # Copy data from the old table to the new table
        cursor.execute('''
            INSERT INTO transactions_new (transaction_id, bank_number, amount, description, date)
            SELECT transaction_id, bank_number, amount, description, date
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
    check_column()  # Ensure the bank_number column is added if it doesn't exist
    remove_source_account_id()  # Ensure the source_account_id column is removed

    while True:
        bank_number = input("Enter destination bank number (4 digits): ")
        if valid_bank_num(bank_number):
            break

        print("Invalid bank number. Please enter a 4-digit number.")

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
        "bank_number": bank_number,
        "amount": amount,
        "description": description,
        "date": transaction_date,
    }

    print("Want to record the following transaction? :")
    print(f"Bank number: {transaction['bank_number']}")
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
            bank_number TEXT,
            amount REAL,
            description TEXT,
            date TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO transactions (bank_number, amount, description, date)
        VALUES (?, ?, ?, ?)
    ''', (transaction['bank_number'], transaction['amount'],
          transaction['description'], transaction['date']))
    conn.commit()
    conn.close()

    print("Transaction added successfully!")
    print(transaction)

if __name__ == '__main__':
    add_transaction()