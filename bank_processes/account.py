from abc import abstractmethod
from bank_processes.user import User


class Account(User):
    currency: str = 'Naira'  # Currency in which the account is denominated.

    def __init__(self, account_number: str = None, account_type: str = None, account_holder: str = None,
                 account_balance: float = None, transaction_pin: str = None, account_status: str = None,
                 account_tier: str = None, transaction_limit: int = None, overdraft_protection: str = None):
        super().__init__()
        self.__account_number = account_number  # Unique identifier for the account.
        self.__account_type = account_type  # Type of account (e.g., savings, checking, credit card).
        self.__account_holder = account_holder  # User or users associated with the account.
        self.__account_balance = account_balance  # Current balance of the account.
        self.__transaction_pin = transaction_pin  # Pin used for transaction authentication.
        self.__account_status = account_status  # Status of the account (e.g., active, closed, frozen).
        self.__overdraft_protection = overdraft_protection  # Indicator of whether the account has overdraft protection enabled.
        self.__account_tier = account_tier  # Current level of the account
        self.__transaction_limit = transaction_limit  # Limits on the number or amount of transactions allowed within a certain period.

    def open_account(self):
        """Method to register a new user with the bank app, including capturing and validating personal information
        such as name, address, contact details, and identification documents."""

        query = f"""
                insert into {self.database.db_tables[3]}
                (account_number, account_type, account_holder, account_balance, transaction_pin, account_status, 
                account_tier, overdraft_protection, transaction_limit)
                values('{self.__account_number}', '{self.__account_type}', '{self.__account_holder}', 
                {self.__account_balance}, '{self.__transaction_pin}', '{self.__account_status}', '{self.__account_tier}',
                '{self.__overdraft_protection}', '{self.__transaction_limit}')
                """

        self.database.query(query)

    @abstractmethod
    def deposit(self):
        """Method to allow users to deposit money into their account. It should update the account balance
        accordingly."""
        raise NotImplementedError('This Method not in Use.')

    @abstractmethod
    def withdraw(self):
        """Method to allow users to withdraw money from their account. It should update the account balance and handle
        cases where the withdrawal amount exceeds the available balance."""
        raise NotImplementedError('This Method not in Use.')

    @abstractmethod
    def transfer(self):
        """Method to facilitate transferring funds between accounts. It should handle transferring money from one
        account to another, updating the balances of both accounts involved."""
        raise NotImplementedError('This Method not in Use.')

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

    def __str__(self):
        """For Debugging"""
        return f"""{self.account_number} {self.account_type} {self.account_balance} {self.account_holder} 
{self.account_tier} {self.account_status} {self.transaction_limit} {self.overdraft_protection} {self.transaction_pin}"""

    @property
    def account_number(self):
        return self.__account_number

    @account_number.setter
    def account_number(self, _account_number: str):
        self.__account_number = _account_number

    @account_number.deleter
    def account_number(self):
        del self.__account_number

    @property
    def account_type(self):
        return self.__account_type

    @account_type.setter
    def account_type(self, _account_type: str):
        self.__account_type = _account_type

    @account_type.deleter
    def account_type(self):
        del self.__account_type

    @property
    def account_holder(self):
        return self.__account_holder

    @account_holder.setter
    def account_holder(self, _account_holder: str):
        self.__account_holder = _account_holder

    @account_holder.deleter
    def account_holder(self):
        del self.__account_holder

    @property
    def account_balance(self):
        return self.__account_balance

    @account_balance.setter
    def account_balance(self, _account_balance: float):
        self.__account_balance = _account_balance

    @account_balance.deleter
    def account_balance(self):
        del self.__account_balance

    @property
    def transaction_pin(self):
        return self.__transaction_pin

    @transaction_pin.setter
    def transaction_pin(self, _transaction_pin: str):
        self.__transaction_pin = _transaction_pin

    @transaction_pin.deleter
    def transaction_pin(self):
        del self.__transaction_pin

    @property
    def account_status(self):
        return self.__account_status

    @account_status.setter
    def account_status(self, _account_status: str):
        self.__account_status = _account_status

    @account_status.deleter
    def account_status(self):
        del self.__account_status

    @property
    def overdraft_protection(self):
        return self.__overdraft_protection

    @overdraft_protection.setter
    def overdraft_protection(self, _overdraft_protection: str):
        self.__overdraft_protection = _overdraft_protection

    @overdraft_protection.deleter
    def overdraft_protection(self):
        del self.__overdraft_protection

    @property
    def account_tier(self):
        return self.__account_tier

    @account_tier.setter
    def account_tier(self, _account_tier: str):
        self.__account_tier = _account_tier

    @account_tier.deleter
    def account_tier(self):
        del self.__account_tier

    @property
    def transaction_limit(self):
        return self.__transaction_limit

    @transaction_limit.setter
    def transaction_limit(self, _transaction_limit: int):
        self.__transaction_limit = _transaction_limit

    @transaction_limit.deleter
    def transaction_limit(self):
        del self.__transaction_limit


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
