# Delete account from the account database

import sqlite3

def delete_account():
    # Get account name
    account_name = input("Enter account name: ")

    # Connect to the SQLite database
    connection = sqlite3.connect('personal_finance.db')
    cursor = connection.cursor()

    # Check if the account name exists
    cursor.execute('SELECT * FROM Accounts WHERE name = ?', (account_name,))
    account = cursor.fetchone()

    if account is None:
        print("Error: Account name does not exist.")
    else:
        # Ask for confirmation
        confirmation = input(f"Are you sure to delete the account '{account_name}'? Type 'yes' to confirm or 'no' to cancel: ").strip().lower()
        if confirmation == 'yes':
            # Delete the account from the database
            cursor.execute('DELETE FROM Accounts WHERE name = ?', (account_name,))
            
            # Commit the changes and close the connection
            connection.commit()
            print("Account deleted successfully!")
        else:
            print("Account deletion canceled.")

    connection.close()

def main():
    delete_account()

if __name__ == "__main__":
    main()