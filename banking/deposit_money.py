import re
import time
from bank_processes.authentication import Authentication
from banking.register_panel import countdown_timer
from banking.script import go_back, header
from banking.transfer_money import session_token, transaction_pin


def deposit(auth: Authentication):
    """

    Parameters
    ----------
    auth : Authentication
        Contains the entire details of the User.

    Returns
    -------

    """
    try:
        while True:
            header()

            print('\nAMOUNT TO BE DEPOSITED: (more than N10.0)')
            print('~~~~~~~~~~~~~~~~~~~~~~~')

            amount = input('>>> ')
            if re.search('^.*(back|return).*$', amount.strip(), re.IGNORECASE):
                break
            elif not amount.isdigit():
                print('\n:: Digits Only')
                time.sleep(3)
                continue
            elif float(amount) < 10.0:
                print('\n:: Amount must be more than 10.0 naira.')
                time.sleep(3)
                continue
            else:
                auth.amount = amount
                auth.narration = f'DEP/CBB/DEPOSIT TO {auth.account_holder}'
                transaction_pin(auth)
                session_token(auth)

                header()
                countdown_timer(_register='\rProcessing Deposit', _duty='', countdown=5)
                # auth.process_transaction(deposit=True)
                # auth.transaction_record(deposit=True)
                # receipt and notification missing

                header()
                print("\n:: Deposition Successfully")
                print(f":: You deposited N{auth.amount} into your Beta Account")
                time.sleep(3)
                break

    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: deposit_money.py \nFunction: deposit \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')
