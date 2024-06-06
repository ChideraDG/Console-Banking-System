import time
from datetime import datetime
import random
from abc import ABC
from typing import Tuple, Any
from prettytable import PrettyTable
from animation.colors import *
from pymysql.cursors import DictCursor
from bank_processes.account import Account


def get_month_values(input_month: str, input_year: int):
    """ function to return the numerical value of a month and the last days in any month in a tuple"""

    # Determine the number of days in February based on whether it is a leap year
    february_days = 29 if input_year % 4 == 0 else 28
    # Dictionary of the number of days in each month and their corresponding numeric values
    month_values = {'january': (31, 1), 'february': (february_days, 2), 'march': (31, 3), 'april': (30, 4),
                    'may': (31, 5), 'june': (30, 6), 'july': (31, 7), 'august': (31, 8), 'september': (30, 9),
                    'october': (31, 10), 'november': (30, 11), 'december': (31, 12)}

    # Get the numeric value and end day for the specified month
    month_val = month_values.get(input_month.lower())
    # return the month value and ending day of the specified month
    return month_val


class Transaction(Account, ABC):
    currency: str = 'Naira'

    def __init__(self, transaction_id: str = None,
                 transaction_type: str = None,
                 amount: float = None, transaction_date_time: datetime = None,
                 received_transaction_date_time: datetime = None,
                 receiver_acct_num: str = None,
                 description: str = None, transaction_status: str = None, fees: float = None, merchant_info: str = None,
                 transaction_category: str = None, user_id: str = None, account_type: str = None,
                 receiver_name: str = None, balance: float = None, transfer_limit: float = None, charges: float = None,
                 transaction_mode: str = None):
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
        self.__transaction_mode = transaction_mode

    def transaction_record(self, transfer: bool = False, fixed_deposit: bool = False, withdrawal: bool = False,
                           deposit: bool = False, central_bank: bool = False):
        """Method to record new transactions made by the sender and the relevant information

        Parameters
        ----------
        transfer : bool, optional
            If set to True, records a transfer transaction.
        fixed_deposit : bool, optional
            If set to True, records a fixed deposit transaction.
        withdrawal: bool, optional
            If set to True, records a withdrawal transaction.
        deposit: bool, optional
            If set to True, records a deposit transaction
        central_bank: bool, optional
            If set to True, record a central bank deposit
        """
        from banking.register_panel import verify_data
        self.__transaction_id = 'cbb' + str(random.randint(10000000000000000000000000,
                                                           99999999999999999999999999))
        while verify_data('transaction_id', 2, self.__transaction_id):
            self.__transaction_id = 'cbb' + str({random.randint(10000000000000000000000000,
                                                                99999999999999999999999999)})
        if transfer:
            self.__transaction_status = 'successful'

            try:
                query = f"""
                        INSERT INTO {self.database.db_tables[2]}
                        (transaction_id, transaction_type, transaction_amount, sender_account_number, sender_name,
                        receiver_account_number, receiver_name, transaction_date_time, description, status, account_type,
                        account_balance, transaction_mode)
                        VALUES('{self.__transaction_id}', '{self.__transaction_type}', '{self.__amount + self.charges}',
                        '{self.account_number}', '{self.account_holder}', '{self.__receiver_acct_num}',
                        '{self.__receiver_name}', '{self.__transaction_date_time}', '{self.__description}',
                        '{self.__transaction_status}', '{self.account_type}', '{self.account_balance}', 'debit')
                         """
                self.database.query(query)

                _receiver_obj = Account()
                _receiver_obj.account_number = self.receiver_acct_num
                receiver_description = f'TRF/CBB/TO {self.__receiver_name.upper()} FROM {self.account_holder.upper()}'
                receiver_query = f"""
                                INSERT INTO {self.database.db_tables[2]}
                                (transaction_id, transaction_type, transaction_amount, sender_account_number, sender_name,
                                receiver_account_number, receiver_name, transaction_date_time, description, status,
                                account_type, account_balance, transaction_mode)
                                VALUES('{self.__transaction_id}', '{self.transaction_type}', '{self.__amount}',
                                '{self.account_number}', '{self.account_holder}', '{self.receiver_acct_num}',
                                '{self.__receiver_name}', '{self.__transaction_date_time}', '{receiver_description}',
                                '{self.__transaction_status}', '{_receiver_obj.account_type}', 
                                '{_receiver_obj.account_balance}', 'credit')
                                """
                self.database.query(receiver_query)
            except Exception:
                # Rollback changes if an error occurs
                self.database.rollback()

            del _receiver_obj
        elif fixed_deposit:
            self.__transaction_type = 'fixed_deposit'
            self.__transaction_status = 'successful'
            self.account_type = 'fixed_deposit'

            try:
                query = f"""
                        INSERT INTO {self.database.db_tables[2]}
                        (transaction_id, transaction_type, transaction_amount, sender_account_number, sender_name,
                        receiver_account_number, receiver_name, transaction_date_time, description, status, account_type,
                        account_balance, transaction_mode)
                        VALUES('{self.__transaction_id}', '{self.__transaction_type}', '{self.__amount}',
                        '{self.account_number}', '{self.account_holder}', 'NULL',
                        'NULL', '{self.__transaction_date_time}', '{self.__description}',
                        '{self.__transaction_status}', '{self.account_type}', '{self.account_balance}', 'debit')
                        """
                self.database.query(query)
            except Exception:
                # Rollback changes if an error occurs
                self.database.rollback()

        elif withdrawal:
            self.__transaction_type = 'withdrawal'
            self.__transaction_status = 'successful'

            try:
                query = f"""
                        INSERT INTO {self.database.db_tables[2]}
                        (transaction_id, transaction_type, transaction_amount, sender_account_number, sender_name,
                        receiver_account_number, receiver_name, transaction_date_time, description, status, account_type,
                        account_balance, transaction_mode)
                        VALUES('{self.__transaction_id}', '{self.__transaction_type}', '{self.__amount}',
                        '{self.account_number}', '{self.account_holder}', 'NULL',
                        'NULL', '{self.__transaction_date_time}', '{self.__description}',
                        '{self.__transaction_status}', '{self.account_type}', '{self.account_balance}', 'debit')
                        
                """
                self.database.query(query)

            except Exception:
                # Rollback changes if an error occurs
                self.database.rollback()

        elif deposit:
            self.__transaction_type = 'deposit'
            self.__transaction_status = 'successful'

            try:
                query = f"""
                        INSERT INTO {self.database.db_tables[2]}
                        (transaction_id, transaction_type, transaction_amount, sender_account_number, sender_name,
                        receiver_account_number, receiver_name, transaction_date_time, description, status, account_type,
                        account_balance, transaction_mode)
                        VALUES('{self.__transaction_id}', '{self.__transaction_type}', '{self.__amount}',
                        'NULL', 'NULL', '{self.account_number}', '{self.account_holder}', 
                        '{self.__transaction_date_time}', '{self.__description}', '{self.__transaction_status}', 
                        '{self.account_type}', '{self.account_balance}', 'credit')

                """
                self.database.query(query)

            except Exception:
                # Rollback changes if an error occurs
                self.database.rollback()

        elif central_bank:
            self.__transaction_type = 'deposit'
            self.__transaction_status = 'successful'

            try:
                query = f"""
                                    INSERT INTO {self.database.db_tables[2]}
                                    (transaction_id, transaction_type, transaction_amount, sender_account_number, sender_name,
                                    receiver_account_number, receiver_name, transaction_date_time, description, status, account_type,
                                    account_balance, transaction_mode)
                                    VALUES('{self.__transaction_id}', '{self.__transaction_type}', '{self.__amount}',
                                    'NULL', 'NULL', '1000000009', 'CENTRAL BANK', '{self.__transaction_date_time}', 
                                    '{self.__description}', '{self.__transaction_status}', 
                                    '{self.account_type}', '{self.central_bank}', 'credit')

                            """
                self.database.query(query)

            except Exception:
                # Rollback changes if an error occurs
                self.database.rollback()

    def transaction_receipts(self, user_session_token):
        """Method to generate receipts for each transaction made"""

        print('                      {bold}TRANSACTION RECEIPT')
        print('+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+')
        print('| You sent:                                                    |')
        print(f'| {bold}{self.amount}                                         |')
        print('|                                                              |')
        print('| Recipient:                                                   |')
        print(f'| {bold}{self.receiver_name}{' ' * (52 - (len(self.receiver_name) - 9))}|')
        print('|                                                              |')
        print('| Recipient Bank:                   Recipient Account Number:  |')
        print(f'| {bold}Console Beta Bank         {bold}{self.receiver_acct_num}')
        print('|                                                              |')
        print('| Description:                                                 |')
        print(f'| {bold}{self.description}')
        print('|                                                              |')
        print(f'Sent {bold}{self.amount} to Console Beta Bank-{bold}{self.receiver_acct_num}')
        print('|                                                              |')
        print(f'| Date:                                                        |')
        print(f'| {bold}{self.__transaction_date_time}')
        print('|                                                              |')
        print('| Transaction type:                Transaction status:         |')
        print(f'| {bold}{self.transaction_type}                    {bold}{self.__transaction_status}')
        print('|                                                              |')
        print('+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+')
        print('| Transaction reference:                                       |')
        print(f'| {bold}{self.__transaction_id}                                |')
        print('|                                                              |')
        print('| Status:                                                      |')
        print(f'| {bold}{self.__transaction_status}                            |')
        print('|                                                              |')
        print('| Session ID:                                                  |')
        print(f'| {bold}{user_session_token}                                   |')
        print('+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+\n')

    def retrieve_transaction(self):
        """Method to retrieve a list of transaction based on a certain criteria"""
        pass

    def cal_transaction_fees(self):
        """Method to calculate fees associated with the transfer depending on the amount """
        # return self.__fees + self.__amount
        pass

    def transaction_validation(self, amount: bool = False, transfer_limit: bool = False) -> tuple[bool, str]:
        """Method to validate the transaction, ensuring that it meets any requirements or constraints imposed by
        the bank or regulatory authorities.

        Parameters
        ----------
        amount : bool, optional
            If set to True, validates whether the user's account has sufficient funds for the transaction.
        transfer_limit : bool, optional
            If set to True, validates whether the transaction amount exceeds the user's daily transfer limit.

        Returns
        -------
        tuple[bool, str]
            A tuple where the first element is a boolean indicating if the validation passed (True) or failed (False),
            and the second element is a string message describing the result.
        """
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
        """Validate if the receiver can receive the specified amount and apply necessary steps.

        This method checks if the receiver's account balance exceeds the maximum allowed balance.
        If so, it updates the receiver's account status to 'blocked'.

        Returns
        -------
        tuple[bool, str, Optional[Any], Optional[str]]
            A tuple containing:
            - A boolean indicating if the validation was successful.
            - A message describing the validation result.
            - The account status of the receiver (if applicable).
            - The account number of the receiver (if applicable).
        """
        # Create an Account object for the receiver
        _object = Account()
        _object.account_number = self.receiver_acct_num

        # Check if the receiver's account balance exceeds the maximum balance
        if _object.account_balance > _object.maximum_balance:
            # Query to update the receiver's account status to 'blocked'
            query = f"""
            UPDATE {self.database.db_tables[3]}
            SET account_status = 'blocked'
            WHERE account_number = {self.receiver_acct_num}
            """
            # Execute the query
            self.database.query(query)

            # Return the validation result
            return False, 'Maximum Balance passed!!!', _object.account_status, self.receiver_acct_num

        # Clean up the _object instance
        del _object

    def process_transaction(self, transfer: bool = False, fixed_deposit: bool = False, withdrawal: bool = False,
                            deposit: bool = False, central_bank: bool = False):
        """Method to process the transaction, including updating account balances, recording transaction details,
        and handling any necessary validations or checks.

        Parameters
        ----------

        transfer : bool, optional
            If set to True, processes a transfer transaction between accounts.
        fixed_deposit : bool, optional
            If set to True, processes a fixed deposit transaction.
        withdrawal: bool, optional
            If set to True, processes a withdrawal transaction.
        deposit: bool, optional
            If set to True, processes a deposit transaction
        central_bank: bool, optional
            If set to True, processes a central bank deposit
        """
        debited_amount = self.amount + self.charges
        updated_transaction_limit = self.transaction_limit - 1
        updated_transfer_limit = self.transfer_limit - self.amount
        self.__transaction_date_time = datetime.now()
        if transfer:
            try:
                sender_updated_balance = self.account_balance - debited_amount
                sender_query = f"""
                UPDATE {self.database.db_tables[3]}
                SET account_balance = '{sender_updated_balance}', transaction_limit = {updated_transaction_limit},
                transfer_limit = '{updated_transfer_limit}'
                WHERE account_number = {self.account_number}  
                """
                self.database.query(sender_query)

                _receiver_object = Account()
                _receiver_object.account_number = self.receiver_acct_num
                receiver_updated_balance = _receiver_object.account_balance + self.amount
                receiver_query = f"""
                UPDATE {self.database.db_tables[3]}
                SET account_balance = '{receiver_updated_balance}'
                WHERE account_number = {self.receiver_acct_num}
                """
                self.database.query(receiver_query)
            except Exception:
                # Rollback changes if an error occurs
                self.database.rollback()

            del _receiver_object
        elif fixed_deposit:
            sender_updated_balance = self.account_balance - self.amount
            query = f"""
            UPDATE {self.database.db_tables[3]}
            SET account_balance = '{sender_updated_balance}', transaction_limit = {updated_transaction_limit},
            transfer_limit = '{updated_transfer_limit}'
            WHERE account_number = {self.account_number}  
            """
            self.database.query(query)

        elif withdrawal:
            withdrawer_updated_balance = self.account_balance - self.amount
            query = f"""
            UPDATE {self.database.db_tables[3]}
            SET account_balance = '{withdrawer_updated_balance}', transaction_limit = {updated_transaction_limit},
            transfer_limit = '{updated_transfer_limit}'
            WHERE account_number = {self.account_number}  
            """
            self.database.query(query)

        elif deposit:
            depositor_updated_balance = self.account_balance + self.amount
            query = f"""
            UPDATE {self.database.db_tables[3]}
            SET account_balance = '{depositor_updated_balance}'
            WHERE account_number = {self.account_number}  
            """
            self.database.query(query)

        elif central_bank:
            updated_balance = self.central_bank + self.amount
            query = f"""
                    UPDATE {self.database.db_tables[3]}
                    SET account_balance = '{updated_balance}'
                    WHERE account_number = '1000000009'
                    """
            self.database.query(query)

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

    def transaction_statement(self, start_date: datetime = None, end_date: datetime = None, time_period: bool = False):
        """Method to generate a statement of account providing a summary of all transactions within a particular
        period of time by a user.
        Parameters
        ----------
        start_date : datetime, optional
            The start date for the transaction statement query.
        end_date : datetime, optional
            The end date for the transaction statement query.
        time_period : bool, optional
            Flag to indicate if a specific time period (start_date to end_date) should be used.
        """

        # Store the original cursor and switch to a dictionary cursor for this query
        original = self.database.db_cursor
        self.database.db_cursor = self.database.db_connection.cursor(DictCursor)
        if time_period:
            # Query to get transaction details where the user is the sender within the specified date range
            user_sender_query = f"""select transaction_date_time, description, transaction_id, transaction_amount,
                                account_balance
                                FROM {self.database.db_tables[2]} WHERE sender_account_number = '{self.account_number}'
                                AND transaction_date_time BETWEEN '{start_date}' AND '{end_date}'
                                """
            sender_data = list(self.database.fetch_data(user_sender_query))
            # creating an  empty list
            user_data_debit = []
            for data in sender_data:
                # create two keys for debit amount and credit amount to replace transaction_amount key
                # add the rest too
                new_sender_data = {'transaction_date_time': data['transaction_date_time'],
                                   'description': data['description'], 'transaction_id': data['transaction_id'],
                                   'debit_transaction_amount': data['transaction_amount'],
                                   'credit_transaction_amount': ' ', 'account_balance': data['account_balance']}
                # appending each dictionary to the list created earlier
                user_data_debit.append(new_sender_data)

            # Query to get transaction details where the user is the receiver within the specified date range
            user_receiver_query = f"""select transaction_date_time, description, transaction_id, transaction_amount,
                                account_balance
                            FROM {self.database.db_tables[2]} WHERE receiver_account_number = '{self.account_number}'
                            AND transaction_date_time BETWEEN '{start_date}' AND '{end_date}'
                            """
            receiver_data = list(self.database.fetch_data(user_receiver_query))
            # creating an  empty list
            user_data_credit = []
            for data2 in receiver_data:
                # create two keys for debit amount and credit amount to replace transaction_amount key
                # add the rest too
                new_receiver_data = {'transaction_date_time': data2['transaction_date_time'],
                                     'description': data2['description'], 'transaction_id': data2['transaction_id'],
                                     'credit_transaction_amount': data2['transaction_amount'],
                                     'debit_transaction_amount': ' ', 'account_balance': data2['account_balance']}
                # appending each dictionary to the list created earlier
                user_data_credit.append(new_receiver_data)

            # combining both lists appended
            all_user_transactions = user_data_debit + user_data_credit
            # sort the combined list by time
            sorted_transaction_statement = sorted(all_user_transactions,
                                                  key=lambda criteria: criteria['transaction_date_time'])

            # Prepare the table to display the transaction statement
            transaction_statement = PrettyTable()
            transaction_statement.field_names = ['Post Date', 'Value Date', 'Narration', 'Ref No.', 'Debits', 'Credits',
                                                 'Balance']

            # Add rows to the table
            for transaction in sorted_transaction_statement:
                transaction_statement.add_row(
                    [transaction['transaction_date_time'], transaction['transaction_date_time'],
                     transaction['description'], transaction['transaction_id'],
                     transaction['debit_transaction_amount'],
                     transaction['credit_transaction_amount'], transaction['account_balance']])

    def transaction_history(self, start_date: datetime = None, end_date: datetime = None, year: int = None,
                            month: str = None, time_period: bool = False, is_month: bool = False):
        """Method to retrieve the transaction history associated with a specific account or user,
        providing details of past transactions for reference and auditing purposes.

        Parameters
        ----------
        start_date : datetime, optional
            The start date for the transaction history query.
        end_date : datetime, optional
            The end date for the transaction history query.
        year : int, optional
            The year for the transaction history query (used with the month).
        month : str, optional
            The month for the transaction history query (used with the year).
        time_period : bool, optional
            Flag to indicate if a specific time period (start_date to end_date) should be used.
        is_month : bool, optional
            Flag to indicate if the query should be for a specific month.
        """

        # Store the original cursor and switch to a dictionary cursor for this query
        original = self.database.db_cursor
        self.database.db_cursor = self.database.db_connection.cursor(DictCursor)

        if time_period:
            # Query to get transactions where the user is the sender within the specified date range
            user_sender_transaction_query = f"""SELECT transaction_id, transaction_type, transaction_amount,
                   sender_account_number, sender_name, receiver_account_number, receiver_name, description, status,
                   transaction_date_time
                   FROM {self.database.db_tables[2]}
                   WHERE sender_account_number = '{self.account_number}'
                   AND transaction_date_time BETWEEN '{start_date}' AND '{end_date}'
                   """
            sender_data = list(self.database.fetch_data(user_sender_transaction_query))

            # Query to get transactions where the user is the receiver within the specified date range
            user_receiver_transaction_query = f"""SELECT transaction_id, transaction_type, transaction_amount,
                   sender_account_number, sender_name, receiver_account_number, receiver_name, description, status,
                   transaction_date_time
                   FROM {self.database.db_tables[2]}
                   WHERE receiver_account_number = '{self.account_number}'
                   AND transaction_date_time BETWEEN '{start_date}' AND '{end_date}'
                   """
            receiver_data = list(self.database.fetch_data(user_receiver_transaction_query))

            # Combine and sort the transactions
            all_user_transactions = sender_data + receiver_data
            sorted_transaction_history = sorted(all_user_transactions,
                                                key=lambda criteria: criteria['transaction_date_time'])

            # Prepare the table to display the transaction history
            transaction_history_table = PrettyTable()
            transaction_history_table.field_names = ['Transaction ID', 'Transaction Type', 'Transaction Amount',
                                                     'Sender Account Number', 'Sender Name',
                                                     'Receiver Account Number',
                                                     'Receiver Name', 'Description', 'Status', 'Transaction Date']

            # Add rows to the table
            for transaction in sorted_transaction_history:
                transaction_history_table.add_row([transaction['transaction_id'], transaction['transaction_type'],
                                                   transaction['transaction_amount'],
                                                   transaction['sender_account_number'],
                                                   transaction['sender_name'],
                                                   transaction['receiver_account_number'],
                                                   transaction['receiver_name'], transaction['description'],
                                                   transaction['status'], transaction['transaction_date_time']])

        elif is_month:
            (end_day, month_value) = get_month_values(month, year)
            start_date = datetime(year, month_value, 1)
            end_date = datetime(year, month_value, end_day)

            # Query to get transactions where the user is the sender within the specified month
            user_sender_transaction_query = f"""SELECT transaction_id, transaction_type, transaction_amount,
                               sender_account_number, sender_name, receiver_account_number, receiver_name, description,
                               status, transaction_date_time
                               FROM {self.database.db_tables[2]}
                               WHERE sender_account_number = '{self.account_number}'
                               AND transaction_date_time BETWEEN '{start_date}' AND '{end_date}'
                               """
            sender_data = list(self.database.fetch_data(user_sender_transaction_query))

            # Query to get transactions where the user is the receiver within the specified month
            user_receiver_transaction_query = f"""SELECT transaction_id, transaction_type, transaction_amount,
                               sender_account_number, sender_name, receiver_account_number, receiver_name, description, 
                               status, transaction_date_time
                               FROM {self.database.db_tables[2]}
                               WHERE receiver_account_number = '{self.account_number}' 
                               AND transaction_date_time BETWEEN '{start_date}' AND '{end_date}'
                               """
            receiver_data = list(self.database.fetch_data(user_receiver_transaction_query))

            # Combine and sort the transactions
            all_user_transactions = sender_data + receiver_data
            sorted_transaction_history = sorted(all_user_transactions,
                                                key=lambda criteria: criteria['transaction_date_time'])

            # Prepare the table to display the transaction history
            transaction_history_table = PrettyTable()
            transaction_history_table.field_names = ['Transaction ID', 'Transaction Type', 'Transaction Amount',
                                                     'Sender Account Number', 'Sender Name',
                                                     'Receiver Account Number',
                                                     'Receiver Name', 'Description', 'Status', 'Transaction Date']

            # Add rows to the table
            for transaction in sorted_transaction_history:
                transaction_history_table.add_row([transaction['transaction_id'], transaction['transaction_type'],
                                                   transaction['transaction_amount'],
                                                   transaction['sender_account_number'],
                                                   transaction['sender_name'],
                                                   transaction['receiver_account_number'],
                                                   transaction['receiver_name'], transaction['description'],
                                                   transaction['status'], transaction['transaction_date_time']])

        else:
            # Query to get all transactions where the user is the sender
            user_sender_transaction_query = f"""SELECT transaction_id, transaction_type, transaction_amount,
            sender_account_number, sender_name, receiver_account_number, receiver_name, description, status,
            transaction_date_time
            FROM {self.database.db_tables[2]}
            WHERE sender_account_number = '{self.account_number}'
            """
            sender_data = list(self.database.fetch_data(user_sender_transaction_query))

            # Query to get all transactions where the user is the receiver
            user_receiver_transaction_query = f"""SELECT transaction_id, transaction_type, transaction_amount,
            sender_account_number, sender_name, receiver_account_number, receiver_name, description, status,
            transaction_date_time
            FROM {self.database.db_tables[2]}
            WHERE receiver_account_number = '{self.account_number}'
            """
            receiver_data = list(self.database.fetch_data(user_receiver_transaction_query))

            # Combine and sort the transactions
            all_user_transactions = sender_data + receiver_data
            sorted_transaction_history = sorted(all_user_transactions,
                                                key=lambda criteria: criteria['transaction_date_time'])

            # Prepare the table to display the transaction history
            transaction_history_table = PrettyTable()
            transaction_history_table.field_names = ['Transaction ID', 'Transaction Type', 'Transaction Amount',
                                                     'Sender Account Number', 'Sender Name',
                                                     'Receiver Account Number',
                                                     'Receiver Name', 'Description', 'Status', 'Transaction Date']

            # Add rows to the table
            for transaction in sorted_transaction_history:
                transaction_history_table.add_row([transaction['transaction_id'], transaction['transaction_type'],
                                                   transaction['transaction_amount'],
                                                   transaction['sender_account_number'],
                                                   transaction['sender_name'],
                                                   transaction['receiver_account_number'],
                                                   transaction['receiver_name'], transaction['description'],
                                                   transaction['status'], transaction['transaction_date_time']])

        # Print the transaction history table
        print(transaction_history_table)

        # Restore the original database cursor
        self.database.db_cursor = original
        del original

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
                    self.transfer_limit = float(transfer_limit)

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

        elif self.amount <= 50000:
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
