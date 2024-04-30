from datetime import datetime


class Authentication:

    def __int__(self, username: str, password: str, failed_login_attempts: int, login_time_stamp: datetime,
                auth_outcome: str, session_token: str):

        self.username = username  # Information necessary for user authentication.
        self.password = password  # Information necessary for user authentication.
        self.failed_login_attempts = failed_login_attempts  # Count of failed login attempts for each user.
        self.login_time_stamp = login_time_stamp  # Records timestamp of every activity.
        self.auth_outcome = auth_outcome  # Records authentication outcomes.
        self.session_token = session_token  # Tokens generated upon successful user authentication, used for session management and maintaining user sessions.


        