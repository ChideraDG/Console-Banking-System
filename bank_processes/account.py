import datetime
import json
from abc import abstractmethod, ABC
from bank_processes.user import User


class Account(User):
    currency: str = 'Naira'  # Currency in which the account is denominated.

    def __init__(self, account_number: str = None, account_type: str = None, account_holder: str = None,
                 account_balance: float = None, minimum_balance: float = None, maximum_balance: float = None,
                 account_fee: float = None, transaction_pin: str = None, account_status: str = None,
                 account_tier: str = None, transaction_limit: int = None, overdraft_protection: str = None,
                 beneficiaries: dict = None, transfer_limit: float = None, fixed_account: str = None):
        super().__init__()
        self.__account_number = account_number  # Unique identifier for the account.
        self.__account_type = account_type  # Type of account (e.g., savings, checking, credit card).
        self.__account_holder = account_holder  # User or users associated with the account.
        self.__account_balance = account_balance  # Current balance of the account.
        self.__minimum_balance = minimum_balance  # Minimum balance required to avoid fees or maintain the account.
        self.__maximum_balance = maximum_balance
        self.__account_fee = account_fee  # fees associated with the account, such as monthly maintenance fees.
        self.__transaction_pin = transaction_pin  # Pin used for transaction authentication.
        self.__account_status = account_status  # Status of the account (e.g., active, closed, frozen).
        self.__overdraft_protection = overdraft_protection  # Indicator of whether the account has overdraft protection enabled.
        self.__account_tier = account_tier  # Current level of the account
        self.__transaction_limit = transaction_limit  # Limits on the number or amount of transactions allowed within a certain period.
        self.__transfer_limit = transfer_limit
        self.__beneficiaries = beneficiaries  # Beneficiaries of the Account
        self.__fixed_account = fixed_account

    def open_account(self):
        """Method to register a new user with the bank app, including capturing and validating personal information
        such as name, address, contact details, and identification documents."""

        query = f"""
                INSERT INTO {self.database.db_tables[3]}
                (account_number, 
                account_type, 
                account_holder, 
                account_balance, 
                minimum_balance, 
                maximum_balance, 
                account_fee, 
                transaction_pin, 
                account_status, 
                account_tier, 
                overdraft_protection, 
                transaction_limit, 
                transfer_limit)
                VALUES(
                '{self.__account_number}', 
                '{self.__account_type}', 
                '{self.__account_holder}', 
                {self.__account_balance}, 
                {self.__minimum_balance}, 
                {self.__maximum_balance}, 
                {self.__account_fee}, 
                '{self.__transaction_pin}', 
                '{self.__account_status}', 
                '{self.__account_tier}', 
                '{self.__overdraft_protection}', 
                {self.__transaction_limit}, 
                {self.__transfer_limit})
                """

        self.database.query(query)

    @abstractmethod
    def deposit(self):
        """Method to allow users to deposit money into their account. It should update the account balance
        accordingly."""
        pass

    @abstractmethod
    def withdraw(self):
        """Method to allow users to withdraw money from their account. It should update the account balance and handle
        cases where the withdrawal amount exceeds the available balance."""
        pass

    @abstractmethod
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

    def block_account(self):
        """Method to block user accounts after multiple failed pin attempts, preventing brute force
        attacks and unauthorized access."""
        query = (f""" 
        UPDATE {self.database.db_tables[3]}
        SET account_status = 'blocked'
        WHERE account_number = {self.account_number}
        """)

        self.database.query(query)

    def add_beneficiaries(self, _account_number: str, _account_holder: str):
        """Method to add new beneficiaries to an Account"""
        value = len(self.beneficiaries)

        self.__beneficiaries.update({str(value + 1): [_account_number, _account_holder]})

        query = (f"""
        UPDATE {self.database.db_tables[3]}
        SET beneficiaries = '{str(self.__beneficiaries).replace("'", '"')}'
        WHERE account_number = {self.account_number}
        """)
        self.database.query(query)

    def for_debugging(self):
        """For Debugging"""
        return f"""{self.account_number} {self.account_type} {self.account_balance} {self.account_holder} 
{self.account_tier} {self.account_status} {self.transaction_limit} {self.overdraft_protection} {self.transaction_pin}"""

    @property
    def account_number(self):
        if self.user_id is not None:
            query = (f"""
            SELECT account_number 
            FROM {self.database.db_tables[3]} 
            WHERE account_id = {self.user_id}
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for account_number in data:
                    self.account_number = account_number

        return self.__account_number

    @account_number.setter
    def account_number(self, _account_number: str):
        self.__account_number = _account_number

    @account_number.deleter
    def account_number(self):
        del self.__account_number

    @property
    def account_type(self):
        if self.account_number is not None:
            query = (f"""
            SELECT account_type 
            FROM {self.database.db_tables[3]} 
            WHERE account_number = '{self.account_number}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for account_type in data:
                    self.account_type = account_type

        return self.__account_type

    @account_type.setter
    def account_type(self, _account_type: str):
        self.__account_type = _account_type

    @account_type.deleter
    def account_type(self):
        del self.__account_type

    @property
    def account_holder(self):
        if self.account_number is not None:
            query = (f"""
            SELECT account_holder 
            FROM {self.database.db_tables[3]} 
            WHERE account_number = '{self.account_number}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for account_holder in data:
                    self.account_holder = account_holder

        return self.__account_holder

    @account_holder.setter
    def account_holder(self, _account_holder: str):
        self.__account_holder = _account_holder

    @account_holder.deleter
    def account_holder(self):
        del self.__account_holder

    @property
    def account_balance(self):
        if self.account_number is not None:
            query = (f"""
            SELECT account_balance 
            FROM {self.database.db_tables[3]} 
            WHERE account_number = '{self.account_number}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for account_balance in data:
                    self.account_balance = account_balance

        return self.__account_balance

    @account_balance.setter
    def account_balance(self, _account_balance: float):
        self.__account_balance = _account_balance

    @account_balance.deleter
    def account_balance(self):
        del self.__account_balance

    @property
    def transaction_pin(self):
        if self.account_number is not None:
            query = (f"""
            SELECT transaction_pin 
            FROM {self.database.db_tables[3]} 
            WHERE account_number = '{self.account_number}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for transaction_pin in data:
                    self.transaction_pin = transaction_pin

        return self.__transaction_pin

    @transaction_pin.setter
    def transaction_pin(self, _transaction_pin: str):
        self.__transaction_pin = _transaction_pin

    @transaction_pin.deleter
    def transaction_pin(self):
        del self.__transaction_pin

    @property
    def account_status(self):
        if self.account_number is not None:
            query = (f"""
            SELECT account_status 
            FROM {self.database.db_tables[3]} 
            WHERE account_number = '{self.account_number}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for account_status in data:
                    self.account_status = account_status

        return self.__account_status

    @account_status.setter
    def account_status(self, _account_status: str):
        self.__account_status = _account_status

    @account_status.deleter
    def account_status(self):
        del self.__account_status

    @property
    def overdraft_protection(self):
        if self.account_number is not None:
            query = (f"""
            SELECT overdraft_protection 
            FROM {self.database.db_tables[3]} 
            WHERE account_number = '{self.account_number}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for overdraft_protection in data:
                    self.overdraft_protection = overdraft_protection

        return self.__overdraft_protection

    @overdraft_protection.setter
    def overdraft_protection(self, _overdraft_protection: str):
        self.__overdraft_protection = _overdraft_protection

    @overdraft_protection.deleter
    def overdraft_protection(self):
        del self.__overdraft_protection

    @property
    def account_tier(self):
        if self.account_number is not None:
            query = (f"""
            SELECT account_tier 
            FROM {self.database.db_tables[3]} 
            WHERE account_number = '{self.account_number}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for account_tier in data:
                    self.account_tier = account_tier

        return self.__account_tier

    @account_tier.setter
    def account_tier(self, _account_tier: str):
        self.__account_tier = _account_tier

    @account_tier.deleter
    def account_tier(self):
        del self.__account_tier

    @property
    def transaction_limit(self):
        if self.account_number is not None:
            query = (f"""
            SELECT transaction_limit 
            FROM {self.database.db_tables[3]} 
            WHERE account_number = '{self.account_number}'
            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for transaction_limit in data:
                    self.transaction_limit = transaction_limit

        return self.__transaction_limit

    @transaction_limit.setter
    def transaction_limit(self, _transaction_limit: int):
        self.__transaction_limit = _transaction_limit

    @transaction_limit.deleter
    def transaction_limit(self):
        del self.__transaction_limit

    @property
    def beneficiaries(self):
        if self.account_number is not None:
            query = (f"""
                SELECT beneficiaries 
                FROM {self.database.db_tables[3]} 
                WHERE account_number = '{self.account_number}'
                """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for beneficiaries in data:
                    self.beneficiaries = json.loads(beneficiaries)

        return self.__beneficiaries

    @beneficiaries.setter
    def beneficiaries(self, _beneficiaries: dict):
        self.__beneficiaries = _beneficiaries

    @beneficiaries.deleter
    def beneficiaries(self):
        del self.__beneficiaries

    @property
    def minimum_balance(self):
        if self.account_number is not None:
            query = (f"""
                    SELECT minimum_balance 
                    FROM {self.database.db_tables[3]} 
                    WHERE account_number = '{self.account_number}'
                    """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for minimum_balance in data:
                    self.minimum_balance = minimum_balance

        return self.__minimum_balance

    @minimum_balance.setter
    def minimum_balance(self, _minimum_balance: dict):
        self.__minimum_balance = _minimum_balance

    @minimum_balance.deleter
    def minimum_balance(self):
        del self.__minimum_balance

    @property
    def account_fee(self):
        if self.account_number is not None:
            query = (f"""
                    SELECT account_fee 
                    FROM {self.database.db_tables[3]} 
                    WHERE account_number = '{self.account_number}'
                    """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for account_fee in data:
                    self.account_fee = account_fee

        return self.__account_fee

    @account_fee.setter
    def account_fee(self, _account_fee: dict):
        self.__account_fee = _account_fee

    @account_fee.deleter
    def account_fee(self):
        del self.__account_fee

    @property
    def maximum_balance(self):
        if self.account_number is not None:
            query = (f"""
                        SELECT maximum_balance 
                        FROM {self.database.db_tables[3]} 
                        WHERE account_number = '{self.account_number}'
                        """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for maximum_balance in data:
                    self.maximum_balance = maximum_balance

        return self.__maximum_balance

    @maximum_balance.setter
    def maximum_balance(self, _maximum_balance: dict):
        self.__maximum_balance = _maximum_balance

    @maximum_balance.deleter
    def maximum_balance(self):
        del self.__maximum_balance

    @property
    def transfer_limit(self):
        if self.account_number is not None:
            query = (f"""
                        SELECT transfer_limit 
                        FROM {self.database.db_tables[3]} 
                        WHERE account_number = '{self.account_number}'
                        """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for transfer_limit in data:
                    self.transfer_limit = transfer_limit

        return self.__transfer_limit

    @transfer_limit.setter
    def transfer_limit(self, _transfer_limit: dict):
        self.__transfer_limit = _transfer_limit

    @transfer_limit.deleter
    def transfer_limit(self):
        del self.__transfer_limit

    @property
    def fixed_account(self):
        if self.account_number is not None:
            query = (f"""
                            SELECT fixed_account 
                            FROM {self.database.db_tables[3]} 
                            WHERE account_number = '{self.account_number}'
                            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for fixed_account in data:
                    self.fixed_account = fixed_account

        return self.__fixed_account

    @fixed_account.setter
    def fixed_account(self, _fixed_account: dict):
        self.__fixed_account = _fixed_account

    @fixed_account.deleter
    def fixed_account(self):
        del self.__fixed_account


class FixedDeposit(Account, ABC):
    def __init__(self, deposit_id: str = None, deposit_title: str = None, initial_deposit: float = None,
                 interest_rate: float = None, total_interest_earned: float = None, start_date: datetime.date = None,
                 payback_date: datetime.date = None, payback_time: datetime.time = None, status: str = None):
        super().__init__()
        self.__deposit_id = deposit_id
        self.__deposit_title = deposit_title
        self.__initial_deposit = initial_deposit
        self.__interest_rate = interest_rate  # Interest rate applied to the account balance (if applicable).
        self.__total_interest_earned = total_interest_earned  # Total amount of interest earned on the account balance.
        self.__start_date = start_date
        self.__payback_date = payback_date
        self.__payback_time = payback_time
        self.__status = status

    def deposit(self):
        """Method to allow users to deposit money into their account. It should update the account balance
        accordingly."""
        pass

    def withdraw(self):
        """Method to allow users to withdraw money from their account. It should update the account balance and handle
        cases where the withdrawal amount exceeds the available balance."""
        pass

    @property
    def deposit_id(self):
        if self.account_number is not None:
            query = (f"""
                    SELECT deposit_id 
                    FROM {self.database.db_tables[4]} 
                    WHERE account_number = '{self.account_number}'
                    """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for deposit_id in data:
                    self.deposit_id = deposit_id

        return self.__deposit_id

    @deposit_id.setter
    def deposit_id(self, _deposit_id):
        self.__deposit_id = _deposit_id

    @deposit_id.deleter
    def deposit_id(self):
        del self.__deposit_id

    @property
    def deposit_title(self):
        if self.account_number is not None:
            query = (f"""
                            SELECT deposit_title 
                            FROM {self.database.db_tables[3]} 
                            WHERE account_number = '{self.account_number}'
                            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for deposit_title in data:
                    self.deposit_title = deposit_title

        return self.__deposit_title

    @deposit_title.setter
    def deposit_title(self, _deposit_title):
        self.__deposit_title = _deposit_title

    @deposit_title.deleter
    def deposit_title(self):
        del self.__deposit_title

    @property
    def initial_deposit(self):
        if self.account_number is not None:
            query = (f"""
                            SELECT initial_deposit 
                            FROM {self.database.db_tables[3]} 
                            WHERE account_number = '{self.account_number}'
                            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for initial_deposit in data:
                    self.initial_deposit = initial_deposit

        return self.__initial_deposit

    @initial_deposit.setter
    def initial_deposit(self, _initial_deposit):
        self.__initial_deposit = _initial_deposit

    @initial_deposit.deleter
    def initial_deposit(self):
        del self.__initial_deposit

    @property
    def total_interest_earned(self):
        if self.account_number is not None:
            query = (f"""
                            SELECT total_interest_earned 
                            FROM {self.database.db_tables[3]} 
                            WHERE account_number = '{self.account_number}'
                            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for total_interest_earned in data:
                    self.total_interest_earned = total_interest_earned

        return self.__total_interest_earned

    @total_interest_earned.setter
    def total_interest_earned(self, _total_interest_earned):
        self.__total_interest_earned = _total_interest_earned

    @total_interest_earned.deleter
    def total_interest_earned(self):
        del self.__total_interest_earned

    @property
    def start_date(self):
        if self.account_number is not None:
            query = (f"""
                            SELECT start_date 
                            FROM {self.database.db_tables[3]} 
                            WHERE account_number = '{self.account_number}'
                            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for start_date in data:
                    self.start_date = start_date

        return self.__start_date

    @start_date.setter
    def start_date(self, _start_date):
        self.__start_date = _start_date

    @start_date.deleter
    def start_date(self):
        del self.__start_date

    @property
    def payback_date(self):
        if self.account_number is not None:
            query = (f"""
                            SELECT payback_date 
                            FROM {self.database.db_tables[3]} 
                            WHERE account_number = '{self.account_number}'
                            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for payback_date in data:
                    self.payback_date = payback_date

        return self.__payback_date

    @payback_date.setter
    def payback_date(self, _payback_date):
        self.__payback_date = _payback_date

    @payback_date.deleter
    def payback_date(self):
        del self.__payback_date

    @property
    def payback_time(self):
        if self.account_number is not None:
            query = (f"""
                        SELECT payback_time 
                        FROM {self.database.db_tables[3]} 
                        WHERE account_number = '{self.account_number}'
                        """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for payback_time in data:
                    self.payback_time = payback_time

        return self.__payback_time

    @payback_time.setter
    def payback_time(self, _payback_time):
        self.__payback_time = _payback_time

    @payback_time.deleter
    def payback_time(self):
        del self.__payback_time

    @property
    def status(self):
        if self.account_number is not None:
            query = (f"""
                            SELECT status 
                            FROM {self.database.db_tables[3]} 
                            WHERE account_number = '{self.account_number}'
                            """)

            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for status in data:
                    self.status = status

        return self.__status

    @status.setter
    def status(self, _status):
        self.__status = _status

    @status.deleter
    def status(self):
        del self.__status
