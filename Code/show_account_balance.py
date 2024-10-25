"""show_account_balance.py 
Program to show the account balance that let user choose 
to display all account or selected account which keep in the account_database.db """

import sqlite3

def connect_db():
    # Connect to the SQLite database
    return sqlite3.connect('personal_finance.db')

def display_all_accounts(connection):
    # Display all account balances.
    cursor = connection.cursor()
    cursor.execute("SELECT account_id, amount FROM accounts")
    accounts = cursor.fetchall()
    for account in accounts:
        print(f"Account ID: {account[0]}, Balance: {account[1]}")

def display_selected_account(connection, account_id):
    #Display balance for a selected account.
    cursor = connection.cursor()
    cursor.execute("SELECT amount FROM accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    if account:
        print(f"Account ID: {account_id}, Balance: {account[0]}")
    else:
        print(f"No account found with ID: {account_id}")

def main():
    connection = connect_db()
    try:
        choice = input("Enter 'all account' to display all accounts or 'select account' to display a specific account: ").strip().lower()
        if choice == 'all account':
            display_all_accounts(connection)
        elif choice == 'select account':
            account_id = input("Enter the account ID: ").strip()
            display_selected_account(connection, account_id)
        else:
            print("Invalid choice. Please enter 'all account' or 'select account'.")
    finally:
        connection.close()

if __name__ == "__main__":
    main()