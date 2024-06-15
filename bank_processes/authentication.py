import time
from abc import ABC
from datetime import datetime, date
import random
from typing import Any
from bank_processes.account import FixedDeposit
from bank_processes.database import DataBase
from bank_processes.loan import Loan
from bank_processes.transaction import Transaction
from bank_processes.notification import Notification


def verify_data(get_column: str, table_number: int, _object: str) -> bool:
    """
    Validates unique values against the database to check if it exists before or not.

    Parameters
    ----------
    get_column : str
        The column name to fetch data from.
    table_number : int
        The index of the table in the database tables list.
    _object : str
        The value to be checked for uniqueness.

    Returns
    -------
    bool
        True if the value exists in the database, otherwise False.
    """
    db: DataBase = DataBase()

    # Construct a query to fetch the specified column from the specified table
    query = (f"""
    select {get_column} from {db.db_tables[table_number]}
    """)

    # Fetch data from the database
    datas: tuple = db.fetch_data(query)

    # Check if the provided value exists in the fetched data
    for data in datas:
        if (_object,) == data:
            return True

    return False


def check_account_status(username: str) -> tuple[bool, Any | None, Any | None] | tuple[bool, Any | None]:
    """
    Checks the status of an account.

    Parameters
    ----------
    username : str
        The username whose account status is to be checked.

    Returns
    -------
    tuple
        A tuple containing:
        - bool: True if the account is active, otherwise False.
        - Any | None: The account status.
        - Any | None: The user ID.
    """
    db: DataBase = DataBase()

    # Construct a query to fetch the user ID based on the username
    query = (f"""
    select id from {db.db_tables[1]} where username = '{username}'
    """)

    # Fetch data from the database
    datas: tuple = db.fetch_data(query)

    id_num = None
    # Extract the user ID from the fetched data
    for data in datas:
        for number in data:
            id_num = number

    account_status = None
    # Construct a query to fetch the account status based on the user ID
    query = (f"""
    select account_status from {db.db_tables[3]} where account_id = {id_num}
    """)

    # Fetch data from the database
    datas: tuple = db.fetch_data(query)

    # Extract the account status from the fetched data
    for status in datas:
        for data in status:
            account_status = data
        if ('active',) == status:
            return True, account_status, id_num

    return False, account_status, id_num


def get_username_from_database(_object: str, email: bool = False, phone_number: bool = True):
    """
    Gets the username of any user with respect to their email or phone number.

    Parameters
    ----------
    _object : str
        The email or phone number to search for.
    email : bool, optional
        Flag to indicate if the search is based on email. Default is False.
    phone_number : bool, optional
        Flag to indicate if the search is based on phone number. Default is True.

    Returns
    -------
    str
        The username associated with the given email or phone number.

    Raises
    ------
    ValueError
        If neither 'email' nor 'phone_number' is True.
    """
    db: DataBase = DataBase()

    if email:
        phone_number = False

    # Construct a query to fetch the username based on the provided email or phone number
    if phone_number:
        query = (f"""
        select username from {db.db_tables[1]} where phone_number = '{_object}'
        """)
    elif email:
        query = (f"""
        select username from {db.db_tables[1]} where email = '{_object}'
        """)
    else:
        raise ValueError("Either 'email' argument or 'phone_number' must be True")

    # Fetch data from the database
    datas: tuple = db.fetch_data(query)

    # Return the username from the fetched data
    for data in datas:
        for username in data:
            return username


def token_auth() -> str:
    """
    Generates a token for username and password recovery.

    Returns
    -------
    str
        The generated token.

    Description
    -----------
    This method generates a random token, sends a notification to the user,
    and writes the token to a file for recovery purposes.
    """
    from banking.login_panel import notify

    token = str(random.randint(100000, 999999))

    # Send a notification to the user with the generated token
    notify.token_notification(
        title='Console Beta Banking',
        message=f"Your Token Number: {token}. Don't Share it.\nExpires after 30 minutes.",
        channel='Token_Number'
    )

    return token


