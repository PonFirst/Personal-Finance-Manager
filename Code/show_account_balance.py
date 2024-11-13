"""
show_account_balance.py 
Program to show the account balance that ask user choice to show balance 
of all account, or selected account which can show by account ID or account name.

Create by Baipor.
"""

import sqlite3

# Function to connect to the database
def connect_db():
   
    return sqlite3.connect('personal_finance.db')

# Function to display all account balances
def display_all_accounts(connection):
    
    cursor = connection.cursor()
    cursor.execute("SELECT account_id, name, balance FROM Accounts")
    accounts = cursor.fetchall()
    for account in accounts:
        print(f"Account ID: {account[0]}, Account Name: {account[1]}, Balance: {account[2]}\n")

# Function to display balance of selected account by ID
def display_selected_account_by_id(connection, account_id):

    cursor = connection.cursor()
    cursor.execute("SELECT name, balance FROM Accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    if account:
        print(f"Account ID: {account_id}, Account Name: {account[0]}, Balance: {account[1]}")
    else:
        print(f"No account found with ID: {account_id}")

# Function to display balance of selected account by name
def display_selected_account_by_name(connection, account_name):
    
    cursor = connection.cursor()
    cursor.execute("SELECT account_id, balance FROM Accounts WHERE name = ?", (account_name,))
    account = cursor.fetchone()
    if account:
        print(f"Account Name: {account_name}, Account ID: {account[0]}, Balance: {account[1]}\n")
    else:
        print(f"No account found with name: {account_name}\n")

#Function to show balance base on user choice
def show_balance():

    connection = connect_db()
    try:
        while True:
            choice = input(
                "Enter '1' to show balance of all accounts,\n"
                "      '2' to show balance by an account ID,\n"
                "      '3' to show balance of an account by name,\n"
                "      '4' to exit the program: "
            ).strip()

            if choice == '1':
                display_all_accounts(connection)
            elif choice == '2':
                account_id = input("Enter the account ID: ").strip()
                if account_id.isdigit():
                    display_selected_account_by_id(connection, account_id)
                else:
                    print("Invalid account ID. Please enter a numeric value.\n")
            elif choice == '3':
                account_name = input("Enter the account name: ").strip()
                display_selected_account_by_name(connection, account_name)
            elif choice == '4':
                print("Exiting the program.")
                break
            else:
                print("\nInvalid choice. Please enter '1', '2', '3', or '4'.\n")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()