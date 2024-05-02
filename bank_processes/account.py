from bank_processes.user import User


class Account(User):
    currency: str = 'Naira'  # Currency in which the account is denominated.

    def __init__(self, account_number: str = None, account_type: str = None, account_holder: str = None,
                 account_balance: float = None, transaction_pin: str = None, account_status: str = None,
                 account_tier: str = None, transaction_limit: int = None, overdraft_protection: str = None):
        super().__init__()
        self.account_number = account_number  # Unique identifier for the account.
        self.account_type = account_type  # Type of account (e.g., savings, checking, credit card).
        self.account_holder = account_holder  # User or users associated with the account.
        self.account_balance = account_balance  # Current balance of the account.
        self.transaction_pin = transaction_pin  # Pin used for transaction authentication.
        self.account_status = account_status  # Status of the account (e.g., active, closed, frozen).
        self.overdraft_protection = overdraft_protection  # Indicator of whether the account has overdraft protection enabled.
        self.account_tier = account_tier  # Current level of the account
        self.transaction_limit = transaction_limit  # Limits on the number or amount of transactions allowed within a certain period.

    def register(self):
        """Method to register a new user with the bank app, including capturing and validating personal information
        such as name, address, contact details, and identification documents."""

        query = f"""
                insert into {self.database.db_tables[3]}
                (account_number, account_type, account_holder, account_balance, transaction_pin, account_status, 
                account_tier, overdraft_protection, transaction_limit)
                values('{self.account_number}', '{self.account_type}', '{self.account_holder}', 
                {self.account_balance}, '{self.transaction_pin}', '{self.account_status}', '{self.account_tier}',
                '{self.overdraft_protection}', '{self.transaction_limit}')
                """

        self.database.query(query)

    def deposit(self):
        """Method to allow users to deposit money into their account. It should update the account balance
        accordingly."""
        pass

    def withdraw(self):
        """Method to allow users to withdraw money from their account. It should update the account balance and handle
        cases where the withdrawal amount exceeds the available balance."""
        pass

    def transfer(self):
        """Method to facilitate transferring funds between accounts. It should handle transferring money from one
        account to another, updating the balances of both accounts involved."""
        pass

    def get_balance(self):
        """Method to retrieve the current balance of the account."""
        pass

    def transaction_history(self):
        """Method to retrieve the transaction history of the account, including details such as transaction type,
        amount, date, and counterparty information."""
        pass

    def calculate_interest(self):
        """Method to calculate and apply interest to the account balance, if applicable (e.g., for savings accounts
        or investment accounts)."""
        pass

    def close_account(self):
        """Method to allow users to close their account. It should handle any necessary cleanup tasks, such as
        transferring remaining funds and closing associated records."""
        pass

    def account_validation(self):
        """Method to validate the account, ensuring that it meets any requirements or constraints imposed by the bank
        or regulatory authorities."""
        pass

    def transaction_limits(self):
        """Method to enforce transaction limits, such as daily withdrawal limits or maximum transfer amounts, to
        prevent fraudulent or unauthorized transactions."""
        pass


class Savings(Account):
    __minimum_balance: float = 500.0  # Minimum balance required to avoid fees or maintain the account.
    __account_fees: float = 100.0  # fees associated with the account, such as monthly maintenance fees.

    def __init__(self):
        super().__init__()

    def deposit(self):
        """Method to allow users to deposit money into their account. It should update the account balance
        accordingly."""
        pass

    def withdraw(self):
        """Method to allow users to withdraw money from their account. It should update the account balance and handle
        cases where the withdrawal amount exceeds the available balance."""
        pass

    def transfer(self):
        """Method to facilitate transferring funds between accounts. It should handle transferring money from one
        account to another, updating the balances of both accounts involved."""
        pass

    @property
    def minimum_balance(self):
        return self.__minimum_balance

    @property
    def account_fees(self):
        return self.__account_fees


class Current(Account):
    __minimum_balance: float = 5000.0
    __account_fees: float = 1000.0  # fees associated with the account, such as monthly maintenance fees.

    def __init__(self):
        super().__init__()

    def deposit(self):
        """Method to allow users to deposit money into their account. It should update the account balance
        accordingly."""
        pass

    def withdraw(self):
        """Method to allow users to withdraw money from their account. It should update the account balance and handle
        cases where the withdrawal amount exceeds the available balance."""
        pass

    def transfer(self):
        """Method to facilitate transferring funds between accounts. It should handle transferring money from one
        account to another, updating the balances of both accounts involved."""
        pass

    @property
    def minimum_balance(self):
        return self.__minimum_balance

    @property
    def account_fees(self):
        return self.__account_fees


class FixedDeposit(Account):
    def __init__(self, interest_rate: float = 0.0, interest_earned: float = 0.0):
        super().__init__()
        self.interest_rate = interest_rate  # Interest rate applied to the account balance (if applicable).
        self.interest_earned = interest_earned  # Total amount of interest earned on the account balance.

    def deposit(self):
        """Method to allow users to deposit money into their account. It should update the account balance
        accordingly."""
        pass

    def withdraw(self):
        """Method to allow users to withdraw money from their account. It should update the account balance and handle
        cases where the withdrawal amount exceeds the available balance."""
        pass
