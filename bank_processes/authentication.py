from datetime import datetime
import random

from bank_processes.database import DataBase


def verify_data(get_column: str, table_number: int, _object: str) -> bool:
    """Validates unique values against the database to check if it exists before or not"""
    db: DataBase = DataBase()

    query = (f"""
    select {get_column} from {db.db_tables[table_number]}
    """)

    datas: tuple = db.fetch_data(query)

    for data in datas:
        if (_object,) == data:
            return True

    return False


class Authentication:

    def __init__(self, username: str = None, password: str = None, failed_login_attempts: int = 0,
                 auth_outcome: str = None, login_time_stamp: datetime = datetime.now().time(),
                 session_token: str = str(random.randint(100000, 999999))):
        self.__username = username  # User's name for authentication.
        self.__password = password  # User's password for authentication.
        self.__failed_login_attempts = failed_login_attempts  # Count of failed login attempts for each user.
        self.__login_time_stamp = login_time_stamp  # Records timestamp of every activity.
        self.__auth_outcome = auth_outcome  # Records authentication outcomes.
        self.__session_token = session_token  # Tokens generated upon successful user authentication, used for session management and maintaining user sessions.

    def user_login(self):
        """Method to authenticate and log in an existing user, verifying their credentials (e.g., username and
        password) against stored user data."""
        db: DataBase = DataBase()

        query = (f"""
            select username from {db.db_tables[1]}
            """)

        datas: tuple = db.fetch_data(query)

        for data in datas:
            if (f'{self.__username}',) == data:
                return True

        return False

    def user_logout(self):
        """Method to log out the currently logged-in user from the bank app, terminating their session and clearing
        any authentication tokens."""
        pass

    def password_validation(self):
        """Method to validate user passwords during registration and login, enforcing password strength requirements
        and checking against common password dictionaries."""
        db: DataBase = DataBase()

        query = (f"""
            select password from {db.db_tables[1]} where username = {self.__username}
            """)

        datas: tuple = db.fetch_data(query)

        for data in datas:
            if (f'{self.__password}',) == data:
                return True

        return False

    def session_management(self):
        """Method to manage user sessions, including generating and validating session tokens, tracking session
        expiration, and handling session timeouts."""
        pass

    def password_reset(self):
        """Method to initiate the password reset process for users who have forgotten their password, sending a
        temporary password or password reset link via email or SMS."""
        pass

    def account_lockout(self):
        """Method to temporarily lock user accounts after multiple failed login attempts, preventing brute force
        attacks and unauthorized access."""
        pass

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
        self.__username = pass_word

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

