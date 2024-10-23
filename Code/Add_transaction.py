import datetime
import csv

# Function to validate bank number
def validate_bank_number(bank_number):
    return bank_number.isdigit() and len(bank_number) == 4  # assuming 4 digits

# Function to validate the amount
def validate_amount(amount):
    try:
        amount = float(amount)
        return amount > 0
    except ValueError:
        return False

# Function to validate date and time input
def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

# Function to add transaction to the record
def add_transaction():
    # Ask for bank number
    while True:
        bank_number = input("Enter destination bank number (4 digits): ")
        if validate_bank_number(bank_number):
            break
        else:
            print("Invalid bank number. Please enter a 4-digit number.")

    # Ask for transaction amount
    while True:
        amount = input("Enter the transaction amount: ")
        if validate_amount(amount):
            amount = float(amount)
            break
        else:
            print("Invalid amount. Please enter a positive number.")

    # Ask for description
    description = input("Enter a description for the transaction: ")

    # Ask for transaction date and time
    while True:
        transaction_date = input("Enter transaction date and time (format: YYYY-MM-DD HH:MM:SS): ")
        if validate_date(transaction_date):
            break
        else:
            print("Invalid date format. Please enter a valid date and time (YYYY-MM-DD HH:MM:SS).")

    # Prepare transaction record
    transaction = {
        "bank_number": bank_number,
        "amount": amount,
        "description": description,
        "date": transaction_date
    }
    
    # Confirm transaction details with user
    print("Want to record the following transaction? :")
    print(f"Bank number: {transaction['bank_number']}")
    print(f"Amount: {transaction['amount']}")
    print(f"Description: {transaction['description']}")
    print(f"Date: {transaction['date']}")
    confirmation = input(" Y for Yes, N for No: ").upper()
    if confirmation == 'N':
        print("Transaction cancelled.")
        return
    elif confirmation == 'Y':
        print("Transaction confirmed.")
    else: 
        print("Invalid input. Transaction cancelled.")
        return
    
    
    # Append to a CSV file
    with open('transactions.csv', 'a', newline='') as csvfile:
        fieldnames = ['bank_number', 'amount', 'description', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        
        writer.writerow(transaction)
        
        print("Transaction added successfully!")
        print(transaction)

# Call function to add transaction
add_transaction()
