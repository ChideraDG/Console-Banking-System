from abc import ABC
from datetime import datetime
import random
from typing import Any
from bank_processes.account import FixedDeposit
from bank_processes.database import DataBase
from plyer import notification as note
from bank_processes.transaction import Transaction


def verify_data(get_column: str, table_number: int, _object: str) -> bool:
    """Validates unique values against the database to check if it exists before or not

    Arguments:

    get_column - name of the column you want to verify your object from
    table_number - the index of the table you want to verify your object from
    _object - the item you want to verify"""
    db: DataBase = DataBase()

    query = (f"""
    select {get_column} from {db.db_tables[table_number]}
    """)

    datas: tuple = db.fetch_data(query)

    for data in datas:
        if (_object,) == data:
            return True

    return False


def check_account_status(username: str) -> tuple[bool, Any | None, Any | None] | tuple[bool, Any | None]:
    """Checks the status of an Account.

    Argument:

    username - the username of the account you want to check its status"""
    db: DataBase = DataBase()

    query = (f"""
    select id from {db.db_tables[1]} where username = '{username}'
    """)

    datas: tuple = db.fetch_data(query)

    id_num = None
    for data in datas:
        for number in data:
            id_num = number

    account_status = None
    query = (f"""
    select account_status from {db.db_tables[3]} where account_id = {id_num}
    """)

    datas: tuple = db.fetch_data(query)

    for status in datas:
        for data in status:
            account_status = data
        if ('active',) == status:
            return True, account_status, id_num

    return False, account_status, id_num


def get_username_from_database(_object: str, email: bool = False, phone_number: bool = True):
    """Gets the username of any user with respect to their email or phone number

    Arguments:

    _object - the email or phone number of the user that will be used to get the user's username
    email - when True, the email of the user will be used to get the user's username
    phone_number - when True, the phone_number of the user will be used to get the user's username"""
    db: DataBase = DataBase()

    if email:
        phone_number = False

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

    datas: tuple = db.fetch_data(query)

    for data in datas:
        for username in data:
            return username


def token_auth():
    """Generates token for username and password recovery."""
    token = str(random.randint(100000, 999999))

    note.notify(
        title='Username Notification',
        message=f"Your Token Number: {token}. Don't Share it.\nExpires after 30 minutes.",
        timeout=30
    )
    with open('token_notification.txt', 'w') as file:
        file.write(f"Your Token Number: {token}. Don't Share it.\nExpires after 30 minutes.")

    return token


class Authentication(Transaction, FixedDeposit, ABC):

    def __init__(self, username: str = None, password: str = None, failed_login_attempts: int = 0,
                 auth_outcome: bool = None, login_time_stamp: datetime = None, session_token: str = None):
        super().__init__()
        self.__username = username  # User's name for authentication.
        self.__password = password  # User's password for authentication.
        self.__failed_login_attempts = failed_login_attempts  # Count of failed login attempts for each user.
        self.__login_time_stamp = login_time_stamp  # Records timestamp of every activity.
        self.__auth_outcome = auth_outcome  # Records authentication outcomes.
        self.__session_token = session_token  # Tokens generated upon successful user authentication, used for session management and maintaining user sessions.

    def user_login(self):
        """Method to authenticate and log in an existing user, verifying their credentials (e.g., username and
        password) against stored user data."""
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

        if self.account_type == 'savings' and self.account_tier == 'Tier 1':
            if self.last_login_timestamp.date() < datetime.today().date():
                query = (f"""
                        UPDATE {self.database.db_tables[3]} 
                        SET transaction_limit = 10, transfer_limit = 50000
                        WHERE account_number = '{self.account_number}'
                        """)

                self.database.query(query)

        elif self.account_type == 'current' and self.account_tier == 'Tier 1':
            if self.last_login_timestamp.date() < datetime.today().date():
                query = (f"""
                        UPDATE {self.database.db_tables[3]} 
                        SET transaction_limit = 50, transfer_limit = 500000
                        WHERE account_number = '{self.account_number}'
                        """)

                self.database.query(query)

        query = (f"""
                UPDATE {self.database.db_tables[1]} 
                SET last_login_timestamp = '{self.login_time_stamp}' 
                WHERE username = '{self.username}'
                """)

        self.database.query(query)

    def user_logout(self):
        """Method to log out the currently logged-in user from the bank app, terminating their session and clearing
        any authentication tokens."""
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
        """Method to validate user passwords during registration and login; and checking against common password
        dictionaries."""

        query = (f"""
        select password from {self.database.db_tables[1]} where username = '{self.__username}'
        """)

        datas: tuple = self.database.fetch_data(query)

        for data in datas:
            if (f'{self.__password}',) == data:
                return True

        return False

    def session_management(self, token_object: str = None):
        """Method to manage user sessions, including generating and validating session tokens, tracking session
        expiration, and handling session timeouts."""

        if token_object is None:
            if self.auth_outcome:
                self.session_token = str(random.randint(100000, 999999))
            else:
                self.session_token = None
        else:
            if self.session_token == token_object:
                return True
            else:
                return False

    # def password_reset(self):
    #     """Method to initiate the password reset process for users who have forgotten their password, sending a
    #     temporary password or password reset link via email or SMS."""
    #     pass

    def account_lockout(self):
        """Method to temporarily lock user accounts after multiple failed login attempts, preventing brute force
        attacks and unauthorized access."""

        query = (f"""
        update {self.database.db_tables[3]} set account_status = 'suspended' where 
        account_id = {check_account_status(self.username)[2]}
        """)

        self.database.query(query)

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
