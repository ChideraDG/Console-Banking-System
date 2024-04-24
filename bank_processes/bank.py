import time
import sys
import os
def clear():
    if os.name == 'nt':
        os.system('cls')

def countdown_and_wait():
    for i in range(3, 0, -1):
        sys.stdout.flush()  # Flush the output buffer
        print(f"Clearing in {i} seconds...", end="")  # Optional: You can add a message here for clarity
        time.sleep(1)
        print(end='\r')
    time.sleep(1) # Optional: Add an extra delay for better visibility
    clear()

def wait_and_count():
    sys.stdout.flush()
    print("Please wait..", end='')
    time.sleep(1)
    print(end='\r')
    clear()



class Bank:
    bank_name: str = None  # The name of the bank.
    interest_rate: float = None  # Current interest rates offered for various types of accounts and financial products.
    fee_and_charges: float = None  # Details about fees and charges; Account maintenance fees, transaction fees, and overdraft fees.
    security_measures: str = None  # Information about security measures implemented by the bank to protect customer data and prevent fraud, such as encryption, firewalls, and fraud detection systems.
    financial_performances: str = None  # Information about the bank's financial performance, including revenue, profits, and assets under management.
    history_and_heritage: str = None  # Historical information about the bank, including its founding date, milestones, and notable achievements.
    mission_and_values: str = None  # The mission statement and core values of the bank, guiding its operations and interactions with customers and stakeholders.

    @classmethod
    def open_account(cls):
        """this will enable a user open an account"""
        print("OPEN ACCOUNT")
        print("~~~~~~~~~~~~")
        clear()




    @classmethod
    def close_account(cls):
        """Method to close an existing account"""
        pass

    @classmethod
    def view_account_details(cls):
        """Method to view account details"""
        pass

    @classmethod
    def list_accounts(cls):
        """Method to see the list of accounts"""
        pass

    @classmethod
    def calculate_interest(cls):
        """Method to calculate interest """
        pass

    @classmethod
    def process_transactions(cls):
        """Method to process transactions"""
        pass

    @classmethod
    def authorize_transactions(cls):
        """Method to authorize transactions."""
        pass

    @classmethod
    def manage_fees_and_charges(cls):
        """Method to manage fees and charges"""
        pass

    @classmethod
    def general_reports(cls):
        """Method for handling general reports"""
        pass


    @classmethod
    def handle_regulatory_compliances(cls):
        """Method for handling regulatory compliances"""
        pass