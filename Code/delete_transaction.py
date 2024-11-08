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
def delete_transaction(transaction_id):
    """
    Delete a transaction from the database by its ID.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('personal_finance.db')
        cursor = conn.cursor()

        # Execute a query to delete a transaction by id
        cursor.execute("DELETE FROM transactions WHERE transaction_id=?", (transaction_id,))
        if cursor.rowcount == 0:
            print(f"No transaction found with id {transaction_id}.")
            return

        # Commit the transaction
        conn.commit()
        print(f"Transaction with id {transaction_id} deleted successfully.")

        # Close the connection
        conn.close()

    except sqlite3.OperationalError as error:
        print(f"An error occurred: {error}")

# Add the function call to delete_transaction
def main():
    """
    Main function that asks whether the user wants to search by account or date or show the list
    of transactions to view before deleting a transaction by its ID.
    """
    while True:
        search_by = input("Do you want to search by source account id or date? (account/date/show all): ")
        if search_by.lower() == "account":
            search_by_account()
            break
        elif search_by.lower() == "date":
            search_by_date()
            break
        elif search_by.lower() == "show all":
            show_transactions()
            break
        else:
            print("Invalid search option. Please enter 'account' or 'date' or 'show all'.")

    while True:
        transaction_id = input("Enter the transaction id to delete: ")
        try:
            transaction_id = int(transaction_id)
            delete_transaction(transaction_id)
            break
        except ValueError:
            print("Invalid transaction id. Please enter a numeric value.")


def search_by_account():
    """
    Search transactions by bank account number.
    """
    account_number = input("Enter the bank id number (4 digits): ")
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

def search_by_date():
    """
    Search transactions by date.
    """
    date_str = input("Enter the date (YYYY-MM-DD HH:MM:SS): ")
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
        print("Invalid date format. Please enter the date in the format YYYY-MM-DD HH:MM:SS.")

if __name__ == "__main__":
    main()