'''
Function to search for transaction from database
By asking if user want to search by Bank number or Date

Created by Copter
'''

import datetime
import sqlite3

def valid_id(account_id):
    '''
    Function to check if the bank number is valid
    '''
    return account_id.isdigit() and len(account_id) == 4

def valid_date(date_str):
    '''
    Function to check if the date is valid
    '''
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def search_transaction():
    '''
    Function to search for transaction from database
    '''
    print("How would you like to search for the transaction?")
    print("1. By Bank Number")
    print("2. By Date")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        account_id = input("Enter the source account id to search for: ")
        if not valid_id(account_id):
            print("Invalid bank number. Please enter a 4-digit number.")
            return

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

        print("Transactions found:")
        for result in results:
            print(result)

    elif choice == "2":
        while True:
            date_str = input("Enter the date to search for (format: YYYY-MM-DD): ")
            if valid_date(date_str):
                break
            print("Invalid date format. Please re-enter (YYYY-MM-DD).")

        connection = sqlite3.connect("personal_finance.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Transactions WHERE date(date) = date(?)", (date_str,))
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        connection.close()

        if not results:
            print(f"No transactions found for date {date_str}.")
        else:
            print("Transactions found:")
            for result in results:
                for col_name, value in zip(column_names, result):
                    print(f"{col_name}: {value}")
                print()

    else:
        print("Invalid choice. Please enter 1 or 2.")
