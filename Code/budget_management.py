"""
This module is use to define the budgets class and its modules.
Created by Pon (First) Yimcharoen
"""


import sqlite3

# This class manages budget functionalities including adding, modifying,
# deleting, and printing budget reports.
class Budget:
    def __init__(self, db_name="personal_finance.db"):
        self.db_name = db_name

    def _connect(self):
        return sqlite3.connect(self.db_name)

    # This function asks the user to enter a valid category name.
    def get_valid_category(self, prompt):
        while True:
            new_category = input(prompt).strip()
            if not new_category:
                print("Invalid budget name! Please enter a non-empty category name.")
            else:
                return new_category

    # This function is used to add a budget with specified category, amount, and account ID.
    def add_budget(self):
        connection = self._connect()
        cursor = connection.cursor()

        while True:
            category = self.get_valid_category("Enter the category for your budget (Or type cancel to exit): ")
            if category.lower() == "cancel":
                print("Operation canceled.")
                break

            # Check if the category already exists in Budgets
            cursor.execute("SELECT budgeted_amount, account_id FROM Budgets WHERE category = ?", (category,))
            existing_budget = cursor.fetchone()

            if existing_budget:
                print(f"Category '{category}' already exists with a budget of {existing_budget[0]:.2f},"
                    f" linked to Account ID: {existing_budget[1]}.")
                continue

            account_id = input("Enter the account ID of this budget (Expense type): ").strip()

            # Verify that the account ID is valid and of type 'Expense'
            cursor.execute("SELECT name, category FROM Accounts WHERE account_id = ?", (account_id,))
            account_info = cursor.fetchone()

            if account_info and account_info[1] == "Expense":
                try:
                    amount = float(input("Enter the amount of your budget: "))
                    if amount < 0:
                        raise ValueError("Budget amount cannot be negative.")
                except ValueError as error:
                    print(f"Invalid budget amount! {error}")
                    continue

                # Insert the new budget
                cursor.execute(
                    "INSERT INTO Budgets (category, budgeted_amount, account_id, actual_expense) VALUES (?, ?, ?, ?)",
                    (category, amount, account_id, 0.0)
                )
                print(f"Budget for '{category}' added with amount: {amount:.2f} linked to account '{account_id}'.")
                break  # Exit after successful addition

            else:
                print(f"Invalid or non-expense account ID '{account_id}'. Please enter a valid Expense account ID.")

        connection.commit()
        connection.close()

    # This function is use to modify an existing budget's amount or linked account.
    def modify_budget(self):
        connection = self._connect()
        cursor = connection.cursor()

        category = self.get_valid_category("Enter the category of the budget to modify (Or type cancel to exit): ")
        if category.lower() == "cancel":
            print("Operation canceled.")
            return
        cursor.execute("SELECT budgeted_amount, account_id FROM Budgets WHERE category = ?",
                        (category,))
        existing_budget = cursor.fetchone()

        if existing_budget:
            print(f"Current budget for '{category}': {existing_budget[0]:.2f}, "
                  f"Account ID: {existing_budget[1]}")

            # Modify the budget amount
            try:
                amount = float(input("Enter the new budget amount: "))
                if amount < 0:
                    raise ValueError("Amount cannot be negative.")
                cursor.execute("UPDATE Budgets SET budgeted_amount = ? WHERE category = ?",
                               (amount, category))
                print(f"Budget for '{category}' updated to {amount:.2f}.")
            except ValueError as error:
                print(f"Invalid budget amount! {error}")

            # Modify associated account
            while True:
                modify_account = input("Change the associated account? (y/n): ").strip().lower()
                if modify_account == "y":
                    account_id = input("Enter the new account ID (Expense type only): ").strip()
                    cursor.execute("SELECT category FROM Accounts WHERE account_id = ?",
                                   (account_id,))
                    account_category = cursor.fetchone()

                    if account_category and account_category[0] == "Expense":
                        cursor.execute("UPDATE Budgets SET account_id = ? WHERE category = ?",
                                       (account_id, category))
                        print(f"Budget '{category}' is now linked to account '{account_id}'.")
                    else:
                        print("Invalid or non-expense account ID.")
                    break
                if modify_account == "n":
                    print("No changes made to the associated account.")
                    break
                print("Invalid input! Please enter 'y' or 'n'.")

        else:
            print(f"Budget category '{category}' not found.")

        connection.commit()
        connection.close()

    # This function is use to delete a budget.
    def delete_budget(self):
        connection = self._connect()
        cursor = connection.cursor()

        category = self.get_valid_category("Enter the category of the budget to delete (Or type cancel to exit): ")
        if category.lower() == "cancel":
            print("Operation canceled.")
            return
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

    # This function generates a report comparing actual expenses with the budgeted amounts.
    def create_budget_report(self):
        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT budget_id, category, budgeted_amount, account_id, actual_expense
            FROM Budgets
        ''')
        budgets = cursor.fetchall()

        if not budgets:  # If the budgets list is empty
            print("No Budget")
        else:
            print("Budget vs. Actual Expense Report:")
            for budget in budgets:
                budget_id, category, budgeted_amount, account_id, current_actual_expense = budget

                cursor.execute('''
                    SELECT SUM(amount) 
                    FROM Transactions 
                    WHERE source_account_id = ?
                ''', (account_id,))
                
                actual_expense = cursor.fetchone()[0] or 0
                
                # Update the actual_expense in the Budgets table
                if current_actual_expense != actual_expense:
                    cursor.execute('''
                        UPDATE Budgets 
                        SET actual_expense = ? 
                        WHERE budget_id = ?
                    ''', (actual_expense, budget_id))

                # Display the budget table
                print(f"Category: {category:<20} "
                    f"Account ID: {account_id:<10} "
                    f"Budgeted: {budgeted_amount:<10.2f} "
                    f"Actual Expense: {actual_expense:<10.2f} "
                    f"Difference: {budgeted_amount - actual_expense:.2f}")

        connection.commit()
        connection.close()
