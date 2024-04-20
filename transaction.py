class Transaction:
    currency = 'Naira'

    def __init__(self, transaction_id: str = None, transaction_type: str = None,
                 amount: float = None, date_time: str = None, sender_acct: str = None, receiver_acct: str = None,
                 description: str = None, status: str = None, fees: float = None, merchant_info: str = None,
                 transaction_category: str = None, user_id: str = None,):
        self.transaction_id = transaction_id  # unique identifier for transaction
        self.date_time = date_time  # timestamp for when the transaction occurred
        self.sender_acct = sender_acct  # sender's account details
        self.receiver = receiver_acct   # receiver's account details
        self.description = description  # description of the transaction
        self.status = status    # status of the transaction
        self.fees = fees    # fees associated with the amount
        self.merchant_info = merchant_info  # info about the merchant or receiver
        self.transaction_category = transaction_category    # category of the transfer
        self.user_id = user_id  # identifier of the user who initiated the transaction

    def transaction_record(self):
        """Method to record new transactions made and the relevant information"""
        pass

    def retrieve_transaction(self):
        """Method to retrieve a list of transaction based on a certain criteria"""
        pass

    def cal_transaction_fees(self):
        """Method to calculate fees associated with the transfer depending on the amount """
        pass

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