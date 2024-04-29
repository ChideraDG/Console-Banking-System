from datetime import datetime


class Authentication:

    def __int__(self, username: str, password: str, failed_login_attempts: int, login_time_stamp: datetime,
                auth_outcome: str, auth_token: str):

        self.username = username  # Information necessary for user authentication.
        self.password = password  # Information necessary for user authentication.
        self.failed_login_attempts = failed_login_attempts  # Count of failed login attempts for each user.
        self.login_time_stamp = login_time_stamp
        self.auth_outcome = auth_outcome
        self.session_token = auth_token


        