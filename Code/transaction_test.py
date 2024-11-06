import delete_transaction as dt

search_by = input("Do you want to search by bank account or date? (account/date/show all): ")
if search_by.lower() == "account":
    dt.search_by_account()
elif search_by.lower() == "date":
    dt.search_by_date()
elif search_by.lower() == "show all":
    dt.show_transactions()
else:
    print("Invalid search option. Please enter 'account' or 'date' or 'show all'.")
        
transaction_id = input("Enter the transaction id to delete: ")
try:
    transaction_id = int(transaction_id)
    dt.delete_transaction('personal_finance.db', transaction_id)
except ValueError:
    print("Invalid transaction id. Please enter a numeric value.")