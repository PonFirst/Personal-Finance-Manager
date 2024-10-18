import initialize_account as init_acc
import budget_report as br


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
                pass
            elif choice == 3:
                pass
            elif choice == 4:
                br.create_budget_report()
            elif choice == 5:
                break
            else:
                print("Invalid Choice!")
        except ValueError:
            print("Invalid Choice!")
            
            
def initialize_account_chart():
    print("1. Use Template")
    print("2. Upload A Template")
    
    try:
        choice = int(input("Choose a option: "))
        if choice == 1:
            init_acc.use_template()
        elif choice == 2:
            init_acc.upload_template()
        else:
            print("Invalid Choice!")
    except ValueError:
        print("Invalid Choice!")
