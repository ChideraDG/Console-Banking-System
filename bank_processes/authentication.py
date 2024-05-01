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

    def user_login(self):
        """Method to authenticate and log in an existing user, verifying their credentials (e.g., username and
        password) against stored user data."""
        pass

    def user_logout(self):
        """Method to log out the currently logged-in user from the bank app, terminating their session and clearing
        any authentication tokens."""
        pass

    def password_validation(self):
        """Method to validate user passwords during registration and login, enforcing password strength requirements
        and checking against common password dictionaries."""
        pass

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
        