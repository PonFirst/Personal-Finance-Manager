"""show_account_balance02.py 
Program to show the account balance that lets the user choose 
to display all accounts or a selected account, which is kept in the personal_finance.db database.
version 2"""

import sqlite3

def connect_db():
    # Connect to the SQLite database
    return sqlite3.connect('personal_finance.db')

def display_all_accounts(connection):
    # Display all account balances.
    cursor = connection.cursor()
    cursor.execute("SELECT account_id, name, balance FROM Accounts")
    accounts = cursor.fetchall()
    for account in accounts:
        print(f"Account ID: {account[0]}, Account Name: {account[1]}, Balance: {account[2]}")

def display_selected_account_by_id(connection, account_id):
    # Display balance for a selected account by ID.
    cursor = connection.cursor()
    cursor.execute("SELECT name, balance FROM Accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    if account:
        print(f"Account ID: {account_id}, Account Name: {account[0]}, Balance: {account[1]}")
    else:
        print(f"No account found with ID: {account_id}")

def display_selected_account_by_name(connection, account_name):
    # Display balance for a selected account by name.
    cursor = connection.cursor()
    cursor.execute("SELECT account_id, balance FROM Accounts WHERE name = ?", (account_name,))
    account = cursor.fetchone()
    if account:
        print(f"Account Name: {account_name}, Account ID: {account[0]}, Balance: {account[1]}")
    else:
        print(f"No account found with name: {account_name}")

def main():
    connection = connect_db()
    try:
        while True:
            choice = input("Enter 'all' to show balance of all accounts,\n 'select by ID' to show balance by a account ID,\n 'select by name' to show balance of an account by name, or 'exit' to exit the program: ").strip().lower()
            if choice == 'all':
                display_all_accounts(connection)
            elif choice == 'select by id':
                account_id = input("Enter the account ID: ").strip()
                display_selected_account_by_id(connection, account_id)
            elif choice == 'select by name':
                account_name = input("Enter the account name: ").strip()
                display_selected_account_by_name(connection, account_name)
            elif choice == 'exit':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter 'all accounts', 'select account by ID', 'select account by name', or 'exit'.")
    finally:
        connection.close()

if __name__ == "__main__":
    main()