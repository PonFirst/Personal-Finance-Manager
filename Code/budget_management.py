import sqlite3
from account import Account


def add_budget():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    
    category = input("Enter the category for your budget: ")
    
    amount = float(input("Enter the amount of your budget: "))
        
    cursor.execute("SELECT budgeted_amount FROM Budgets WHERE category = ?", (category,))
    existing_budget = cursor.fetchone()
    
    if existing_budget:
        print(f"Budget category '{category}' already exists with amount: {existing_budget[0]:.2f}. Skipping creation.")
    else:
        cursor.execute('''
            INSERT INTO Budgets (category, budgeted_amount) VALUES (?, ?)
        ''', (category, amount))
        print(f"Budget for '{category}' added with amount: {amount:.2f}.")
    
    connection.commit()
    connection.close()
    
    
def modify_budget():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    
    category = input("Enter the category for your budget you want to modify: ")
        
    cursor.execute("SELECT budgeted_amount FROM Budgets WHERE category = ?", (category,))
    existing_budget = cursor.fetchone()
    
    if existing_budget:
        print(f"Current budget for '{category}' is {existing_budget[0]:.2f}.")
        amount = float(input("Enter the amount of your budget: "))
        
        cursor.execute('''
            UPDATE Budgets
            SET budgeted_amount = ?
            WHERE category = ?
        ''', (amount, category))
        print(f"Budget for '{category}' has been updated to {amount:.2f}.")
    else:
        print(f"Budget category '{category}' doesn't exists!")
        
    connection.commit()
    connection.close()
    
    
def delete_budget():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    
    category = input("Enter the category for your budget you want to delete: ")
        
    cursor.execute("SELECT budgeted_amount FROM Budgets WHERE category = ?", (category,))
    existing_budget = cursor.fetchone()
    
    if existing_budget:
        print(f"Current budget for '{category}' is {existing_budget[0]:.2f}.")
        confirm = input("Confirm you want to delete (y/n)").lower()
        
        if confirm == "y":
            cursor.execute("DELETE FROM Budgets WHERE category = ?", (category,))
            print(f"Budget for '{category}' has been deleted.")
        else:
            print("Budget deletion have been cancelled.")
    else:
        print(f"Budget category '{category}' doesn't exists!")
        
    connection.commit()
    connection.close()


def create_budget_report():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Budgets (
            budget_id INTEGER PRIMARY KEY,
            category VARCHAR(64) NOT NULL UNIQUE,
            budgeted_amount FLOAT NOT NULL
        );
    ''')

    sample_budgets = [
        ("Groceries", 300.00),
        ("Rent", 1200.00),
        ("Utilities", 200.00),
        ("Transportation", 150.00),
        ("Entertainment", 100.00),
        ("Savings", 500.00),
    ]

    for category, budgeted_amount in sample_budgets:
        cursor.execute("SELECT COUNT(*) FROM Budgets WHERE category = ?", (category,))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO Budgets (category, budgeted_amount) VALUES (?, ?)
            ''', (category, budgeted_amount))
    
    cursor.execute("SELECT category, budgeted_amount FROM Budgets")
    budgets = cursor.fetchall()
    
    print("Budget Report:")
    for budget in budgets:
        category, budgeted_amount = budget
        print(f"{category:<20} {budgeted_amount:<10.2f}")
    
    connection.commit()
    connection.close()