import time
from animation.colors import *
from bank_processes.authentication import Authentication
from banking.script import log_error, go_back, header


def beneficiaries(auth: Authentication):
    try:
        header()

        beneficiary = auth.beneficiaries

        while True:
            print(end='\n')
            if beneficiary:
                header()
                print('\n')

                # Display the list of beneficiaries
                for account_number, account_name in beneficiary.items():
                    print(f'{account_number} - {account_name[0]} : {account_name[1].upper()}')
                    print('    ~~~', "~" * (len(account_name[0]) + len(account_name[1])), sep='')

                input("\nTO RETURN -+- PRESS ENTER  ")  # Prompt the user to press Enter to return.
                break
            else:
                print(red, '\n' + ':: You have NO Beneficiaries', end)
                time.sleep(3)
                break
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)
