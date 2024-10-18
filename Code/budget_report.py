import sqlite3


def create_budget_report():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    
    # Create the Budgets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Budgets (
            budget_id INTEGER PRIMARY KEY,
            category VARCHAR(64) NOT NULL,
            budgeted_amount FLOAT NOT NULL
        );
    ''')

    sample_budgets = [
        ("Groceries", 300.00),
        ("Rent", 1200.00),
        ("Utilities", 200.00),
        ("Transportation", 150.00),
        ("Entertainment", 100.00),
        ("Savings", 500.00)
    ]

    for category, budgeted_amount in sample_budgets:
        cursor.execute('''
            INSERT OR IGNORE INTO Budgets (category, budgeted_amount) VALUES (?, ?)
        ''', (category, budgeted_amount))
    
    cursor.execute("SELECT category, budgeted_amount FROM Budgets")
    budgets = cursor.fetchall()
    
    print("Budget Report:")
    for budget in budgets:
        category, budgeted_amount = budget
        print(f"{category:<20} {budgeted_amount:<10.2f}")
    
    connection.close()
    