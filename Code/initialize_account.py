"""
This module is use to initialize the account table based on the template or
the user own template.
Created by Pon (First) Yimcharoen
"""

import csv
import account_database
from account import Account


def use_template(csv_file):
    """
    This function is use to initialize the account database with
    the template accounts.
    """
    account_database.create_account_table()
    account_database.create_transactions_table()
    account_database.create_budget_table()

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            account_id, name, category, balance = row
            account = Account(int(account_id), name, category, float(balance))

            account_database.insert_account(account)

    print(f"Accounts from {csv_file} have been successfully loaded into the database.")


def upload_template():
    """
    This function initializes the account database with
    the template accounts from a CSV file.
    """
    filename = input("Enter the name of the file you want to use: ")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header row

            required_columns = ["Account_ID", "Name", "Category", "Balance"]
            valid_columns = True

            # Validate the header
            if len(header) < len(required_columns):
                print("Error: Missing columns in the file header.")
                valid_columns = False
            else:
                for i, required_col in enumerate(required_columns):
                    if i < len(header) and header[i] != required_col:
                        print(f"Error: Column {i + 1} must be '{required_col}'.")
                        valid_columns = False

            # Process rows only if header is valid
            if valid_columns:
                all_rows_valid = True
                for row in reader:
                    if len(row) < len(required_columns):
                        print("Error: Missing values in a row.")
                        all_rows_valid = False
                        continue

                    account_id, name, category, balance = row

                    # Validate Account ID format based on Category
                    if not is_valid_account_id(account_id, category):
                        print(f"Error: Account ID '{account_id}' is invalid for category '{category}'.")
                        all_rows_valid = False
                        continue

                    # Validate Balance is a valid number
                    if not is_valid_balance(balance):
                        print(f"Error: Balance '{balance}' must be a valid number.")
                        all_rows_valid = False
                        continue

                if all_rows_valid:
                    use_template(filename)
                else:
                    print("Errors in the file prevent loading the template.")

            else:
                print("Errors in the file header prevent loading the template.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Please check the file name and try again.")



def is_valid_account_id(account_id, category):
    """
    Validate the account ID based on the category.
    """
    if category == "Income" and account_id.startswith('1'):
        return True
    elif category == "Expense" and account_id.startswith('2'):
        return True
    elif category == "Asset" and account_id.startswith('3'):
        return True
    elif category == "Liability" and account_id.startswith('4'):
        return True
    return False


def is_valid_balance(balance):
    """
    Validate that the balance is a valid number.
    """
    try:
        float(balance)
        return True
    except ValueError:
        return False
