from datetime import datetime
import random
from abc import ABC
from typing import Tuple, Any

from bank_processes.account import Account


class Transaction(Account, ABC):
    currency: str = 'Naira'

    def __init__(self, transaction_id: str = None,
                 transaction_type: str = None,
                 amount: float = None, transaction_date_time: datetime = None,
                 received_transaction_date_time: datetime = None,
                 receiver_acct_num: str = None,
                 description: str = None, transaction_status: str = None, fees: float = None, merchant_info: str = None,
                 transaction_category: str = None, user_id: str = None, account_type: str = None,
                 receiver_name: str = None, balance: float = None, transfer_limit: float = None, charges: float = None):
        super().__init__()
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__transaction_id = transaction_id  # unique identifier for transaction
        self.__transaction_date_time = transaction_date_time  # timestamp for when the transaction occurred
        self.__received_transaction_date_time = received_transaction_date_time
        self.__receiver_acct_num = receiver_acct_num  # receiver's account number
        self.__description = description  # description of the transaction
        self.__transaction_status = transaction_status  # status of the transaction
        self.__merchant_info = merchant_info  # info about the merchant or receiver
        self.__transaction_category = transaction_category  # category of the transfer
        self.__user_id = user_id  # identifier of the user who initiated the transaction
        self.__account_type = account_type  # whether fixed deposit, savings or current
        self.__receiver_name = receiver_name
        self.__balance = balance
        self.__transfer_limit = transfer_limit
        self.__charges = charges

    def sender_transaction_record(self):
        """Method to record new transactions made by the sender  and the relevant information"""
        from banking.register_panel import verify_data
        self.__transaction_id = str(random.randint(100000000000000000000000000000,
                                                   999999999999999999999999999999))
        self.__transaction_id = str(random.randint(100000000000000000000000000000,
                                                   999999999999999999999999999999))
        while verify_data('transaction_id', 2, self.__transaction_id):
            self.__transaction_id = str({random.randint(100000000000000000000000000000,
                                                        999999999999999999999999999999)})

        query = f"""
                INSERT INTO {self.database.db_tables[2]}
                (transaction_id, transaction_type, transaction_amount, sender_account_number, sender_name,
                receiver_account_number, receiver_name, transaction_date_time, description, status,account_type,
                user_id)
                VALUES('{self.__transaction_id}', '{self.__transaction_type}', {self.__amount},
                '{self.account_number}', '{self.account_holder}', '{self.__receiver_acct_num}',
                '{self.__receiver_name}', {self.__transaction_date_time}, '{self.__description}'
                '{self.__transaction_status}', '{self.account_type}', {self.user_id})
                 """
        self.database.query(query)

    def recipient_trans_record(self):
        """Method to record new transactions made to the receiver  and the relevant information"""
        pass

    def retrieve_transaction(self):
        """Method to retrieve a list of transaction based on a certain criteria"""
        pass

    def cal_transaction_fees(self):
        """Method to calculate fees associated with the transfer depending on the amount """
        # return self.__fees + self.__amount
        pass

    def transaction_validation(self, amount: bool = False, transfer_limit: bool = False) -> tuple[bool, str]:
        """Method to validate the transaction, ensuring that it meets any requirements or constraints imposed by
        the bank or regulatory authorities. """
        debited_amount = self.amount + self.charges
        sender_updated_balance = self.account_balance - debited_amount

        if amount:
            if debited_amount > self.account_balance:
                return False, 'Insufficient Balance!!!'
            elif sender_updated_balance < self.minimum_balance:
                return False, 'Insufficient Balance!!!'

            else:
                return True, 'Sufficient Balance'

        if transfer_limit:
            if self.amount > self.transfer_limit:
                return False, 'Daily Transfer limit passed!!!'

            else:
                return True, 'Sufficient Balance'

    def receiver_transaction_validation(self) -> tuple[bool, str, Any | None, str | None]:
        """Method to validate if the receiver is allowed to receive such amount and then apply the necessary step"""
        _object = Account()
        _object.account_number = self.receiver_acct_num
        if _object.account_balance > _object.maximum_balance:
            query = (f""" 
            UPDATE {self.database.db_tables[3]}
            SET account_status = 'blocked'
            WHERE account_number = {self.receiver_acct_num}""")
            self.database.query(query)
            return False, 'Maximum Balance passed!!!', _object.account_status, self.receiver_acct_num
        del _object

    def process_transaction(self):
        """Method to process the transaction, including updating account balances, recording transaction details,
        and handling any necessary validations or checks."""
        debited_amount = self.amount + self.charges
        if self.transaction_type == 'transfer':
            sender_updated_balance = self.account_balance - debited_amount
            sender_query = f"""
            UPDATE {self.database.db_tables[3]}
            SET account_balance = {sender_updated_balance}
            WHERE account_number = {self.account_number}  
            """
            self.database.query(sender_query)

            _receiver_object = Account()
            _receiver_object.account_number = self.receiver_acct_num
            receiver_updated_balance = _receiver_object.account_balance + self.amount
            receiver_query = f"""
            UPDATE {self.database.db_tables[3]}
            SET account_balance = {receiver_updated_balance}
            WHERE account_number = {self.receiver_acct_num}
            """
            self.database.query(receiver_query)
            del _receiver_object

    def cancel_transaction(self):
        """Method to cancel a pending or incomplete transaction, reversing any changes made to account balances
        and transaction records."""
        pass

    def transaction_status_update(self):
        """Method to update the status of a transaction, such as pending, completed, or failed, based on
        its progress and outcome."""
        pass

    def transaction_authorization(self):
        """Method to authorize the transaction, verifying the identity and authorization of the user or
        entity initiating the transaction."""
        pass

    def transaction_history(self):
        """ Method to retrieve the transaction history associated with a specific account or user,
         providing details of past transactions for reference and auditing purposes."""

    @property
    def receiver_acct_num(self):
        return self.__receiver_acct_num

    @receiver_acct_num.setter
    def receiver_acct_num(self, _receiver_account_number: str):
        self.__receiver_acct_num = _receiver_account_number

    @receiver_acct_num.deleter
    def receiver_acct_num(self):
        del self.__receiver_acct_num

    @property
    def receiver_name(self):
        return self.__receiver_name

    @receiver_name.setter
    def receiver_name(self, _receiver_name):
        self.__receiver_name = _receiver_name

    @receiver_name.deleter
    def receiver_name(self):
        del self.__receiver_name

    @property
    def transfer_limit(self):
        if self.account_number is not None:
            query = (f"""
                SELECT transfer_limit 
                FROM {self.database.db_tables[3]} 
                WHERE account_number = {self.account_number}
                """)
            datas: tuple = self.database.fetch_data(query)

            for data in datas:
                for transfer_limit in data:
                    self.transfer_limit = transfer_limit

        return self.__transfer_limit

    @transfer_limit.setter
    def transfer_limit(self, _transfer_limit):
        self.__transfer_limit = _transfer_limit

    @transfer_limit.deleter
    def transfer_limit(self):
        del self.__transfer_limit

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, _amount: float):
        self.__amount = _amount

    @amount.deleter
    def amount(self):
        del self.__amount

    @property
    def transaction_date_time(self):
        transaction_time = datetime.now()
        self.transaction_date_time = transaction_time
        return self.__transaction_date_time

    @transaction_date_time.setter
    def transaction_date_time(self, _transaction_date_time):
        self.__transaction_date_time = _transaction_date_time

    @transaction_date_time.deleter
    def transaction_date_time(self):
        del self.__transaction_date_time

    @property
    def transaction_type(self):
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, _transaction_type):
        self.__transaction_type = _transaction_type

    @transaction_type.deleter
    def transaction_type(self):
        del self.__transaction_type

    @property
    def charges(self):
        if self.amount <= 5000:
            self.charges = 10.53

        elif self.amount <= 50_000:
            self.charges = 26.88

        else:
            self.charges = 53.57

        return self.__charges

    @charges.setter
    def charges(self, _charges):
        self.__charges = _charges

    @charges.deleter
    def charges(self):
        del self.__charges

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, _description):
        self.__description = _description

    @description.deleter
    def description(self):
        del self.__description
