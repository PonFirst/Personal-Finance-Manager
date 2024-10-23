'''
delete transaction from the database
'''

import csv

# Function to delete transaction from the record
def delete_transaction(file_path, bank_number):
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            transactions = list(csv_reader)
    except FileNotFoundError:  # Just incase the file is error and cannot be found
        print(f"The file {file_path} does not exist.")
        return
    except Exception as e:  # Catch all other exceptions
        print(f"An error occurred: {e}")
        return

    # Find the transaction to delete
    found = False
    for transaction in transactions:
        if transaction[0] == bank_number:
            transactions.remove(transaction)
            found = True
            break

    # If transaction not found, print a message and return
    if not found:
        print(f"Transaction with bank number {bank_number} not found.")
        return

    # Write the updated transactions to the file
    with open(file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv