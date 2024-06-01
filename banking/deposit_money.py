import re
import time
from bank_processes.authentication import Authentication
from banking.script import go_back, header


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

    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: deposit_money.py \nFunction: deposit \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')
