import re
import time
from datetime import datetime
from bank_processes.authentication import Authentication
from bank_processes.notification import Notification
from banking.register_panel import countdown_timer
from banking.script import go_back, header, log_error
from banking.transfer_money import session_token, transaction_pin, receipt


notify = Notification()


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

                        note = f"""
Debit
Amount :: NGN{auth.amount:,.2f}
Acc :: {auth.account_number[:3]}******{auth.account_number[-3:]}
Desc :: {auth.description}
Time :: {datetime.today().now().time()}
Balance :: {auth.account_balance}
                        """

                        # Trigger a withdraw notification with the formatted note
                        notify.withdraw_notification(
                            title='Console Beta Banking',
                            message=note,
                            channel='ConsoleBeta'
                        )
                        # TODO: Add receipt generation and notification sending

                        header()
                        print("\n:: Withdraw Successfully")
                        print(f":: You withdrew N{auth.amount}")

                        time.sleep(1.5)

                        receipt(auth)

                        time.sleep(1.5)
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
        log_error(e)
        go_back('script')
