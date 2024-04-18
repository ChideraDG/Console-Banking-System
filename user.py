class User:
    username = None  # Unique identifier for the user's account.
    password = None  # Securely stored password for authentication.
    first_name = None  # User's first name.
    middle_name = None  # User's middle name.
    last_name = None  # User's last name.
    email = None  # Contact information for communication and account verification.
    phone_number = None  # Contact information for communication and account verification.
    address = None  # User's residential or mailing address.
    date_of_birth = None  # User's date of birth for age verification and security purposes.
    account_type = None  # Type of account (e.g., savings, current, joint) associated with the user.
    account_balance = None  # Current balance of the user's account(s).
    account_status = None  # Status of the user's account(s), such as active, suspended, or closed.
    security_question = None  # Additional security measures for account recovery or verification.
    security_answer = None  # Additional security measures for account recovery or verification.
    authentication_token = None  # Tokens used for session management and authentication.
    transaction_pin = None  # Pin used for transaction authentication.
    linked_acconuts = None  # Information about any linked accounts, such as joint accounts or beneficiaries.
    last_login_timestamp = None  # Timestamp indicating the user's last login activity.

    @classmethod
    def register(cls):
        """Method to register a new user with the bank app, including capturing and validating personal information
        such as name, address, contact details, and identification documents."""
        pass

    @classmethod
    def login(cls):
        """Method to authenticate and log in an existing user, verifying their credentials (e.g., username and password)
         against stored user data."""
        pass

    @classmethod
    def logout(cls):
        """Method to log out the currently logged-in user from the bank app."""
        pass

    @classmethod
    def update_personal_info(cls):
        """Method to allow users to update their personal information, such as contact details, address, or password."""
        pass

    @classmethod
    def open_account(cls):
        """Method to allow users to open a new account, specifying the type of account and initial deposit amount."""
        pass

    @classmethod
    def close_account(cls):
        """Method to allow users to close an existing account, handling any necessary validations or checks before
        closing the account."""
        pass

    @classmethod
    def view_account(cls):
        """Method to retrieve information about the user's accounts, including account numbers, types, balances, and
        transaction history."""
        pass

    @classmethod
    def change_password(cls):
        """Method to allow users to change their password, providing a mechanism for updating login credentials
        securely."""
        pass

    @classmethod
    def reset_password(cls):
        """Method to initiate the password reset process, sending a temporary password or password reset link to the
        user's registered email or phone number."""
        pass

    @classmethod
    def reset_transaction_pin(cls):
        """Method to initiate the transaction pin reset process, sending a temporary password or password reset link to the
        user's registered email or phone number."""
        pass