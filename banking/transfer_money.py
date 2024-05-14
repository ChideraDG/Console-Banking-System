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
            file.write(f'Module: transfer_money.py \nFunction: beneficiaries \nError: {repr(e)}')
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

            if re.search("^\\D$", _input):
                print("\n:: Digits Only")
                del _input
                time.sleep(2)
                continue

            if verify_data('account_number', 3, _input):
                if _input != auth.account_number:
                    checking = Authentication()  # New Instance to get the name of the Recipient
                    checking.account_number = _input
                    recipient_name = checking.account_holder
                    print(f'  R.N. ::: {recipient_name} ')
                    print('\nis this the correct RECIPIENT NAME you want to send money to?')
                    print('1. Yes  |  2. No')
                    print('~~~~~~     ~~~~~')
                    checking_input = input(">>> ")

                    if checking_input == '1' or checking_input.lower() == 'yes':
                        del checking_input
                        auth.receiver_acct_num = _input
                        auth.receiver_name = recipient_name
                    elif _input.lower() == 'go back' or _input.lower() == 'goback':
                        del _input
                        time.sleep(1.5)
                        go_back('signed_in', auth=auth)
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
            file.write(f'Module: transfer_money.py \nFunction: recipient_account_number \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('signed_in', auth=auth)


def amount_to_be_transferred(auth: Authentication):
    try:
        while True:
            header()
            print(end='\n')
            print("\nENTER AMOUNT:")
            print("~~~~~~~~~~~~~")
            _input = input(">>> ")

            if re.search("^[0-9.]$", _input):
                print("\n:: No Alphabets")
                del _input
                time.sleep(2)
                continue

            auth.amount = float(_input)
            if auth.transaction_validation(transfer_limit=True)[0]:
                if auth.transaction_validation(amount=True)[0]:
                    print(f'\nyou will be charged {auth.charges} for this transfer')
                    print('1. Yes  |  2. No')
                    print('~~~~~~     ~~~~~')
                    checking_input = input(">>> ")

                    if checking_input == '1' or checking_input.lower() == 'yes':
                        auth.amount = float(_input)
                    elif _input.lower() == 'go back' or _input.lower() == 'goback':
                        del checking_input
                        del _input
                        time.sleep(1.5)
                        go_back('signed_in', auth=auth)
                    else:
                        del _input
                        del checking_input
                        time.sleep(2)
                        continue
                else:
                    print(f"\n:: {auth.transaction_validation(amount=True)[1]}")
                    del _input
                    time.sleep(2)
                    continue
            elif re.search('^(goback|go back)$', _input.lower(), re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            else:
                print(f"\n:: {auth.transaction_validation(transfer_limit=True)[1]}")
                del _input
                time.sleep(3)
                go_back('signed_in', auth=auth)
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Module: transfer_money.py \nFunction: amount_to_be_transferred \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(5)
        go_back('signed_in', auth=auth)


def description(auth):
    try:
        header()
        print(end='\n')
        print("\nENTER DESCRIPTION:")
        print("~~~~~~~~~~~~~~~~~~")
        _input = input(">>> ")

        if re.search('^(goback|go back)$', _input.lower(), re.IGNORECASE):
            del _input
            time.sleep(1.5)
            go_back('signed_in', auth=auth)
        else:
            auth.description = _input
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Module: transfer_money.py \nFunction: description \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(5)
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
                    recipient_account_number(auth)
                    amount_to_be_transferred(auth)
                    description(auth)
                    time.sleep(10)
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
            file.write(f'Module: transfer_money.py \nFunction: process_transfer \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(5)
        go_back('signed_in', auth=auth)
    #     auth.transfer()
    # elif auth.account_type == 'current':
    #     auth.transfer()
    # else:
    #     raise TypeError("Account Type doesn't exist")
