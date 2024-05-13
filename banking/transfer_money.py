import json
import re
import time
from bank_processes.authentication import Authentication, verify_data
from banking.script import header, go_back


def beneficiaries(auth: Authentication) -> str | list:
    try:
        while True:
            beneficiary = json.loads(auth.beneficiaries)

            print(end='\n')
            if beneficiary:
                header()
                print('\n')

                for account_number, account_name in beneficiary.items():
                    print(f'{account_number} - {account_name[0]} : {account_name[1]}')
                    print('    ~~~', "~" * (len(account_name[0]) + len(account_name[1])), sep='')

                print("\nPick a Beneficiary:")
                _input = input('>>> ')

                if re.search("^\\D$", _input):
                    print("\n:: Digits Only")
                    del _input
                    time.sleep(2)
                    continue

                if int(_input) <= len(beneficiary):
                    for key in beneficiary.keys():
                        if _input == key:
                            return beneficiary[key]
                else:
                    continue
            else:
                return ':: Empty'
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Error: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('signed_in', auth=auth)


def recipient_account_number(auth: Authentication):
    try:
        while True:
            header()
            print(end='\n')
            print("\nENTER YOUR RECIPIENT ACCOUNT NUMBER:")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            _input = input(">>> ")

            if verify_data('account_number', 3, _input):
                if _input != auth.account_number:
                    checking = Authentication()  # New Instance to get the name of the Recipient
                    checking.account_number = _input
                    recipient_name = checking.account_holder
                    print(f'\n::: {recipient_name} :::')
                    print('\nis this the correct RECIPIENT NAME you want to send money to?')
                    print('1. Yes  |  2. No')
                    print('~~~~~~     ~~~~~')
                    checking_input = input(">>> ")

                    if checking_input == '1' or checking_input.lower() == 'yes':
                        del checking
                        del checking_input
                        return _input
                    else:
                        del checking
                        del _input
                        del checking_input
                        time.sleep(2)
                        continue
                else:
                    print("\n:: Account Number can not be your own Account Number")
                    del _input
                    time.sleep(3)
                    continue
            elif _input.lower() == 'go back' or _input.lower() == 'goback':
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            else:
                print("\n:: Account Number not Found")
                del _input
                time.sleep(2)
                continue
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Error: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('signed_in', auth=auth)


def transferred_amount(auth: Authentication):
    try:
        while True:
            header()
            print(end='\n')
            print("\nENTER AMOUNT:")
            print("~~~~~~~~~~~~~")
            _input = input(">>> ")

            if auth.transaction_validation(transfer_limit=True)[0]:
                if auth.transaction_validation(amount=True)[0]:
                    pass
                else:
                    pass
                pass
            else:
                pass
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Error: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('signed_in', auth=auth)


def process_transfer(auth: Authentication):
    try:
        if auth.transaction_limit > 0:
            while True:
                header()

                print(end='\n')
                print(" ~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~ ")
                print("|  1. to BANK  |  2. to BENEFICIARY  |")
                print(" ~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~ ")
                user_input = input(">>> ")

                if re.search('^1$', user_input):
                    receiver_account_number = recipient_account_number(auth)
                elif re.search('^2$', user_input):
                    bene = beneficiaries(auth)
                    if bene == ':: Empty':
                        print('\n' + bene)
                        time.sleep(3)
                        continue
                    else:
                        print(bene)
                        time.sleep(5)
                        break
                elif re.search('^(goback|go back)$', user_input.lower(), re.IGNORECASE):
                    del user_input
                    time.sleep(1.5)
                    go_back('signed_in', auth=auth)
                else:
                    continue
        else:
            print("\n:: Daily Transaction Limit Exceeded")
            time.sleep(3)
            go_back('signed_in', auth=auth)
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Error: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('signed_in', auth=auth)
    #     auth.transfer()
    # elif auth.account_type == 'current':
    #     auth.transfer()
    # else:
    #     raise TypeError("Account Type doesn't exist")
