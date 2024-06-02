import re
import time
from bank_processes.authentication import Authentication
from banking.register_panel import countdown_timer
from banking.script import go_back, header
from banking.transfer_money import session_token, transaction_pin


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

            print('\nAMOUNT TO BE WITHDRAWN: (more than N10.0)')
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
                        auth.description = f'WTD/CBB/WITHDRAWN FROM {auth.account_holder}'
                        transaction_pin(auth)
                        session_token(auth)

                        header()
                        countdown_timer(_register='\rProcessing Withdrawal', _duty='', countdown=5)
                        auth.process_transaction(withdrawal=True)
                        auth.transaction_record(withdrawal=True)
                        # receipt and notification missing

                        header()
                        print("\n:: Withdraw Successfully")
                        print(f":: You withdraw N{auth.amount}")
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
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: deposit_money.py \nFunction: deposit \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')
