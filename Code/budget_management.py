import sqlite3
from account import Account

class Budget:
    """
    This class manages budget functionalities including adding, modifying, 
    deleting, and printing budget reports.
    
    Created by Pon (First) Yimcharoen
    """
    
    def __init__(self, db_name="personal_finance.db"):
        self.db_name = db_name
    
    def _connect(self):
        return sqlite3.connect(self.db_name)
    
    # Prompt the user to enter a valid category name.
    def get_valid_category(self, prompt):
        while True:
            new_category = input(prompt).strip()
            if not new_category:
                print("Invalid budget name! Please enter a non-empty category name.")
            else:
                return new_category

    # Add budget with associated accounts
    def add_budget(self):
        connection = self._connect()
        cursor = connection.cursor()

        while True:
            category = self.get_valid_category("Enter the category for your budget: ")
            account_id = input("Enter the account ID to associate with this budget (Expense type): ").strip()
            
            # Check if the account is valid and an Expense account
            cursor.execute("SELECT name, category FROM Accounts WHERE account_id = ?", (account_id,))
            account_info = cursor.fetchone()
            
            if account_info and account_info[1] == "Expense":
                try:
                    amount = float(input("Enter the amount of your budget: "))
                    if amount < 0:
                        raise ValueError("Budget amount cannot be negative.")
                except ValueError as e:
                    print(f"Invalid budget amount! {e}")
                    continue
                
                cursor.execute('''
                    INSERT INTO Budgets (category, budgeted_amount, account_id) VALUES (?, ?, ?)
                ''', (category, amount, account_id))
                print(f"Budget for '{category}' added with amount: {amount:.2f} linked to account '{account_id}'.")
                break
            else:
                print(f"Invalid or non-expense account ID '{account_id}'. Please enter a valid Expense account ID.")
        
        connection.commit()
        connection.close()
    
    # Modify an existing budget category, amount, or linked account
    def modify_budget(self):
        connection = self._connect()
        cursor = connection.cursor()

        category = self.get_valid_category("Enter the category of the budget to modify: ")
        cursor.execute("SELECT budgeted_amount, account_id FROM Budgets WHERE category = ?", (category,))
        existing_budget = cursor.fetchone()
        
        if existing_budget:
            print(f"Current budget for '{category}': {existing_budget[0]:.2f}, Account ID: {existing_budget[1]}")
            
            # Modify the budget amount
            try:
                amount = float(input("Enter the new budget amount: "))
                if amount < 0:
                    raise ValueError("Amount cannot be negative.")
                cursor.execute("UPDATE Budgets SET budgeted_amount = ? WHERE category = ?", (amount, category))
                print(f"Budget for '{category}' updated to {amount:.2f}.")
            except ValueError as e:
                print(f"Invalid budget amount! {e}")
            
            # Modify associated account
            modify_account = input("Do you want to change the associated account? (y/n): ").strip().lower()
            if modify_account == "y":
                account_id = input("Enter the new account ID (Expense type only): ").strip()
                cursor.execute("SELECT category FROM Accounts WHERE account_id = ?", (account_id,))
                account_category = cursor.fetchone()
                
                if account_category and account_category[0] == "Expense":
                    cursor.execute("UPDATE Budgets SET account_id = ? WHERE category = ?", (account_id, category))
                    print(f"Budget '{category}' is now linked to account '{account_id}'.")
                else:
                    print("Invalid or non-expense account ID.")
        
        else:
            print(f"Budget category '{category}' not found.")
        
        connection.commit()
        connection.close()

    # Delete a budget
    def delete_budget(self):
        connection = self._connect()
        cursor = connection.cursor()
        
        category = self.get_valid_category("Enter the category of the budget to delete: ")
        cursor.execute("SELECT budgeted_amount FROM Budgets WHERE category = ?", (category,))
        existing_budget = cursor.fetchone()
        
        if existing_budget:
            confirm = input(f"Confirm deletion of budget '{category}'? (y/n): ").strip().lower()
            if confirm == "y":
                cursor.execute("DELETE FROM Budgets WHERE category = ?", (category,))
                print(f"Budget for '{category}' has been deleted.")
            else:
                print("Deletion canceled.")
        else:
            print(f"Budget category '{category}' not found.")
        
        connection.commit()
        connection.close()

    # Create a budget report
    def create_budget_report(self):
        connection = self._connect()
        cursor = connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Budgets (
                budget_id INTEGER PRIMARY KEY,
                category VARCHAR(64) NOT NULL,
                budgeted_amount FLOAT NOT NULL,
                account_id VARCHAR(10),
                FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
            );
        ''')

        cursor.execute('''
            SELECT Budgets.category, Budgets.budgeted_amount, Accounts.name AS account_name
            FROM Budgets
            LEFT JOIN Accounts ON Budgets.account_id = Accounts.account_id
        ''')
        
        budgets = cursor.fetchall()
        
        print("Budget Report:")
        for budget in budgets:
            category, budgeted_amount, account_name = budget
            print(f"Category: {category:<20} Amount: {budgeted_amount:<10.2f} Linked Account: {account_name}")
        
        connection.commit()
        connection.close()
