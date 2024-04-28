import datetime
from bank_processes.database import DataBase


class User:
    def __init__(self, username: str = None, password: str = None, first_name: str = None, middle_name: str = None,
                 last_name: str = None, gender: str = None, email: str = None, phone_number: str = None,
                 address: str = None, date_of_birth: str = None, account_number: str = None, account_type: str = None,
                 account_balance: float = None, account_status: str = None, authentication_token: str = None,
                 transaction_pin: str = None, linked_accounts: list = None,
                 last_login_timestamp: datetime.datetime = None, account_open_date: datetime.datetime = None,
                 account_close_date: datetime.datetime = None):
        self.database = DataBase
        self.username = username  # Unique identifier for the user's account.
        self.password = password  # Securely stored password for authentication.
        self.first_name = first_name  # User's first name.
        self.middle_name = middle_name  # User's middle name.
        self.last_name = last_name  # User's last name.
        self.gender = gender
        self.email = email  # Contact information for communication and account verification.
        self.phone_number = phone_number  # Contact information for communication and account verification.
        self.address = address  # User's residential or mailing address.
        self.date_of_birth = date_of_birth  # User's date of birth for age verification and security purposes.
        self.account_number = account_number
        self.account_type = account_type  # Type of account (e.g., savings, current, joint) associated with the user.
        self.account_balance = account_balance  # Current balance of the user's account(s).
        self.account_status = account_status  # Status of the user's account(s), such as active, suspended, or closed.
        self.authentication_token = authentication_token  # Tokens used for session management and authentication.
        self.transaction_pin = transaction_pin  # Pin used for transaction authentication.
        self.linked_accounts = linked_accounts  # Information about any linked accounts, such as joint accounts or beneficiaries.
        self.last_login_timestamp = last_login_timestamp  # Timestamp indicating the user's last login activity.
        self.account_open_date = account_open_date  # Date when the account was opened.
        self.account_close_date = account_close_date  # Date when the account was closed.

    def register(self):
        """Method to register a new user with the bank app, including capturing and validating personal information
        such as name, address, contact details, and identification documents."""

        query = f"""
                insert into {self.database.db_tables[1]}
                (username, password, first_name, middle_name, last_name, gender, email, phone_number, address, 
                date_of_birth, account_number, account_type, account_balance, account_status, transaction_pin, 
                linked_accounts, last_login_timestamp, account_open_date)
                values('{self.username}', '{self.password}', '{self.first_name}', '{self.middle_name}', 
                '{self.last_name}', '{self.gender}', '{self.email}', '{self.phone_number}', '{self.address}', 
                '{self.date_of_birth}', '{self.account_number}', '{self.account_type}', {self.account_balance}, 
                '{self.account_status}', '{self.transaction_pin}', '{self.linked_accounts}', 
                '{self.last_login_timestamp}', '{self.account_open_date}')
                """

        self.database.query(query)

    def login(self):
        """Method to authenticate and log in an existing user, verifying their credentials (e.g., username and password)
         against stored user data."""
        pass

    def logout(self):
        """Method to log out the currently logged-in user from the bank app."""
        pass

    def update_personal_info(self):
        """Method to allow users to update their personal information, such as contact details, address, or password."""
        pass

    def open_account(self):
        """Method to allow users to open a new account, specifying the type of account and initial deposit amount."""
        pass

    def close_account(self):
        """Method to allow users to close an existing account, handling any necessary validations or checks before
        closing the account."""
        pass

    def view_account(self):
        """Method to retrieve information about the user's accounts, including account numbers, types, balances, and
        transaction history."""
        pass

    def change_password(self):
        """Method to allow users to change their password, providing a mechanism for updating login credentials
        securely."""
        pass

    def reset_password(self):
        """Method to initiate the password reset process, sending a temporary password or password reset link to the
        user's registered email or phone number."""
        pass

    def reset_transaction_pin(self):
        """Method to initiate the transaction pin reset process, sending a temporary password or password reset link to the
        user's registered email or phone number."""
        pass

    def __str__(self):
        return f'{self.first_name} {self.account_number}'