class Authentication(Transaction, FixedDeposit, Notification, ABC):

    def __init__(self, username: str = None, password: str = None, failed_login_attempts: int = 0,
                 auth_outcome: bool = None, login_time_stamp: datetime = None, session_token: str = None):
        super().__init__()
        self.__username = username  # User's name for authentication.
        self.__password = password  # User's password for authentication.
        self.__failed_login_attempts = failed_login_attempts  # Count of failed login attempts for each user.
        self.__login_time_stamp = login_time_stamp  # Records timestamp of every activity.
        self.__auth_outcome = auth_outcome  # Records authentication outcomes.
        self.__session_token = session_token  # Tokens generated upon successful user authentication, used for
        # session management and maintaining user sessions.
        self.loan = Loan()

    def user_login(self):
        """
        Authenticate and log in an existing user, verifying their credentials (e.g., username and
        password) against stored user data.

        Description
        -----------
        This method performs the following actions:
        1. Sets user attributes.
        2. Manages user session.
        3. Updates transaction and transfer limits based on account type and tier.
        4. Updates the last login timestamp in the database.
        5. Checks fixed deposit due dates and processes them if necessary.
        6. Checks loan payments.
        """

        from banking.script import log_error, go_back  # Import necessary functions for error logging and navigation

        try:
            # Set user attributes
            self.username = self.username
            self.password = self.password
            self.user_id = self.user_id
            self.login_time_stamp = datetime.now()
            self.auth_outcome = True
            self.session_management()
            self.first_name = self.first_name
            self.middle_name = self.middle_name
            self.last_name = self.last_name
            self.gender = self.gender
            self.email = self.email
            self.phone_number = self.phone_number
            self.address = self.address
            self.date_of_birth = self.date_of_birth
            self.linked_accounts = self.linked_accounts
            self.account_open_date = self.account_open_date
            self.account_number = self.account_number
            self.account_type = self.account_type
            self.account_holder = self.account_holder
            self.account_balance = self.account_balance
            self.transaction_pin = self.transaction_pin
            self.account_status = self.account_status
            self.overdraft_protection = self.overdraft_protection
            self.account_tier = self.account_tier
            self.transaction_limit = self.transaction_limit
            self.fixed_account = self.fixed_account

            # Update transaction and transfer limits for savings Tier 1 accounts
            if self.account_type == 'savings' and self.account_tier == 'Tier 1':
                if self.last_login_timestamp.date() < datetime.today().date():
                    query = (f"""
                            UPDATE {self.database.db_tables[3]} 
                            SET transaction_limit = 10, transfer_limit = 50000
                            WHERE account_number = '{self.account_number}'
                            """)
                    self.database.query(query)

            # Update transaction and transfer limits for current Tier 1 accounts
            elif self.account_type == 'current' and self.account_tier == 'Tier 1':
                if self.last_login_timestamp.date() < datetime.today().date():
                    query = (f"""
                            UPDATE {self.database.db_tables[3]} 
                            SET transaction_limit = 50, transfer_limit = 500000
                            WHERE account_number = '{self.account_number}'
                            """)
                    self.database.query(query)

            try:
                # Update the last login timestamp in the database
                query = (f"""
                        UPDATE {self.database.db_tables[1]} 
                        SET last_login_timestamp = '{self.login_time_stamp}' 
                        WHERE username = '{self.username}'
                        """)
                self.database.query(query)
            except Exception as e:
                # Rollback changes if an error occurs
                self.database.rollback()

            # Check Fixed Deposits if the PayBack date is due or not
            self.fixed_deposit_due_date_validation()

            # Check loan payments
            self.check_loan_payments()

        except Exception as e:  # Handle any exceptions that occur during the login process
            log_error(e)  # Log the error
            go_back('script')  # Navigate back in the script

    def user_logout(self):
        """
        Log out the currently logged-in user from the bank app, terminating their session and clearing
        any authentication tokens.

        Description
        -----------
        This method performs the following actions:
        1. Deletes all user-related attributes to terminate the session.
        2. Clears any authentication tokens.
        """
        from banking.login_panel import notify

        notify.sign_out_notification(
            title='Console Beta Banking',
            message=f"{self.account_holder}, You logged out of your Account",
            channel='Log_Out'
        )
        
        # Delete user-related attributes to log out the user
        del self.username
        del self.password
        del self.user_id
        del self.login_time_stamp
        del self.auth_outcome
        del self.session_token
        del self.first_name
        del self.middle_name
        del self.last_name
        del self.gender
        del self.email
        del self.phone_number
        del self.address
        del self.date_of_birth
        del self.linked_accounts
        del self.last_login_timestamp
        del self.account_open_date
        del self.account_number
        del self.account_type
        del self.account_holder
        del self.account_balance
        del self.transaction_pin
        del self.account_status
        del self.overdraft_protection
        del self.account_tier
        del self.transaction_limit

    def password_validation(self) -> bool:
        """
        Validate user passwords during registration and login by checking against stored passwords.

        Returns
        -------
        bool
            True if the password matches the stored password, otherwise False.

        Description
        -----------
        This method performs the following actions:
        1. Constructs a SQL query to fetch the stored password for the given username.
        2. Executes the query and retrieves the stored password.
        3. Compares the provided password with the stored password.
        4. Returns True if the passwords match, otherwise returns False.
        """

        # Construct a SQL query to fetch the stored password for the given username
        query = (f"""
        select password from {self.database.db_tables[1]} where username = '{self.__username}'
        """)

        # Execute the query and store the result in 'datas'
        datas: tuple = self.database.fetch_data(query)

        # Iterate through the fetched data
        for data in datas:
            # Check if the provided password matches the stored password
            if (f'{self.__password}',) == data:
                return True  # Return True if the passwords match

        return False  # Return False if no matching password is found

    def session_management(self, token_object: str = None):
        """
        Manage user sessions, including generating and validating session tokens, tracking session
        expiration, and handling session timeouts.

        Parameters
        ----------
        token_object : str, optional
            The session token to validate. If None, a new session token is generated.

        Returns
        -------
        bool
            True if the provided token matches the stored session token, otherwise False.

        Description
        -----------
        This method performs the following actions based on the provided parameters:
        1. If no token_object is provided (token_object is None):
           a. If the user is authenticated (self.auth_outcome is True), generate a new session token.
           b. If the user is not authenticated (self.auth_outcome is False), set the session token to None.
        2. If a token_object is provided:
           a. Validate the provided token against the stored session token.
           b. Return True if the tokens match, otherwise return False.
        """

        # Check if a token object is provided
        if token_object is None:
            # If no token object is provided, check the authentication outcome
            if self.auth_outcome:
                # If authentication is successful, generate a new session token
                self.session_token = str(random.randint(100000, 999999))
            else:
                # If authentication fails, set the session token to None
                self.session_token = None
        else:
            # If a token object is provided, validate it against the stored session token
            if self.session_token == token_object:
                # Return True if the tokens match
                return True
            else:
                # Return False if the tokens do not match
                return False

    def account_lockout(self):
        """Method to temporarily lock user accounts after multiple failed login attempts, preventing brute force
        attacks and unauthorized access."""

        query = (f"""
        update {self.database.db_tables[3]} set account_status = 'suspended' where 
        account_id = {check_account_status(self.username)[2]}
        """)

        self.database.query(query)

    def fixed_deposit_due_date_validation(self):
        """
        Validates due dates for fixed deposits, updates their status if they are due,
        and processes the deposit back to the user's account.

        This method performs the following steps:
        1. Fetches all active fixed deposits from the database.
        2. Iterates through each fixed deposit to check if it is due.
        3. If a fixed deposit is due:
           a. Fetches the initial deposit amount.
           b. Updates the status of the fixed deposit to 'inactive'.
           c. Processes the deposit back to the user's account.
           d. Records the transaction.
           e. Validates the receiver's transaction.
        4. Handles any exceptions that occur during the process and rolls back the transaction if necessary.
        """
        from banking.script import log_error, go_back  # Import necessary functions for error logging and navigation

        try:
            # Query to fetch all active fixed deposits ordered by start date
            query = f"""
                    select * from {self.database.db_tables[4]} where status = 'active'
                    ORDER BY start_date
                    """
            data = self.database.fetch_data(query)  # Fetch the data from the database

            for value in data:  # Iterate through each active fixed deposit
                # Extract the hour, minute, and second from the time string
                hour, minute, second = str(value[8]).split(':')

                # Check if the fixed deposit is due by comparing the end date and time with the current date and time
                if datetime(year=value[7].year, month=value[7].month, day=value[7].day, hour=int(hour),
                            minute=int(minute),
                            second=int(second)) <= datetime.today().now():
                    try:
                        # Query to fetch the initial deposit amount for the due fixed deposit
                        get_deposit = f"""
                                SELECT initial_deposit 
                                FROM {self.database.db_tables[4]} 
                                WHERE deposit_id = '{value[0]}'
                                """
                        datas = self.database.fetch_data(get_deposit)  # Fetch the initial deposit amount

                        # Update the status of the fixed deposit to 'inactive'
                        query = f"""
                                        UPDATE {self.database.db_tables[4]}
                                        SET status = 'inactive'
                                        WHERE deposit_id = '{value[0]}'
                                        """
                        self.database.query(query)  # Execute the update query

                        # Prepare to process the deposit back to the user's account
                        self.receiver_acct_num = self.account_number
                        self.description = f'FIXED_DEPOSIT/CBB/DEPOSIT TO {self.account_holder}'  # Set the description

                        for data in datas:  # Iterate through the fetched deposit data
                            for amount in data:  # Extract the deposit amount
                                self.amount = float(amount)

                        self.process_transaction(deposit=True)  # Process the deposit
                        self.transaction_record(deposit=True)  # Record the transaction
                        self.receiver_transaction_validation()  # Validate the receiver's transaction

                    except Exception:  # Handle any exceptions that occur during processing
                        self.database.rollback()  # Rollback the transaction if an error occurs
        except Exception as e:  # Handle any exceptions that occur during the initial data fetching
            log_error(e)  # Log the error
            go_back('script')  # Navigate back in the script

    def check_loan_payments(self):
        """
        Check and process the user's loan payments.

        This method performs the following steps:
        1. Sets the loan email to the user's email.
        2. Queries the database for active loans (status_id = 1) associated with the user.
        3. Iterates through the retrieved loans and checks if any payments are due.
        4. If a payment is due, fetches the monthly payment amount.
        5. Makes the loan payment and processes the transaction.
        6. Records the transaction.
        7. Updates the loan status to complete (status_id = 3) if the loan end date is reached.

        Returns
        -------
        None
        """
        from banking.login_panel import notify
        from banking.script import log_error, go_back
        try:
            self.loan.email = self.email  # Set the loan email to the user's email

            if self.loan.user_id is not None:
                # Query to fetch active loans for the user
                query = f"""
                        SELECT * 
                        FROM {self.database.db_tables[7]}
                        WHERE user_id = {self.loan.user_id}
                        AND status_id = 1
                        """

                datas = self.database.fetch_data(query)  # Fetch the active loans

                for data in datas:  # Iterate through the fetched loans
                    due_date = str(data[7])  # Set the loan due date
                    end_date = str(data[8])  # Set the loan end date

                    # Check if the current date is within the loan period
                    if datetime.today().date() >= date(
                            int(due_date[:4]), int(due_date[5:7]), int(due_date[8:])) <= date(
                            int(end_date[:4]), int(end_date[5:7]), int(end_date[8:])):

                        # Query to fetch the monthly payment amount for the loan
                        query = f"""
                                SELECT monthly_payment 
                                FROM {self.database.db_tables[7]}
                                WHERE user_id = {self.loan.user_id}
                                AND status_id = 1
                                """

                        datass = self.database.fetch_data(query)  # Fetch the monthly payment amount

                        for dat in datass:  # Iterate through the fetched monthly payments
                            for amount in dat:  # Iterate through the amounts
                                self.amount = float(amount)  # Set the payment amount

                        # Make the loan payment
                        self.loan.make_loan_payments(
                            loan_id=data[0],
                            amount=self.amount,
                            payment_date=str(datetime.today().date())
                        )

                        # Set the transaction details
                        self.description = f'LOAN_REPAYMENT/CBB/TRANSFER TO CONSOLE BETA BANK'
                        self.receiver_acct_num = '1000000009'

                        self.process_transaction(central_bank=True)  # Process the transaction
                        self.transaction_record(central_bank=True)  # Record the transaction

                        # Set the transaction details and Process the transaction for the User
                        self.description = f'LOAN_REPAYMENT/CBB/FROM {self.account_holder} TO CONSOLE BETA BANK'

                        self.process_transaction(loan=True)  # Process the transaction
                        self.transaction_record(loan=True)  # Record the transaction

                        note = f"""
                        Debit
                        Amount :: NGN{self.amount}
                        Acc :: {self.account_number[:3]}******{self.account_number[-3:]}
                        Desc :: {self.description}
                        Time :: {datetime.today().now().time()}
                        Balance :: {self.account_balance}
                        """

                        # Send a notification to the user with the generated token
                        notify.loan_notification(
                            title='Console Beta Banking',
                            message=note,
                            channel='Loan_Repayment'
                        )

                        due_month = int(due_date[5:7]) + 1
                        due_year = int(due_date[:4])

                        # Adjust the due month and year if the month exceeds 12
                        while due_month > 12:
                            due_month -= 12
                            due_year += 1

                        # Update the due date
                        query = f"""
                                UPDATE {self.database.db_tables[7]}
                                SET due_date = '{due_year}-{due_month}-{int(due_date[8:])}'
                                WHERE loan_id = {data[0]}
                                """

                        self.database.query(query)

                        # Check if the loan end date is reached
                        if date(int(due_date[:4]), int(due_date[5:7]), int(due_date[8:])) >= date(
                                int(end_date[:4]), int(end_date[5:7]), int(end_date[8:])):
                            # Update the loan status to complete (status_id = 3)
                            query = f"""
                                    UPDATE {self.database.db_tables[7]}
                                    SET status_id = 3
                                    WHERE loan_id = {data[0]}
                                    """

                            self.database.query(query)  # Execute the update query
        except Exception as e:
            log_error(e)
            go_back('script')

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, user_name: str):
        self.__username = user_name

    @username.deleter
    def username(self):
        del self.__username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, pass_word):
        self.__password = pass_word

    @password.deleter
    def password(self):
        del self.__password

    @property
    def login_attempts(self):
        return self.__failed_login_attempts

    @login_attempts.setter
    def login_attempts(self, login_attempt: str):
        self.__failed_login_attempts = login_attempt

    @login_attempts.deleter
    def login_attempts(self):
        del self.__failed_login_attempts

    @property
    def auth_outcome(self):
        return self.__auth_outcome

    @auth_outcome.setter
    def auth_outcome(self, _auth_outcome: str):
        self.__auth_outcome = _auth_outcome

    @auth_outcome.deleter
    def auth_outcome(self):
        del self.__auth_outcome

    @property
    def login_time_stamp(self):
        return self.__login_time_stamp

    @login_time_stamp.setter
    def login_time_stamp(self, _login_time_stamp: datetime):
        self.__login_time_stamp = _login_time_stamp

    @login_time_stamp.deleter
    def login_time_stamp(self):
        del self.__login_time_stamp

    @property
    def session_token(self):
        return self.__session_token

    @session_token.setter
    def session_token(self, _session_token: str):
        self.__session_token = _session_token

    @session_token.deleter
    def session_token(self):
        del self.__session_token
