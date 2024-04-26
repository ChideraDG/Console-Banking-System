import datetime
import random


class Transaction:
    currency = 'Naira'

    def __init__(self, transaction_id: str = None, transaction_type: str = None,
                 amount: float = None, transaction_date_time: datetime.datetime = None, sender_acct: str = None,
                 receiver_acct: str = None,
                 description: str = None, status: str = None, fees: float = None, merchant_info: str = None,
                 transaction_category: str = None, user_id: str = None, account_type: str = None,
                 sender_name: str = None, receiver_name: str = None):
        self.transaction_type = transaction_type
        self.amount = amount
        self.transaction_id = transaction_id  # unique identifier for transaction
        self.transaction_date_time = transaction_date_time  # timestamp for when the transaction occurred
        self.sender_acct = sender_acct  # sender's account details
        self.receiver = receiver_acct  # receiver's account details
        self.description = description  # description of the transaction
        self.status = status  # status of the transaction
        self.fees = fees  # fees associated with the amount
        self.merchant_info = merchant_info  # info about the merchant or receiver
        self.transaction_category = transaction_category  # category of the transfer
        self.user_id = user_id  # identifier of the user who initiated the transaction
        self.account_type = account_type  # whether fixed deposit, savings or current
        self.sender_name = sender_name  # Person in question doing the transaction
        self.receiver_name = receiver_name

    def transaction_record(self):
        """Method to record new transactions made and the relevant information"""
        now = datetime.datetime.now()
        self.transaction_date_time = now.strftime("%d %B %Y %H:%M:%S")
        amt = ''
        detail_type = ''  # whether sender or receiver
        option_transfer = ''  # 'Payment method' in the  case of a debit and 'Credited' for credit
        self.transaction_type = self.transaction_type.upper()
        if self.transaction_type == 'WITHDRAW':
            amt = f'-{self.amount}'
            detail_type = f'''Recipient Details\t\t\t{self.sender_name}
                          \t\t\tBankApp|{self.sender_acct}'''
            option_transfer = f'''Credited to         \t\tBalance'''

        elif self.transaction_type == 'TRANSFER':
            amt = f'-{self.amount}'
            detail_type = f'''Recipient Details\t\t\t{self.sender_name}
                          \t\t\tBankApp|{self.sender_acct}'''
            option_transfer = f'''Credited to         \t\tBalance'''

        elif self.transaction_type == 'DEPOSIT':
            amt = f'+{self.amount}'
            detail_type = f'''Sender Details\t\t\t\t{self.sender_name}
                          \t\t\tBankApp|{self.sender_acct}'''
            option_transfer = f'''Payment Method         \t\tBalance'''

        trans_record = f"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    {amt}
                    {self.status}
        TRANSACTION DETAILS
        Transaction Type\t\t\t{self.transaction_type}
        {detail_type}
        Remark             \t\t\t{self.description}
        {option_transfer}
        Transaction Number   \t\t{random.randint(100000000000000000, 999999999999999999)}
        Transaction Date      \t\t{self.transaction_date_time}
        Transaction ID         \t\t{random.randint(100000000000000000000000000000,
                                                   999999999999999999999999999999)}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
        print(trans_record)

    def retrieve_transaction(self):
        """Method to retrieve a list of transaction based on a certain criteria"""
        pass

    def cal_transaction_fees(self):
        """Method to calculate fees associated with the transfer depending on the amount """
        acct_type = self.account_type.lower().strip()
        if acct_type == 'current':
            self.fees = 50.00
            return self.fees

        elif acct_type == 'savings':
            self.fees = 10.00
            return self.fees

        elif acct_type == 'fixed deposit':
            self.fees = 40.00
            return self.fees

    def transaction_validation(self):
        """Method to validate the transaction, ensuring that it meets any requirements or constraints imposed by
        the bank or regulatory authorities. """
        pass

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


# obj = Transaction(transaction_type='withdraw', sender_name='Ezenwa Chiedozie', description='Food',
#                   sender_acct='12132537437', status='SUCCESS', amount=500.00)
# obj.transaction_record()
