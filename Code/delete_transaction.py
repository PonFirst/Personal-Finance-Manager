'''
delete transaction from the database
the code will ask user whether they want to search by account or date or show all transaction
before they put in transaction id to delete

Created by Copter
'''

import sqlite3
from add_transaction import valid_bank_num, valid_date
from show_transaction import show_transactions

# Function to delete transaction from the database
def delete_transaction():
    """
    Delete a transaction from the database by its ID.
    """
    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()
    
    while True:
        search_by = input("Do you want to search by source account id or date? (account/date/show all/cancel): ")
        if search_by.lower() == "account":
            if search_by_account():
                conn.close()
                return
            break
        elif search_by.lower() == "date":
            if search_by_date():
                conn.close()
                return
            break
        elif search_by.lower() == "show all":
            show_transactions()
            break
        elif search_by.lower() == "cancel":
            print("Operation cancelled.")
            conn.close()
            return
        else:
            print("Invalid search option. Please enter 'account', 'date', 'show all', or 'cancel'.")

    while True:
        transaction_id = input("Enter the transaction id to delete (or type 'cancel' to exit): ")
        if transaction_id.lower() == 'cancel':
            print("Operation cancelled.")
            conn.close()
            return
        try:
            transaction_id = int(transaction_id)
            # Execute a query to delete a transaction by id
            cursor.execute("DELETE FROM transactions WHERE transaction_id=?", (transaction_id,))
            if cursor.rowcount == 0:
                print(f"No transaction found with id {transaction_id}.")
            else:
                conn.commit()
                print(f"Transaction with id {transaction_id} deleted successfully.")
                break
        except ValueError:
            print("Invalid transaction id. Please enter a numeric value.")

    # Close the connection
    conn.close()


def search_by_account():
    """
    Search transactions by bank account number.
    """
    account_number = input("Enter the bank id number (4 digits) or type 'cancel' to exit: ")
    if account_number.lower() == 'cancel':
        print("Operation cancelled.")
        return True
    if valid_bank_num(account_number):
        # Connect to the SQLite database
        conn = sqlite3.connect('personal_finance.db')
        cursor = conn.cursor()

        # Execute a query to search transactions by account number
        cursor.execute("SELECT * FROM transactions WHERE source_account_id=?", (account_number,))
        transactions = cursor.fetchall()

        if transactions:
            print(f"Transactions for account number {account_number}:")
            column_names = [description[0] for description in cursor.description]
            for transaction in transactions:
                for col_name, value in zip(column_names, transaction):
                    print(f"{col_name}: {value}")
                print("-" * 20)
        else:
            print(f"No transactions found for account number {account_number}.")

        # Close the connection
        conn.close()
    else:
        print("Invalid bank account number. Please enter a 4-digit number.")
    return False

def search_by_date():
    """
    Search transactions by date.
    """
    date_str = input("Enter the date (YYYY-MM-DD HH:MM:SS) or type 'cancel' to exit: ")
    if date_str.lower() == 'cancel':
        print("Operation cancelled.")
        return True
    if valid_date(date_str):
        # Connect to the SQLite database
        conn = sqlite3.connect('personal_finance.db')
        cursor = conn.cursor()

        # Execute a query to search transactions by date
        cursor.execute("SELECT * FROM transactions WHERE date=?", (date_str,))
        transactions = cursor.fetchall()

        if transactions:
            print(f"Transactions for date {date_str}:")
            column_names = [description[0] for description in cursor.description]
            for transaction in transactions:
                for col_name, value in zip(column_names, transaction):
                    print(f"{col_name}: {value}")
                print("-" * 20)
        else:
            print(f"No transactions found for date {date_str}.")

        # Close the connection
        conn.close()
    else:
        print("Invalid date format. Please enter the date in the format YYYY-MM-DD")
    return False
