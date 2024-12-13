"""
This module is use to create the account table, transaction table,
budget table, and inserting new accounts into the account table.
Created by Pon (First) Yimcharoen
"""

import sqlite3


# This function is use to create the account table.
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

# This function is use to clear the account table.
def clear_account_table():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Accounts;")
    connection.commit()
    connection.close()

# This function is use to create the transaction table.
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

# This function is use to clear the transaction table.
def clear_transactions_table():
    """
    This function is use to clear the transaction table.
    """
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Transactions;")
    connection.commit()
    connection.close()

# This function is use to create the budget table.
def create_budget_table():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Budgets (
            budget_id INTEGER PRIMARY KEY,
            category VARCHAR(64) NOT NULL,
            account_id INTEGER,
            budgeted_amount FLOAT NOT NULL,
            actual_expense FLOAT NOT NULL DEFAULT 0.0,
            FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
        );
    ''')

    connection.commit()
    connection.close()

# This function is use to clear the budget table.
def clear_budget_table():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Budgets;")
    connection.commit()
    connection.close()


def insert_account(account):
    """
    This function is use to insert the account into the account table.
    """
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()

    sql_command = """INSERT INTO Accounts (account_id, name, category, balance)
    VALUES (?, ?, ?, ?);"""

    try:
        cursor.execute(sql_command, (account.account_id, account.name,
                                     account.category, account.balance))
        connection.commit()
    except sqlite3.IntegrityError:
        print(f"Account ID {account.account_id} already exists. Skipping this entry.")
    finally:
        connection.close()
