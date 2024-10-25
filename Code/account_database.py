import sqlite3

# Create Account table
def create_account_table():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    sql_command = """CREATE TABLE IF NOT EXISTS Accounts (
        account_id INTEGER PRIMARY KEY,
        name VARCHAR(64) NOT NULL,
        category VARCHAR(16) NOT NULL,
        balance FLOAT NOT NULL
    );"""
    cursor.execute(sql_command)
    connection.commit()
    connection.close()

# Create Transactions table
def create_transactions_table():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
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
    connection.commit()
    connection.close()
    
# Create Budget table
def create_budget_table():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    sql_command = """CREATE TABLE IF NOT EXISTS Budgets (
        budget_id INTEGER PRIMARY KEY,
        category VARCHAR(64) NOT NULL,
        budgeted_amount FLOAT NOT NULL
    );"""
    cursor.execute(sql_command)
    connection.commit()
    connection.close()

# Insert account
def insert_account(account):
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    
    sql_command = """INSERT INTO Accounts (account_id, name, category, balance) VALUES (?, ?, ?, ?);"""
    
    try:
        cursor.execute(sql_command, (account.account_id, account.name, account.category, account.balance))
        connection.commit()
    except sqlite3.IntegrityError:
        print(f"Account ID {account.account_id} already exists. Skipping this entry.")
    finally:
        connection.close()