import datetime
import re
import time
from bank_processes.database import DataBase
from abc import abstractmethod


class User:
    def __init__(self, user_id: int = None, username: str = None, password: str = None, first_name: str = None,
                 middle_name: str = None, last_name: str = None, gender: str = None, email: str = None,
                 phone_number: str = None, address: str = None, date_of_birth: str = None, linked_accounts: list = None,
                 last_login_timestamp: datetime.datetime = None, account_open_date: datetime.datetime = None,
                 account_close_date: datetime.datetime = None):
        self.database = DataBase
        self.__USER_ID = user_id
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

        try:
            query = f"""
                    INSERT INTO {self.database.db_tables[1]}
                    (username, password, first_name, middle_name, last_name, gender, email, phone_number, address, 
                    date_of_birth, linked_accounts, last_login_timestamp, account_open_date)
                    VALUES('{self.__username}', '{self.__password}', '{self.__first_name}', '{self.__middle_name}', 
                    '{self.__last_name}', '{self.__gender}', '{self.__email}', '{self.__phone_number}', '{self.__address}', 
                    '{self.__date_of_birth}', '{self.__linked_accounts}', '{self.__last_login_timestamp}', 
                    '{self.__account_open_date}')
                    """

            self.database.query(query)
        except Exception as e:
            # Rollback changes if an error occurs
            self.database.rollback()

    @abstractmethod
    def user_login(self):
        """Method to authenticate and log in an existing user, verifying their credentials (e.g., username and password)
         against stored user data."""
        raise NotImplementedError('This Method not in Use.')

    @abstractmethod
    def user_logout(self):
        """Method to log out the currently logged-in user from the bank app."""
        raise NotImplementedError('This Method not in Use.')

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
        """
        Updates the password for the current user in the database.

        Notes
        -----
        This method updates the user's password in the database. If an error occurs during the
        database update, the transaction is rolled back.

        Raises
        ------
        Exception
            If there is an error during the database update.
        """
        try:
            # Define the SQL query to update the user's password
            query = (f"""
            UPDATE {self.database.db_tables[1]} 
            SET password = '{self.password}' 
            WHERE username = '{self.username}'
            """)

            # Execute the query to update the password
            self.database.query(query)
        except Exception as e:
            # If an error occurs, roll back the transaction to maintain data integrity
            self.database.rollback()

    def reset_password(self):
        """
        Resets the user's password using either their phone number or email.

        Notes
        -----
        This method guides the user through the process of resetting their password by verifying their identity
        using a phone number or email, and a token authentication process. If the verification is successful,
        the user is prompted to enter a new password.

        The user can choose to reset their password using either their phone number or email.
        For phone number verification, the user must enter the last four digits of their phone number.
        For email verification, the user must enter their complete email address.

        Raises
        ------
        Exception
            If there is an error during the password reset process.
        """
        from bank_processes.authentication import token_auth
        from banking.register_panel import account_password
        from banking.main_menu import header, go_back

        try:
            while True:
                # Display the header for the password reset process
                header()

                # Prompt the user to choose the method for resetting the password
                print("\nReset your password with your Phone Number? Press 1")
                print("---------------------------------------------------")
                print("Reset your password with your Email? Press 2")
                print("--------------------------------------------")
                _input = input(">>> ")  # Get user input for the reset method

                time.sleep(1)  # Pause for a moment

                if re.search('^1$', _input):  # If the user chooses to reset by phone number
                    four_digit = self.phone_number[-4:]  # Get the last four digits of the phone number
                    incomplete_number = self.phone_number[:-4] + '****'  # Mask the phone number for privacy
                    while True:
                        # Display the header and prompt the user to enter the last four digits of their phone number
                        header()
                        print(f"\nENTER THE LAST FOUR DIGITS OF YOUR PHONE NUMBER ({incomplete_number}):")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + "~" * len(incomplete_number))
                        _input = input(">>> ")  # Get user input

                        if four_digit == _input:  # If the input matches the last four digits of the phone number
                            start_time = time.time()  # Record the start time for token expiration
                            _token = token_auth()  # Generate a token for authentication
                            while True:
                                # Prompt the user to enter the token number
                                print("\nENTER YOUR TOKEN NUMBER:")
                                print("~~~~~~~~~~~~~~~~~~~~~~~~")
                                _tokenNumber = input(">>> ")  # Get user input

                                elapsed_time = time.time() - start_time  # Calculate the elapsed time
                                if elapsed_time < 30.0:  # If the token is still valid (within 30 seconds)
                                    if _token == _tokenNumber:  # If the token matches
                                        self.password = account_password()  # Prompt the user to set a new password
                                        break
                                    else:
                                        # If the token does not match, display an error message and prompt again
                                        print("\n*ERROR*\nWrong Token Number.\n\nTry Again")
                                        time.sleep(3)
                                        continue
                                else:
                                    # If the token has expired, generate a new token and prompt again
                                    print("\n*ERROR*\nTime is already over 30 minutes.\n\nRe-Sending Token Number")
                                    start_time = time.time()
                                    _token = token_auth()
                                    time.sleep(3)
                                    continue
                            break
                        else:
                            # If the input does not match, display an error message and prompt again
                            print("\n*ERROR*\nWrong Four Digit Input.")
                            time.sleep(3)
                            continue
                    break
                elif re.search('^2$', _input):  # If the user chooses to reset by email
                    at_index = self.email.index('@')  # Find the index of '@' in the email
                    incomplete_email = self.email[:1 - len(self.email)] + '*' * len(
                        self.email[1:at_index]) + self.email[at_index:]  # Mask the email for privacy
                    while True:
                        # Display the header and prompt the user to enter their email
                        header()
                        print(f"\nENTER YOUR EMAIL ({incomplete_email}):")
                        print("~~~~~~~~~~~~~~~~~~~~" + "~" * len(incomplete_email))
                        _input = input(">>> ")  # Get user input

                        if self.email == _input.lower():  # If the input matches the email
                            start_time = time.time()  # Record the start time for token expiration
                            _token = token_auth()  # Generate a token for authentication
                            while True:
                                # Prompt the user to enter the token number
                                print("\nENTER YOUR TOKEN NUMBER:")
                                print("~~~~~~~~~~~~~~~~~~~~~~~~")
                                _tokenNumber = input(">>> ")  # Get user input

                                elapsed_time = time.time() - start_time  # Calculate the elapsed time
                                if elapsed_time < 30.0:  # If the token is still valid (within 30 seconds)
                                    if _token == _tokenNumber:  # If the token matches
                                        self.password = account_password()  # Prompt the user to set a new password
                                        break
                                    else:
                                        # If the token does not match, display an error message and prompt again
                                        print("\n*ERROR*\nWrong Token Number.\n\nTry Again")
                                        time.sleep(3)
                                        continue
                                else:
                                    # If the token has expired, generate a new token and prompt again
                                    print("\n*ERROR*\nTime is already over 30 minutes.\n\nRe-Sending Token Number")
                                    start_time = time.time()
                                    _token = token_auth()
                                    time.sleep(3)
                                    continue
                            break
                        else:
                            # If the input does not match, display an error message and prompt again
                            print("\n*ERROR*\nWrong Corresponding Email.")
                            time.sleep(3)
                            continue
                    break
                else:
                    # If the input is invalid, display an error message and prompt again
                    print("\n*ERROR*\nWrong Input.")
                    time.sleep(3)
                    continue
        except Exception as e:
            # If an error occurs, log the error and display an error message
            with open('notification/error.txt', 'w') as file:
                file.write(f'Error: {repr(e)}')
            print(f'\nError: {repr(e)}')
            time.sleep(3)
            go_back('script')

    def update_personal_info(self, *, _column_name: str, _data: str, _id_number: int):
        """
        Method to allow users to update their personal information, such as contact details, address, or password.

        Parameters
        ----------
        _column_name : str
            The name of the column to update.
        _data : str
            The new data to be inserted into the specified column.
        _id_number : int
            The ID number identifying the specific user record to be updated.
        """

        # Construct the SQL query as a formatted string
        query = f"""
        UPDATE {self.database.db_tables[1]} 
        SET {_column_name} = '{_data}'
        WHERE id = {_id_number}
        """

        # Execute the query using the database's query method
        self.database.query(query)

    def reset_transaction_pin(self):
        """Method to initiate the transaction pin reset process, sending a temporary password or password reset link
        to the user's registered email or phone number."""
        pass

    @property
    def user_id(self):
        if self.username is not None:
            query = (f"""
                SELECT id 
                FROM {self.database.db_tables[1]} 
                WHERE username = '{self.username}'
                """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for user_id in data:
                    self.user_id = user_id

        return self.__USER_ID

    @user_id.setter
    def user_id(self, _user_id):
        self.__USER_ID = _user_id

    @user_id.deleter
    def user_id(self):
        del self.__USER_ID

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
        if self.username is not None:
            query = (f"""
            SELECT password 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for password in data:
                    self.password = password

        return self.__password

    @password.setter
    def password(self, _password):
        self.__password = _password

    @password.deleter
    def password(self):
        del self.__password

    @property
    def first_name(self):
        if self.username is not None:
            query = (f"""
            SELECT first_name 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for first_name in data:
                    self.first_name = first_name

        return self.__first_name

    @first_name.setter
    def first_name(self, _first_name):
        self.__first_name = _first_name

    @first_name.deleter
    def first_name(self):
        del self.__first_name

    @property
    def middle_name(self):
        if self.username is not None:
            query = (f"""
            SELECT middle_name 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for middle_name in data:
                    self.middle_name = middle_name

        return self.__middle_name

    @middle_name.setter
    def middle_name(self, _middle_name):
        self.__middle_name = _middle_name

    @middle_name.deleter
    def middle_name(self):
        del self.__middle_name

    @property
    def last_name(self):
        if self.username is not None:
            query = (f"""
            SELECT last_name 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for last_name in data:
                    self.last_name = last_name

        return self.__last_name

    @last_name.setter
    def last_name(self, _last_name):
        self.__last_name = _last_name

    @last_name.deleter
    def last_name(self):
        del self.__last_name

    @property
    def gender(self):
        if self.username is not None:
            query = (f"""
            SELECT gender 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for gender in data:
                    self.gender = gender

        return self.__gender

    @gender.setter
    def gender(self, _gender):
        self.__gender = _gender

    @gender.deleter
    def gender(self):
        del self.__gender

    @property
    def email(self):
        if self.username is not None:
            query = (f"""
            SELECT email 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for email in data:
                    self.email = email

        return self.__email

    @email.setter
    def email(self, _email):
        self.__email = _email

    @email.deleter
    def email(self):
        del self.__email

    @property
    def phone_number(self):
        if self.username is not None:
            query = (f"""
            SELECT phone_number 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for phone_number in data:
                    self.phone_number = phone_number

        return self.__phone_number

    @phone_number.setter
    def phone_number(self, _phone_number):
        self.__phone_number = _phone_number

    @phone_number.deleter
    def phone_number(self):
        del self.__phone_number

    @property
    def address(self):
        if self.username is not None:
            query = (f"""
            SELECT address 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for address in data:
                    self.address = address

        return self.__address

    @address.setter
    def address(self, _address):
        self.__address = _address

    @address.deleter
    def address(self):
        del self.__address

    @property
    def date_of_birth(self):
        if self.username is not None:
            query = (f"""
            SELECT date_of_birth 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for date_of_birth in data:
                    self.date_of_birth = date_of_birth

        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, _date_of_birth):
        self.__date_of_birth = _date_of_birth

    @date_of_birth.deleter
    def date_of_birth(self):
        del self.__date_of_birth

    @property
    def linked_accounts(self):
        if self.username is not None:
            query = (f"""
            SELECT linked_accounts 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for linked_account in data:
                    self.linked_accounts = linked_account

        return self.__linked_accounts

    @linked_accounts.setter
    def linked_accounts(self, _linked_accounts):
        self.__linked_accounts = _linked_accounts

    @linked_accounts.deleter
    def linked_accounts(self):
        del self.__linked_accounts

    @property
    def last_login_timestamp(self):
        if self.username is not None:
            query = (f"""
            SELECT last_login_timestamp 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for last_login_timestamp in data:
                    self.last_login_timestamp = last_login_timestamp

        return self.__last_login_timestamp

    @last_login_timestamp.setter
    def last_login_timestamp(self, _last_login_timestamp):
        self.__last_login_timestamp = _last_login_timestamp

    @last_login_timestamp.deleter
    def last_login_timestamp(self):
        del self.__last_login_timestamp

    @property
    def account_open_date(self):
        if self.username is not None:
            query = (f"""
            SELECT account_open_date 
            FROM {self.database.db_tables[1]} 
            WHERE username = '{self.username}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for account_open_date in data:
                    self.account_open_date = account_open_date

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
