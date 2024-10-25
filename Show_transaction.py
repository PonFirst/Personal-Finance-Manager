'''
Show all transactions in the file transactions.csv
After running the script,
all the transactions in the file transactions.csv should be displayed in the console.
'''

import csv

# Function to show all transactions in the file
def show_transactions(file_path):
    try:  # Try to open the file and read the content
        with open(file_path, mode='r') as file:  # Open the file in read mode
            csv_reader = csv.reader(file)   
            header = next(csv_reader) 
            print(f"{' | '.join(header)}")  # Print the header
            print('-' * 50)     # Print a line
            
            for row in csv_reader:  # Print each row
                print(f"{' | '.join(row)}")
                
    except FileNotFoundError:  # Just incase the file is error and cannot be found
        print(f"The file {file_path} does not exist.")
        
    except Exception as e:  # Catch all other exceptions
        print(f"An error occurred: {e}")

# Main function to run the script
if __name__ == "__main__": # This is to run the script
    show_transactions(file_path)