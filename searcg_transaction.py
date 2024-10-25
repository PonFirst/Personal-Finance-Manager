def validate_bank_number(bank_number):
    return bank_number.isdigit() and len(bank_number) == 4  # assuming 4 digits

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False
    
def search_transaction():