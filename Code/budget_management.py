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