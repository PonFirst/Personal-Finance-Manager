
'''
Function to search for transaction from database
By asking if user want to search by Bank number or Date
'''

import datetime
import sqlite3

def valid_id(bank_number):
    return bank_number.isdigit() and len(bank_number) == 4  

def valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False
    
def search_transaction():
    print("How would you like to search for the transaction?")
    print("1. By Bank Number")
    print("2. By Date")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        bank_number = input("Enter the bank number to search for: ")
        if not valid_id(bank_number):
            print("Invalid bank number. Please enter a 4-digit number.")
            return
        
        connection = sqlite3.connect("personal_finance.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Transactions WHERE source_account_id = ? OR destination_account_id = ?", (bank_number, bank_number))
        results = cursor.fetchall()
        connection.close()
        
        if not results:
            print(f"No transactions found for bank number {bank_number}.")
        else:
            print("Transactions found:")
            for result in results:
                print(result)
    
    elif choice == "2":
        while True:
            date_str = input("Enter the date to search for (format: YYYY-MM-DD HH:MM:SS): ")
            if valid_date(date_str):
                break
            else:
                print("Invalid date format. Please enter a valid date and time (YYYY-MM-DD HH:MM:SS).")
        
        connection = sqlite3.connect("personal_finance.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Transactions WHERE date = ?", (date_str,))
        results = cursor.fetchall()
        connection.close()
        
        if not results:
            print(f"No transactions found for date {date_str}.")
        else:
            print("Transactions found:")
            for result in results:
                print(result)
    
    else:
        print("Invalid choice. Please enter 1 or 2.")
        
if __name__ == "__main__":
    search_transaction()
