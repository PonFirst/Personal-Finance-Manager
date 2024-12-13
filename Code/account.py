"""
This module defined the account class.
Created by Pon (First) Yimcharoen
"""

class Account:
    """
    This class represents a account. It contains an ID, name, category, and account balance.
    
    Attributes:
        account_id (str): The unique identifier for the account.
        name (str): The name of the account.
        category (str): The type of account (Income, Expense, Asset, Liability).
        amount (float): The current amount of money inside the account.
    
    """
    VALID_CATEGORIES = ('Income', 'Expense', 'Asset', 'Liability')

    def __init__(self, account_id, name, category, balance):
        self.account_id = account_id
        self.name = name
        self.category = category
        self.balance = balance
