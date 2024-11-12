""" 
delete_account.py
Function to delete account from the account database
Created by Baipor 
"""

import sqlite3

def delete_account():
    """
    Function to delete an account and its related transactions and budget
    """
    # Prompt user to choose deletion method
    method = input("Enter '1' to delete the account by name or '2' to delete by ID: ").strip()

    # Connect to the SQLite database
    connection = sqlite3.connect('personal_finance.db')
    cursor = connection.cursor()

    if method == '1':
        # Get account name
        account_name = input("Enter account name: ").strip()

        # Check if the account name exists
        cursor.execute('SELECT account_id FROM Accounts WHERE name = ?', (account_name,))
        account = cursor.fetchone()

        if account is None:
            print("Error: Account name does not exist.")
            connection.close()
            return
        else:
            account_id = account[0]

    elif method == '2':
        # Get account ID
        account_id = input("Enter account ID: ").strip()

        # Check if the account ID exists
        cursor.execute('SELECT name FROM Accounts WHERE account_id = ?', (account_id,))
        account = cursor.fetchone()

        if account is None:
            print("Error: Account ID does not exist.")
            connection.close()
            return
        else:
            account_name = account[0]

    else:
        print("Invalid choice. Please enter '1' or '2'.")
        connection.close()
        return

    # Ask for confirmation
    confirmation = input(f"Are you sure you want to delete the account '{account_name}' and all its related data? "
                         "Type 'Y' to confirm or 'N' to cancel: ").strip().lower()

    if confirmation == 'y':
        try:
            # Delete the account's transactions if they exist
            cursor.execute('DELETE FROM Transactions WHERE account_id = ?', (account_id,))
            if cursor.rowcount > 0:
                print("Transactions deleted successfully!")
            else:
                print("No transactions found for this account.")

            # Delete the account's budget if it exists
            cursor.execute('DELETE FROM Budgets WHERE account_id = ?', (account_id,))
            if cursor.rowcount > 0:
               print("Budget deleted successfully!")
            else:
               print("No budget found for this account.")

            # Delete the account from the database
            cursor.execute('DELETE FROM Accounts WHERE account_id = ?', (account_id,))
            print("Account deleted successfully!")

            # Commit the changes
            connection.commit()
            print("Account and its related data deleted successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    else:
        print("Account deletion canceled.")

    # Close the connection
    connection.close()