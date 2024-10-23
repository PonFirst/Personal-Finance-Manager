import sqlite3


# Prompt the user to enter a valid category name.
def get_valid_category(prompt):
    while True:
        new_category = input(prompt).strip()
        if not new_category:
            print("Invalid budget name! Please enter a non-empty category name.")
        else:
            return new_category
        
# Add budget
def add_budget():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    
    while True:
        category = get_valid_category("Enter the category for your budget: ")
        
        # Check for blank category name
        if not category:
            print("Invalid budget name!")
            continue 
        
        try:
            amount = float(input("Enter the amount of your budget: "))
        except ValueError:
            print("Invalid budget amount!")
            continue

        # Check for negative budget amount
        if amount < 0:
            print("Invalid budget amount!")
            continue
        
        cursor.execute("SELECT budgeted_amount FROM Budgets WHERE category = ?", (category,))
        existing_budget = cursor.fetchone()
        
        if existing_budget:
            print(f"Budget name '{category}' already exists with amount: {existing_budget[0]:.2f}. Skipping creation.")
            break
        else:
            cursor.execute('''
                INSERT INTO Budgets (category, budgeted_amount) VALUES (?, ?)
            ''', (category, amount))
            print(f"Budget for '{category}' added with amount: {amount:.2f}.")
            break 
    
    connection.commit()
    connection.close()

    
    
    

# Modify an existing budget category and/or its amount.
def modify_budget():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    
    category = get_valid_category("Enter the category for your budget you want to modify: ")
    
    # Check if the budget category exists
    cursor.execute("SELECT budgeted_amount FROM Budgets WHERE category = ?", (category,))
    existing_budget = cursor.fetchone()
    
    if existing_budget:
        print(f"Current budget for '{category}' is {existing_budget[0]:.2f}.")
        
        # Ask the user if they want to modify the category name
        modify_name = input("Do you want to modify the category name? (y/n): ").lower()
        new_category = category
        
        if modify_name == "y":
            new_category = get_valid_category("Enter the new category name: ")
        
        # Ask the user to modify the budget amount
        modify_amount = input("Do you want to modify the budget amount? (y/n): ").lower()
        
        if modify_amount == "y":
            while True:
                try:
                    amount = float(input("Enter the new amount of your budget: "))
                    if amount < 0:
                        print("Invalid budget amount!")
                        continue
                    break
                except ValueError:
                    print("Invalid budget amount!")

            cursor.execute('''
                UPDATE Budgets
                SET budgeted_amount = ?
                WHERE category = ?
            ''', (amount, category))
            print(f"Budget for '{category}' has been updated to {amount:.2f}.")
            
        if modify_name == "y" and new_category != category:
            cursor.execute('''
                UPDATE Budgets
                SET category = ?
                WHERE category = ?
            ''', (new_category, category))
            print(f"Budget category has been changed from '{category}' to '{new_category}'.")
        
    else:
        print(f"Budget category '{category}' doesn't exist!")
        
    connection.commit()
    connection.close()
    
# Delete budget
def delete_budget():
    connection = sqlite3.connect("personal_finance.db")
    cursor = connection.cursor()
    
    category = get_valid_category("Enter the category for your budget you want to delete: ")
        
    cursor.execute("SELECT budgeted_amount FROM Budgets WHERE category = ?", (category,))
    existing_budget = cursor.fetchone()
    
    if existing_budget:
        print(f"Current budget for '{category}' is {existing_budget[0]:.2f}.")
        confirm = input("Confirm you want to delete (y/n): ").lower()
        
        if confirm == "y":
            cursor.execute("DELETE FROM Budgets WHERE category = ?", (category,))
            print(f"Budget for '{category}' has been deleted.")
        else:
            print("Budget deletion have been cancelled.")
    else:
        print(f"Budget category '{category}' doesn't exists!")
        
    connection.commit()
    connection.close()

# Create Budget report
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
    
    cursor.execute("SELECT category, budgeted_amount FROM Budgets")
    budgets = cursor.fetchall()
    
    print("Budget Report:")
    for budget in budgets:
        category, budgeted_amount = budget
        print(f"{category:<20} {budgeted_amount:<10.2f}")
    
    connection.commit()
    connection.close()