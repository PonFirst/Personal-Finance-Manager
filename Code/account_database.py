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

# Create Account table
def create_account_table():
    sql_command = """CREATE TABLE IF NOT EXISTS Accounts (
        account_id INTEGER PRIMARY KEY,
        name VARCHAR(64) NOT NULL,
        category VARCHAR(16) NOT NULL,
        balance FLOAT NOT NULL
    );"""
    cursor.execute(sql_command)

# Create Transactions table
def create_transactions_table():
    sql_command = """CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INTEGER PRIMARY KEY,
        source_account_id INTEGER NOT NULL,
        destination_account_id INTEGER NOT NULL,
        amount FLOAT NOT NULL,
        date DATE NOT NULL,
        description TEXT,
        FOREIGN KEY (source_account_id) REFERENCES Accounts(account_id),
        FOREIGN KEY (destination_account_id) REFERENCES Accounts(account_id)
    );"""
    cursor.execute(sql_command)
    
# Create Budget table
def create_budget_table():
    sql_command = """CREATE TABLE IF NOT EXISTS Budgets (
        budget_id INTEGER PRIMARY KEY,
        category VARCHAR(64) NOT NULL,
        budgeted_amount FLOAT NOT NULL,
    );"""
    cursor.execute(sql_command)

connection.commit()
connection.close()