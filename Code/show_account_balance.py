"""show_account_balance.py 
Program to show the account balance that let user choose 
to display all account or selected account which keep in the account_database.db """

import sqlite3

def connect_db():
    # Connect to the SQLite database
    return sqlite3.connect('account_database.db')

def display_all_accounts(conn):
    # Display all account balances.
    cursor = conn.cursor()
    cursor.execute("SELECT account_id, amount FROM accounts")
    accounts = cursor.fetchall()
    for account in accounts:
        print(f"Account ID: {account[0]}, Balance: {account[1]}")

def display_selected_account(conn, account_id):
    """Display balance for a selected account."""
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    if account:
        print(f"Account ID: {account_id}, Balance: {account[0]}")
    else:
        print(f"No account found with ID: {account_id}")

def main():
    conn = connect_db()
    try:
        choice = input("Enter 'all' to display all accounts or 'one' to display a specific account: ").strip().lower()
        if choice == 'all':
            display_all_accounts(conn)
        elif choice == 'one':
            account_id = input("Enter the account ID: ").strip()
            display_selected_account(conn, account_id)
        else:
            print("Invalid choice. Please enter 'all' or 'one'.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()