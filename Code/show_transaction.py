'''
Show all transactions in the file personal_finance.db file
Created by Copter
'''

import sqlite3

#    Function to show all transactions in the database
def show_transactions():
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("personal_finance.db")
        cursor = conn.cursor()

        # Execute a query to select all transactions
        cursor.execute("SELECT * FROM Transactions;")
        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Get column names from the cursor description
        column_names = [description[0] for description in cursor.description]
        # print(f"{' | '.join(column_names)}")  
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

    # Handle error if file not found
    except sqlite3.OperationalError as _:
        print(f"An error occurred: {_}")
