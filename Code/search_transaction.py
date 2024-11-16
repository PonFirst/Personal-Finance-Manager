'''
Function to search for transaction from database
By asking if user want to search by Bank number or Date

Created by Copter
'''

import datetime
import sqlite3

# Function to check if the bank number is valid
def valid_id(account_id):
    return account_id.isdigit() and len(account_id) == 4

# Function to check if the date is valid
def valid_date(date_str):
    if len(date_str) != 10:
        return False
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to check that will look for transaction in database
def show_check():
    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transactions")
    result = cursor.fetchall()
    conn.close()
    return result

# Act as a main function to search for the transaction
def search_transaction():
    if not show_check():
        print("No transactions available to search.")
        return

    # Ask the user how they would like to search for the transaction
    while True:
        print("How would you like to search for the transaction?")
        print("1. Source account Number")
        print("2. Destination account Number")
        print("3. Date")
        choice = input("Enter your choice (1, 2, 3 or cancel): ")

        if choice == "1":       # Search by bank number
            account_id = input("Enter the source account id to search for (or type 'cancel' to exit): ")
            if account_id.lower() == 'cancel':
                print("Operation cancelled.")
                return
            if not valid_id(account_id):
                print("Invalid account number. Please enter a 4-digit number.")
                continue

            connection = sqlite3.connect("personal_finance.db")
            cursor = connection.cursor()
            query = (
                "SELECT * FROM Transactions WHERE source_account_id = ?"
            )
            cursor.execute(query, (account_id,))
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            connection.close()

            if not results:
                print(f"No transactions found for bank number {account_id}.")
                continue

            print("Transactions found:")
            print("-" * 40)
            for result in results:
                for col_name, value in zip(column_names, result):
                    print(f"{col_name}: {value}")
                print("-" * 40)
            break

        elif choice == "2":     # Search by destination bank number
            account_id = input("Enter the destination account id to search for (or type 'cancel' to exit): ")
            if account_id.lower() == 'cancel':
                print("Operation cancelled.")
                return
            if not valid_id(account_id):
                print("Invalid account number. Please enter a 4-digit number.")
                continue

            connection = sqlite3.connect("personal_finance.db")
            cursor = connection.cursor()
            query = (
                "SELECT * FROM Transactions WHERE destination_account_id = ?"
            )
            cursor.execute(query, (account_id,))
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            connection.close()

            if not results:
                print(f"No transactions found for account number {account_id}.")
                continue

            print("Transactions found:")
            print("-" * 40)
            for result in results:
                for col_name, value in zip(column_names, result):
                    print(f"{col_name}: {value}")
                print("-" * 40)
            break

        elif choice == "3":     # Search by date range
            
            # Get the start date
            while True:
                start_date = input("Enter the start date (format: YYYY-MM-DD) (or type 'cancel' to exit): ")
                if start_date.lower() == 'cancel':
                    print("Operation cancelled.")
                    return
                if valid_date(start_date):
                    break
                print("Invalid date format. Please re-enter (YYYY-MM-DD).")

            # Get the end date
            while True:
                end_date = input("Enter the end date (format: YYYY-MM-DD) (or type 'cancel' to exit): ")
                if end_date.lower() == 'cancel':
                    print("Operation cancelled.")
                    return
                if valid_date(end_date):
                    if end_date >= start_date:
                        break
                    else:
                        print("End date must be after start date. Please re-enter.")
                else:
                    print("Invalid date format. Please re-enter (YYYY-MM-DD).")

            connection = sqlite3.connect("personal_finance.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Transactions WHERE date(date) BETWEEN date(?) AND date(?)", (start_date, end_date))
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            connection.close()

            if not results:
                print(f"No transactions found between dates {start_date} and {end_date}.")
                continue

            print("Transactions found:")
            print("-" * 40)
            for result in results:
                for col_name, value in zip(column_names, result):
                    print(f"{col_name}: {value}")
                print("-" * 40)
            break

        elif choice == "cancel":     # Cancel operation
            print("Operation cancelled.")
            return
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
