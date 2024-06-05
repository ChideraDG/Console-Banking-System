import re
import time
import sys
import os
from bank_processes.authentication import Authentication
from banking.register_panel import countdown_timer
from banking.script import go_back, header
from banking.transfer_money import session_token, transaction_pin


def log_error(error: Exception):
    """Logs errors to a file."""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    with open('notification/error.txt', 'w') as file:
        file.write(f'{exc_type}, \n{os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]}, \n{exc_tb.tb_lineno}, '
                   f'\nError: {repr(error)}')
    print(f'\nError: {repr(error)}')
    time.sleep(3)


def withdraw(auth: Authentication):
    """
    Handles the process of withdrawing money from the user's account.

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class that contains user authentication and transaction details.

    Raises
    ------
    Exception:
        If any unexpected error occurs during the withdrawal process.
    """
    try:
        while True:
            header()

            # Prompt the user to enter the amount to be withdrawn
            print('\nAMOUNT TO BE WITHDRAWN: (more than N10.0)')
            print('~~~~~~~~~~~~~~~~~~~~~~~')

            amount = input('>>> ')

            # Check if the user wants to go back to the previous menu
            if re.search('^.*(back|return).*$', amount.strip(), re.IGNORECASE):
                break

            # Ensure the input is a valid number
            elif re.search("^[0-9]{0,30}[.]?[0-9]{0,2}$", amount, re.IGNORECASE) is None:
                print('\n:: Digits Only')
                time.sleep(3)
                continue

            # Check if the amount is greater than 10.0 naira
            elif float(amount) < 10.0:
                print('\n:: Amount must be more than 10.0 naira.')
                time.sleep(3)
                continue

            else:
                auth.amount = float(amount)

                # Validate if the transaction can proceed within the transfer limits
                if auth.transaction_validation(transfer_limit=True)[0]:

                    # Validate if the amount is permissible
                    if auth.transaction_validation(amount=True)[0]:

                        # Set the description for the transaction
                        auth.description = f'WTD/CBB/WITHDRAWN FROM {auth.account_holder}'

                        # Prompt for the transaction PIN
                        transaction_pin(auth)

                        # Prompt for the session token
                        session_token(auth)

                        # Display a processing message and process the transaction
                        header()
                        countdown_timer(_register='\rProcessing Withdrawal', _duty='', countdown=5)
                        auth.process_transaction(withdrawal=True)

                        # Record the transaction
                        auth.transaction_record(withdrawal=True)

                        # TODO: Add receipt generation and notification sending

                        header()
                        print("\n:: Withdraw Successfully")
                        print(f":: You withdrew N{auth.amount}")
                        time.sleep(3)
                        break
                    else:
                        print(f"\n:: {auth.transaction_validation(amount=True)[1]}")
                        time.sleep(2)
                        continue
                else:
                    print(f"\n:: {auth.transaction_validation(transfer_limit=True)[1]}")
                    time.sleep(2)
                    break

    except Exception as e:
        # Log the error to a file and notify the user
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: deposit_money.py \nFunction: withdraw \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')
