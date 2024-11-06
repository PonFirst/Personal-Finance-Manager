"""
show_account_balance.py 
Program to show the account balance that lets the user choose 
to display all accounts or a selected account, which is kept in the personal_finance.db database.
Create by Baipor.
"""

import sqlite3

def connect_db():
    """
    Function to connect to the database
    """
    return sqlite3.connect('personal_finance.db')

def display_all_accounts(connection):
    """
    Display all account balances.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT account_id, name, balance FROM Accounts")
    accounts = cursor.fetchall()
    for account in accounts:
        print(f"Account ID: {account[0]}, Account Name: {account[1]}, Balance: {account[2]}\n")

def display_selected_account_by_id(connection, account_id):
    """
    Function to display balance of selected account by ID
    """
    cursor = connection.cursor()
    cursor.execute("SELECT name, balance FROM Accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    if account:
        print(f"Account ID: {account_id}, Account Name: {account[0]}, Balance: {account[1]}")
    else:
        print(f"No account found with ID: {account_id}")

def display_selected_account_by_name(connection, account_name):
    """ 
    Function to display balance of selected account by name
    """
    cursor = connection.cursor()
    cursor.execute("SELECT account_id, balance FROM Accounts WHERE name = ?", (account_name,))
    account = cursor.fetchone()
    if account:
        print(f"Account Name: {account_name}, Account ID: {account[0]}, Balance: {account[1]}\n")
    else:
        print(f"No account found with name: {account_name}\n")

def show_balance():
    """ 
    Main function
    """
    connection = connect_db()
    try:
        while True:
            choice = input(
                "\nEnter '1' to show balance of all accounts,\n"
                "'2' to show balance by an account ID,\n"
                "'3' to show balance of an account by name,\n"
                "or '4' to exit the program: "
            ).strip()

            if choice == '1':
                display_all_accounts(connection)
            elif choice == '2':
                account_id = input("Enter the account ID: ").strip()
                if account_id.isdigit():
                    display_selected_account_by_id(connection, account_id)
                else:
                    print("Invalid account ID. Please enter a numeric value.")
            elif choice == '3':
                account_name = input("Enter the account name: ").strip()
                display_selected_account_by_name(connection, account_name)
            elif choice == '4':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter '1', '2', '3', or '4'.\n")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()