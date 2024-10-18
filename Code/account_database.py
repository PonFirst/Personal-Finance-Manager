"""
Test program using sqlite with Python
https://www.geeksforgeeks.org/sql-using-python/
Run the program first and then:
Type "sqlite3 personal_finance.db" to run
Type ".tables" to see the Accounts table
"""
import sqlite3

connection = sqlite3.connect("personal_finance.csv")

cursor = connection.cursor()

def create_account_table():
    # SQL command to create a table in the database
    sql_command = """CREATE TABLE Accounts (
    account_id INTEGER PRIMARY KEY, 
    name VARCHAR(64), 
    category VARCHAR(16), 
    amount FLOAT
    );"""
    
    cursor.execute(sql_command)



connection.close()
