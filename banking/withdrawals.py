import re
import time
from bank_processes.authentication import Authentication
from banking.script import go_back, header


def withdraw(auth: Authentication):
    """

    Parameters
    ----------
    auth

    Returns
    -------

    """
    try:
        while True:
            header()

            print('AMOUNT TO BE WITHDRAWN: (more than N10.0)')
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
                auth.amount = float(amount)
                if auth.transaction_validation(transfer_limit=True)[0]:
                    if auth.transaction_validation(amount=True)[0]:
                        auth.narration = f'WTD/CBB/WITHDRAWN FROM {auth.account_holder}'
                    else:
                        print(f"\n:: {auth.transaction_validation(amount=True)[1]}")
                        time.sleep(2)
                        continue
                else:
                    print(f"\n:: {auth.transaction_validation(transfer_limit=True)[1]}")
                    time.sleep(2)
                    break

    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: deposit_money.py \nFunction: deposit \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')
