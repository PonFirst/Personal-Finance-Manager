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
    account_database.clear_account_table()
    account_database.clear_transactions_table()
    account_database.clear_budget_table()

    account_database.create_account_table()
    account_database.create_transactions_table()
    account_database.create_budget_table()

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            account_id, name, category, balance = row
            if category == "Expense":
                balance = 0.0
            else:
                balance = float(balance)

            account = Account(int(account_id), name, category, balance)
            account_database.insert_account(account)

    print(f"Accounts from {csv_file} have been successfully loaded into the database.")


def upload_template():
    """
    This function initializes the account database with
    the template accounts from a CSV file.
    """
    filename = input("Enter the name of the file you want to use: ")
    
    if not filename.endswith(".csv"):
        print("Error: The file must be in CSV format.")
    else:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader)  # Read the header row

                required_columns = ["Account_ID", "Name", "Category", "Balance"]
                valid_columns = validate_header(header, required_columns)

                if not valid_columns:
                    print("Errors in the file header prevent loading the template.")
                    valid_columns = False

                accounts = set()
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

                    # Check for duplicates
                    if account_id in accounts:
                        print(f"Error: Duplicate account ID '{account_id}' detected.")
                        all_rows_valid = False
                        continue
                    accounts.add(account_id)

                    # Validate Balance is a valid number
                    if not is_valid_balance(balance):
                        print(f"Error: Balance '{balance}' must be a valid number.")
                        all_rows_valid = False
                        continue

                if all_rows_valid:
                    use_template(filename)
                else:
                    print("Errors in the file prevent loading the template.")

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found. Please check the file name and try again.")


def validate_header(header, required_columns):
    """
    This function checks if the CSV file header matches the required columns exactly.
    """
    if len(header) != len(required_columns):
        print(f"Error: Expected {len(required_columns)} columns, but found {len(header)} columns.")
        return False

    for i, required_col in enumerate(required_columns):
        if header[i] != required_col:
            print(f"Error: Column {i + 1} must be '{required_col}', found '{header[i]}' instead.")
            return False
    return True


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

