import initialize_account as init_acc
from budget_management import Budget
import add_account
import delete_account
import show_account_balance
import account_database


def display_dashboard():
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
                pass
            elif choice == 4:
                budget_interface()
            elif choice == 5:
                break
            else:
                print("Invalid Choice!\n")
        except ValueError:
            print("Invalid Choice!\n")
            
            
def initialize_account_chart():
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



def budget_interface():
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