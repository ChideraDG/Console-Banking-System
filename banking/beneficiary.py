import time
from animation.colors import *
from bank_processes.authentication import Authentication
from banking.main_menu import log_error, go_back, header


def beneficiaries(auth: Authentication):
    try:
        header()

        beneficiary = auth.beneficiaries

        while True:
            print(end='\n')
            if beneficiary:
                header()
                print(bold, brt_yellow, '\nBENEFICIARIES', end, sep='')
                print(bold, magenta, '~~~~~~~~~~~~~', end, sep='', end='\n\n')

                # Display the list of beneficiaries
                for number, name in beneficiary.items():
                    print(bold, red, f'{number} - {name[0]} : {name[1].upper()}', end, sep='')
                    print(bold, magenta, '    ~~~', "~" * (len(name[0]) + len(name[1])), sep='')

                input("\nTO RETURN -+- PRESS ENTER  ",)  # Prompt the user to press Enter to return.
                print(end)

                break
            else:
                print(red, '\n' + ':: You have NO Beneficiaries', end)
                time.sleep(3)

                break
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)
