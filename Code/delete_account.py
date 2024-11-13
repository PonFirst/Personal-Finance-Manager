""" 
delete_account_2.py
Function to delete account from the account database
account can be deleted if there are no associated transactions or budgets
Created by Baipor 
"""

import sqlite3

# Function to delete account from the database 
# if there are no associated transactions or budgets
def delete_account():

    # Connect to the SQLite database
    connection = sqlite3.connect('personal_finance.db')
    cursor = connection.cursor()

    while True:
        # ask user to choose option
        option = input("Enter '1' to delete the account by name, '2' to delete by ID, or 'cancel' to exit: ").strip()

        # if option is cancel, close the connection and return
        if option == 'cancel':
            connection.close()
            return
        # if option is 1, get account name
        elif option == '1':
            # get account name
            account_name = input("Enter account name, or 'cancel' to exit: ").strip()

            if account_name == 'cancel':
                connection.close()
                return

            # Check if the account name exists
            cursor.execute('SELECT account_id FROM Accounts WHERE name = ?', (account_name,))
            account = cursor.fetchone()

            if account is None:
                print("Error: Account name does not exist.")
                continue
            else:
                account_id = account[0]
                break

        #if option is 2, get account ID
        elif option == '2':
            # Get account ID
            account_id = input("Enter account ID, or 'cancel' to exit: ").strip()

            if account_id == 'cancel':
                connection.close()
                return

            # Check if the account ID exists
            cursor.execute('SELECT name FROM Accounts WHERE account_id = ?', (account_id,))
            account = cursor.fetchone()

            if account is None:
                print("Error: Account ID does not exist.")
                continue
            else:
                account_name = account[0]
                break

        else:
            print("Invalid choice. Please enter '1' or '2'.")

    # Check for associated transactions
    # if there are associated transactions, print error message and return
    cursor.execute('SELECT COUNT(*) FROM Transactions WHERE source_account_id = ? OR destination_account_id = ?', (account_id, account_id))
    transaction_count = cursor.fetchone()[0]

    if transaction_count > 0:
        print(f"Cannot delete account '{account_name}' because it has associated transactions.")
        connection.close()
        return

    # Check for associated budgets
    # if there are associated budgets, print error message and return
    cursor.execute('SELECT COUNT(*) FROM Budgets WHERE account_id = ?', (account_id,))
    budget_count = cursor.fetchone()[0]

    if budget_count > 0:
        print(f"Cannot delete account '{account_name}' because it has associated budgets.")
        connection.close()
        return

    # Ask for confirmation
    confirmation = input("Are you sure you want to delete the account '{account_name}'? "
                         "Type 'Y' to confirm or 'N' to cancel: ").strip().lower()

    #if user confirm, delete the account
    if confirmation == 'y':
        try:
            # Delete the account from the database
            cursor.execute('DELETE FROM Accounts WHERE account_id = ?', (account_id,))
            print("Account deleted successfully!")

            # Commit the changes
            connection.commit()
            print("Account and its related data deleted successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    #if user cancel, cancel the deletion
    else:
        print("Account deletion canceled.")

    # Close the connection
    connection.close()

