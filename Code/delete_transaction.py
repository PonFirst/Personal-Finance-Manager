'''
delete transaction from the database
the code will ask user whether they want to search by account or date or show all transaction 
before they put in transaction id to delete
'''

import sqlite3
from add_transaction import *
from show_transaction import *

# Function to delete transaction from the database
def delete_transaction(db_path, transaction_id):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute a query to delete a transaction by id
        cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        if cursor.rowcount == 0:
            print(f"No transaction found with id {transaction_id}.")
            return
        
        # Commit the transaction
        conn.commit()
        print(f"Transaction with id {transaction_id} deleted successfully.")
        
        # Close the connection
        conn.close()
        
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
         
def search_by_account():
    account_number = input("Enter the bank account number (4 digits): ")
    if valid_bank_num(account_number):
        # Add logic to search transactions by account number
        print(f"Searching transactions for account number: {account_number}")
    else:
        print("Invalid bank account number. Please enter a 4-digit number.")
        
def search_by_date():
    date_str = input("Enter the date (YYYY-MM-DD HH:MM:SS): ")
    if valid_date(date_str):
        # Add logic to search transactions by date
        print(f"Searching transactions for date: {date_str}")
    else:
        print("Invalid date format. Please enter the date in the format YYYY-MM-DD HH:MM:SS.")
        
# main function that ask whether user want to search by account or date or show full list of transaction to view before delete before they put in transaction id to delete
def main():
    search_by = input("Do you want to search by bank account or date? (account/date/show all): ")
    if search_by.lower() == "account":
        search_by_account()
    elif search_by.lower() == "date":
        search_by_date()
    elif search_by.lower() == "show all":
        show_transactions()
    else:
        print("Invalid search option. Please enter 'account' or 'date' or 'show all'.")
        
    transaction_id = input("Enter the transaction id to delete: ")
    try:
        transaction_id = int(transaction_id)
        delete_transaction('personal_finance.db', transaction_id)
    except ValueError:
        print("Invalid transaction id. Please enter a numeric value.")
    
# Function to search for transaction in the personal finance database
if __name__ == "__main__":
    main()