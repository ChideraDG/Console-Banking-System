import datetime
import random
from abc import ABC
from typing import Tuple, Any

from bank_processes.account import Account


class Transaction(Account, ABC):
    currency: str = 'Naira'

    def __init__(self, transaction_id: str = None,
                 transaction_type: str = None,
                 amount: float = None, transaction_date_time: datetime.datetime = None,
                 received_transaction_date_time: datetime.datetime = None,
                 receiver_acct_num: str = None,
                 description: str = None, trans_status: str = None, fees: float = None, merchant_info: str = None,
                 transaction_category: str = None, user_id: str = None, account_type: str = None,
                 receiver_name: str = None, balance: float = None, transfer_limit: float = None):
        super().__init__()
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__transaction_id = transaction_id  # unique identifier for transaction
        self.__transaction_date_time = transaction_date_time  # timestamp for when the transaction occurred
        self.__received_transaction_date_time = received_transaction_date_time
        self.__receiver_acct_num = receiver_acct_num  # receiver's account number
        self.__description = description  # description of the transaction
        self.__trans_status = trans_status  # status of the transaction
        self.__merchant_info = merchant_info  # info about the merchant or receiver
        self.__transaction_category = transaction_category  # category of the transfer
        self.__user_id = user_id  # identifier of the user who initiated the transaction
        self.__account_type = account_type  # whether fixed deposit, savings or current
        self.__receiver_name = receiver_name
        self.__balance = balance
        self.__transfer_limit = transfer_limit

    def sender_transaction_record(self):
        """Method to record new transactions made by the sender  and the relevant information"""
        from banking.register_panel import verify_data

        now = datetime.datetime.now()
        self.__transaction_date_time = now.strftime("%d %B %Y %H:%M:%S")
        self.__transaction_type = self.__transaction_type.upper()
        self.__transaction_id = str(random.randint(100000000000000000000000000000,
                                                   999999999999999999999999999999))
        while verify_data('transaction_id', 2, self.__transaction_id):
            self.__transaction_id = str({random.randint(100000000000000000000000000000,
                                                        999999999999999999999999999999)})
        sender_trans_record = ''
        if self.__transaction_type == 'TRANSFER':
            sender_trans_record = f"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        -{self.__amount}
                        {self.__trans_status}
            TRANSACTION DETAILS\n
            Transaction Type\t\t\t{self.__transaction_type}
            Recipient Details\t\t\t\t{self.__receiver_name}
                          \t\t\tBankApp|{self.__receiver_acct_num}'''
            Sender Details\t\t\t\t{self.account_holder}
                          \t\t\tBankApp|{self.account_number}'''
            Description        \t\t\t{self.__description}
            Payment Method         \t\tBalance'''
            Transaction Date      \t\t{self.__transaction_date_time}
            Transaction ID         \t\t{self.__transaction_id}
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

        elif self.__transaction_type == 'WITHDRAW':
            self.__receiver_name = ''
            self.__receiver_acct_num = ''
            sender_trans_record = f"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        -{self.__amount}
                        {self.__trans_status}
            TRANSACTION DETAILS\n
            Transaction Type\t\t\t{self.__transaction_type}
            Sender Details\t\t\t\t{self.account_holder}
                            \t\t\tBankApp|{self.account_number}'''
            Description        \t\t\t{self.__description}
            Payment Method         \t\tBalance'''
            Transaction Date      \t\t{self.__transaction_date_time}
            Transaction ID         \t\t{self.__transaction_id}
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

        elif self.__transaction_type == 'DEPOSIT':
            sender_trans_record = f"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        -{self.__amount}
                        {self.__trans_status}
            TRANSACTION DETAILS\n
            Transaction Type\t\t\t{self.__transaction_type}
            Recipient Details\t\t\t\t{self.__receiver_name}
                          \t\t\tBankApp|{self.__receiver_acct_num}'''
            Sender Details\t\t\t\t{self.account_holder}
                            \t\t\tBankApp|{self.account_number}'''
            Description        \t\t\t{self.__description}
            Payment Method         \t\tBalance'''
            Transaction Date      \t\t{self.__transaction_date_time}
            Transaction ID         \t\t{self.__transaction_id}
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
        query = f"""
                INSERT INTO {self.database.db_tables[2]}
                (transaction_id, transaction_type, transaction_amount, sender_account_number, sender_name,
                receiver_account_number, receiver_name, transaction_date_time, description, status,account_type,
                user_id)
                VALUES('{self.__transaction_id}', '{self.__transaction_type}', {self.__amount},
                '{self.account_number}', '{self.account_holder}', '{self.__receiver_acct_num}',
                '{self.__receiver_name}', {self.__transaction_date_time}, '{self.__description}'
                '{self.__trans_status}', '{self.account_type}', {self.user_id})
                 """
        self.database.query(query)
        print(sender_trans_record)

    def recipient_trans_record(self):
        """Method to record new transactions made to the receiver  and the relevant information"""
        now = datetime.datetime.now()
        self.__received_transaction_date_time = now.strftime("%d %B %Y %H:%M:%S")
        self.__transaction_type = self.__transaction_type.upper()

        receiver_trans_record = f"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            f'+{self.__amount}'
                            {self.__trans_status}
                TRANSACTION DETAILS\n
                Transaction Type\t\t\t{self.__transaction_type}
                Sender Details\t\t\t\t{self.account_holder}
                                \t\t\tBankApp|{self.account_number}'''
                Description        \t\t\t{self.__description}
                Credited to        \t\tBalance'''
                Transaction Date      \t\t{self.__received_transaction_date_time}
                Transaction ID         \t\t{self.__transaction_id}
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
        print(receiver_trans_record)

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
        debited_amount = self.amount + self.account_fee
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
        Account.account_number = self.receiver_acct_num
        if self.account_balance > self.maximum_balance:
            query = (f""" 
            UPDATE {self.database.db_tables[3]}
            SET account_status = 'blocked'
            WHERE account_number = {self.receiver_acct_num}""")
            self.database.query(query)

            return False, 'Maximum Balance passed!!!', self.account_status, self.receiver_acct_num

        else:
            return True, 'Allowed balance met', self.account_status, self.receiver_acct_num

    def process_transaction(self):
        """Method to process the transaction, including updating account balances, recording transaction details,
        and handling any necessary validations or checks."""
        pass

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
    def transfer_limit(self):
        if self.user_id is not None:
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
    def transfer_limit(self, _transfer_limit):
        self.__transfer_limit = _transfer_limit

    @transfer_limit.deleter
    def transfer_limit(self):
        del self.__transfer_limit

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, _amount):
        self.__amount = _amount

    @amount.deleter
    def amount(self):
        del self.__amount



