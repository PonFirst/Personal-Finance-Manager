"""
This module is use for displaying the user dashboard and getting
user inputs to call functions like initialize account chart,
account management, transaction management, and budget management.
"""

import initialize_account as init_acc
from budget_management import Budget
import add_transaction
import search_transaction
import delete_transaction
import show_transaction
import add_account
import delete_account
import show_account_balance
import account_database


def display_dashboard():
    """
    This function is use to display the dashboard.
    """
    while True:
        print("----User Dashboard----")
        print("1. Initialize account chart")
        print("2. Account Management")
        print("3. Transaction Management")
        print("4. Budget Management")
        print("5. Exit")

        try:
            choice = int(input("Select an option: "))
            if choice == 1:
                initialize_account_chart()
            elif choice == 2:
                account_management()
            elif choice == 3:
                transaction_management()
            elif choice == 4:
                budget_interface()
            elif choice == 5:
                break
            else:
                print("Invalid Choice!\n")
        except ValueError:
            print("Invalid Choice!\n")


def initialize_account_chart():
    """
    This function allow the user to choose to initialize
    account by using template or their own.
    """
    print("1. Use Template")
    print("2. Upload A Template")

    try:
        choice = int(input("Choose a option: "))
        if choice == 1:
            init_acc.use_template("Finance Template.csv")
        elif choice == 2:
            init_acc.upload_template()
        else:
            print("Invalid Choice!")
    except ValueError:
        print("Invalid Choice!")


def account_management():
    """
    This function allow the user to choose to
    add, delete, or show account balance.
    """
    print("1. Add account")
    print("2. Delete account")
    print("3. Show account balance")

    try:
        choice = int(input("Choose a option: "))
        if choice == 1:
            account_database.create_account_table()
            add_account.add_account()
        elif choice == 2:
            delete_account.delete_account()
        elif choice == 3:
            show_account_balance.show_balance()
        else:
            print("Invalid Choice!")
    except ValueError:
        print("Invalid Choice!")


def transaction_management():
    print("1. Add Transaction")
    print("2. Search Transaction")
    print("3. Delete Transaction")
    print("4. View Transaction")

    try:
        choice = int(input("Choose a option: "))
        if choice == 1:
            add_transaction.add_transaction()
        elif choice == 2:
            search_transaction.search_transaction()
        elif choice == 3:
            delete_transaction.delete_transaction()
        elif choice == 4:
            show_transaction.show_transactions()
        else:
            print("Invalid Choice!")
    except ValueError:
        print("Invalid Choice!")


def budget_interface():
    """
    This function allow the user to choose to
    add budget, delete budget, modify budget 
    or view budget report.
    """
    print("1. Add Budget")
    print("2. Modify Budget")
    print("3. Delete Budget")
    print("4. View Budget Report")
    budget = Budget()
    try:
        choice = int(input("Choose a option: "))
        if choice == 1:
            budget.add_budget()
        elif choice == 2:
            budget.modify_budget()
        elif choice == 3:
            budget.delete_budget()
        elif choice == 4:
            budget.create_budget_report()
        else:
            print("Invalid Choice!")
    except ValueError:
        print("Invalid Choice!")
