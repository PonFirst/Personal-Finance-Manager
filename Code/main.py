import pandas as pd


def initialize_account_chart():
    print("1. Use Template")
    print("2. Upload A Template")
    
    try:
        choice = int(input(""))
        if choice == 1:
            pass
        elif choice == 2:
            pass
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid choice")



def main():
    print("Welcome to Personal Finance Manager")
    initialize_account_chart()
    
    
if __name__ == '__main__':
    main()