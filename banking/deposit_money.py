import re
import time
from datetime import datetime
from bank_processes.authentication import Authentication
from bank_processes.notification import Notification
from banking.register_panel import countdown_timer
from banking.main_menu import go_back, header, log_error
from banking.transfer_money import session_token, transaction_pin, receipt
from animation.colors import *

notify = Notification()


def deposit(auth: Authentication):
    """
    Handles the process of depositing money into the user's account.

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class that contains user authentication and transaction details.

    Raises
    ------
    Exception:
        If any unexpected error occurs during the deposit process.
    """
    try:
        while True:
            header()

            # Prompt the user to enter the amount to be deposited
            print(bold, brt_yellow, '\nAMOUNT TO BE DEPOSITED: (more than N10.0)', end)
            print(magenta, '~~~~~~~~~~~~~~~~~~~~~~~', sep='')

            amount = input('>>> ').strip()
            print(end, end='')

            # Check if the user wants to go back to the previous menu
            if re.search('^.*(back|return).*$', amount, re.IGNORECASE):
                break

            # Ensure the input is a valid number
            elif re.search("^[0-9]{0,30}[.]?[0-9]{0,2}$", amount, re.IGNORECASE) is None:
                print(red, '\n:: Digits Only', end, sep='')
                time.sleep(3)
                continue

            # Check if the amount is greater than 10.0 naira
            elif float(amount) < 10.0:
                print(red, '\n:: Amount must be more than 10.0 naira.', end, sep='')
                time.sleep(3)
                continue

            else:
                auth.receiver_acct_num = auth.account_number

                # Set the amount and narration for the deposit
                auth.amount = float(amount)
                auth.description = f'DEP/CBB/DEPOSIT TO {auth.account_holder}'

                # Prompt for the transaction PIN and session token
                transaction_pin(auth)
                session_token(auth)

                # Display a processing message and process the transaction
                header()
                countdown_timer(_register='\rProcessing Deposit', _duty='', countdown=5)

                # Process and record transaction
                auth.process_transaction(deposit=True)
                auth.transaction_record(deposit=True)
                auth.receiver_transaction_validation()

                # Create a formatted note for the deposit notification
                note = f"""
Credit
Amount :: NGN{auth.amount:,.2f}
Acc :: {auth.account_number[:3]}******{auth.account_number[-3:]}
Desc :: {auth.description}
Time :: {datetime.today().now().time()}
Balance :: {auth.account_balance}
                """

                # Trigger a deposit notification with the formatted note
                notify.deposit_notification(
                    title='Console Beta Banking',
                    message=note,
                    channel='ConsoleBeta'
                )

                header()
                print(green, "\n:: Deposit Successfully")
                print(f":: You deposited N{auth.amount} into your Beta Account", end, sep='')

                time.sleep(1.5)
                break

    except Exception as e:
        # Log the error to a file and notify the user
        log_error(e)
        go_back('signed_in', auth=auth)


def deposit_default(auth: Authentication, _amount: float, _description: str):
    """
    Handles the default deposit process for a given authentication object.

    Parameters
    ----------
    auth : Authentication
        The authentication object representing the user's account.
    _amount : float
        The amount to be deposited into the account.
    _description : str
        The description or narration for the deposit transaction.

    Notes
    -----
    This function sets the deposit amount and description, processes and records the transaction,
    and triggers a notification with the details of the deposit.
    """

    # Set the receiver's account number to the current user's account number
    auth.receiver_acct_num = auth.account_number

    # Set the amount and narration for the deposit
    auth.amount = _amount  # Assign the deposit amount to the authentication object
    auth.description = _description  # Assign the deposit description to the authentication object

    # Process and record the transaction
    auth.process_transaction(deposit=True)  # Process the transaction as a deposit
    auth.transaction_record(deposit=True)  # Record the transaction in the transaction history

    # Create a formatted note for the deposit notification
    note = (f"Credit\nAmount :: NGN{auth.amount:,.2f}\n"
            f"Acc :: {auth.account_number[:3]}******{auth.account_number[-3:]})\n"
            f"Desc :: {auth.description}\nTime :: {datetime.today().now().time()}\nBalance :: {auth.account_balance}")

    # Trigger a deposit notification with the formatted note
    notify.deposit_notification(
        title='Console Beta Banking',  # Set the title of the notification
        message=note,  # Set the message content of the notification
        channel='ConsoleBeta'  # Specify the channel for delivering the notification
    )
