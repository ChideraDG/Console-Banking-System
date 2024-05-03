import datetime
from bank_processes.database import DataBase
from abc import ABC, abstractmethod
# from bank_processes.account import Account


class User:
    def __init__(self, username: str = None, password: str = None, first_name: str = None, middle_name: str = None,
                 last_name: str = None, gender: str = None, email: str = None, phone_number: str = None,
                 address: str = None, date_of_birth: str = None, linked_accounts: list = None,
                 last_login_timestamp: datetime.datetime = None, account_open_date: datetime.datetime = None,
                 account_close_date: datetime.datetime = None):
        self.database = DataBase
        self.__username = username  # Unique identifier for the user's account.
        self.__password = password  # Securely stored password for authentication.
        self.__first_name = first_name  # User's first name.
        self.__middle_name = middle_name  # User's middle name.
        self.__last_name = last_name  # User's last name.
        self.__gender = gender  # User's gender.
        self.__email = email  # Contact information for communication and account verification.
        self.__phone_number = phone_number  # Contact information for communication and account verification.
        self.__address = address  # User's residential or mailing address.
        self.__date_of_birth = date_of_birth  # User's date of birth for age verification and security purposes.
        self.__linked_accounts = linked_accounts  # Information about any linked accounts, such as joint accounts or beneficiaries.
        self.__last_login_timestamp = last_login_timestamp  # Timestamp indicating the user's last login activity.
        self.__account_open_date = account_open_date  # Date when the account was opened.
        self.__account_close_date = account_close_date  # Date when the account was closed.

    def register(self):
        """Method to register a new user with the bank app, including capturing and validating personal information
        such as name, address, contact details, and identification documents."""

        query = f"""
                insert into {self.database.db_tables[1]}
                (username, password, first_name, middle_name, last_name, gender, email, phone_number, address, 
                date_of_birth, linked_accounts, last_login_timestamp, account_open_date)
                values('{self.__username}', '{self.__password}', '{self.__first_name}', '{self.__middle_name}', 
                '{self.__last_name}', '{self.__gender}', '{self.__email}', '{self.__phone_number}', '{self.__address}', 
                '{self.__date_of_birth}', '{self.__linked_accounts}', '{self.__last_login_timestamp}', 
                '{self.__account_open_date}')
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

    @abstractmethod
    def open_account(self):
        """Method to allow users to open a new account, specifying the type of account and initial deposit amount."""
        raise NotImplementedError('This Method not in Use.')

    @abstractmethod
    def close_account(self):
        """Method to allow users to close an existing account, handling any necessary validations or checks before
        closing the account."""
        raise NotImplementedError('This Method not in Use.')

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
        """For debugging"""
        return f"""{self.username} {self.password} {self.first_name} {self.middle_name} {self.last_name} 
                {self.phone_number} {self.email} {self.date_of_birth} {self.gender} {self.address} 
                {self.linked_accounts}"""

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, _username):
        self.__username = _username

    @username.deleter
    def username(self):
        del self.__username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, _password):
        self.__password = _password

    @password.deleter
    def password(self):
        del self.__password

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, _first_name):
        self.__first_name = _first_name

    @first_name.deleter
    def first_name(self):
        del self.__first_name

    @property
    def middle_name(self):
        return self.__middle_name

    @middle_name.setter
    def middle_name(self, _middle_name):
        self.__middle_name = _middle_name

    @middle_name.deleter
    def middle_name(self):
        del self.__middle_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, _last_name):
        self.__last_name = _last_name

    @last_name.deleter
    def last_name(self):
        del self.__last_name

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, _gender):
        self.__gender = _gender

    @gender.deleter
    def gender(self):
        del self.__gender

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, _email):
        self.__email = _email

    @email.deleter
    def email(self):
        del self.__email

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, _phone_number):
        self.__phone_number = _phone_number

    @phone_number.deleter
    def phone_number(self):
        del self.__phone_number

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, _address):
        self.__address = _address

    @address.deleter
    def address(self):
        del self.__address

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, _date_of_birth):
        self.__date_of_birth = _date_of_birth

    @date_of_birth.deleter
    def date_of_birth(self):
        del self.__date_of_birth

    @property
    def linked_accounts(self):
        return self.__linked_accounts

    @linked_accounts.setter
    def linked_accounts(self, _linked_accounts):
        self.__linked_accounts = _linked_accounts

    @linked_accounts.deleter
    def linked_accounts(self):
        del self.__linked_accounts

    @property
    def last_login_timestamp(self):
        return self.__last_login_timestamp

    @last_login_timestamp.setter
    def last_login_timestamp(self, _last_login_timestamp):
        self.__last_login_timestamp = _last_login_timestamp

    @last_login_timestamp.deleter
    def last_login_timestamp(self):
        del self.__last_login_timestamp

    @property
    def account_open_date(self):
        return self.__account_open_date

    @account_open_date.setter
    def account_open_date(self, _account_open_date):
        self.__account_open_date = _account_open_date

    @account_open_date.deleter
    def account_open_date(self):
        del self.__account_open_date

    @property
    def account_close_date(self):
        return self.__account_close_date

    @account_close_date.setter
    def account_close_date(self, _account_close_date):
        self.__account_close_date = _account_close_date

    @account_close_date.deleter
    def account_close_date(self):
        del self.__account_close_date
