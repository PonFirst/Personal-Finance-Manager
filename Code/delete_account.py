# Delete account from the account database
# Remove the available account and all the information inside the database of the account.

import sqlite3

def delete_account():
    # Get account ID
    account_id = input("Enter account ID: ")

    # Connect to the SQLite database
    connection = sqlite3.connect('account_database.db')
    cursor = connection.cursor()

    # Check if the account ID exists
    cursor.execute('SELECT * FROM accounts WHERE account_id = ?', (account_id,))
    account = cursor.fetchone()

    if account is None:
        print("Error: Account ID does not exist.")
    else:
        # Delete the account from the database
        cursor.execute('DELETE FROM accounts WHERE account_id = ?', (account_id,))
        
        # Commit the changes and close the connection
        connection.commit()
        print("Account deleted successfully!")

    connection.close()

def main():
    delete_account()

if __name__ == "__main__":
    main()