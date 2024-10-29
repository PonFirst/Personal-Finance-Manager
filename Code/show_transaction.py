'''
Show all transactions in the file personal_finance.db file
'''

import sqlite3

def show_transactions(db_path):
    '''
    Function to show all transactions in the database
    '''
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute a query to select all transactions
        cursor.execute("SELECT * FROM transactions")
        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Get column names from the cursor description
        column_names = [description[0] for description in cursor.description]
        print(f"{' | '.join(column_names)}")  # Print the header
        print('-' * 50)  # Print a line

        # Print each row with column names
        for row in rows:
            row_dict = dict(zip(column_names, row))
            for column, value in row_dict.items():
                if column == 'id':      # change from printing id to transaction
                    print(f"transaction: {value}")
                else:
                    print(f"{column}: {value}")
            print('-' * 50)  # Print a line between rows

        # Close the connection
        conn.close()

    except sqlite3.OperationalError as _:
        print(f"An error occurred: {_}")

# Main function to run the script
if __name__ == "__main__":
    FILE_PATH = 'personal_finance.db'  # Define the file path
    show_transactions(FILE_PATH)
