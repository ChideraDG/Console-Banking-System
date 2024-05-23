import re
import time
from typing import Any
from bank_processes.authentication import Authentication, verify_data
from banking.register_panel import countdown_timer
from banking.script import header, go_back


def beneficiaries(auth: Authentication, checking_beneficiary: bool = False) -> Any | None:
    """To get the list of beneficiaries or Check if a beneficiary already exists."""
    try:
        beneficiary = auth.beneficiaries

        if checking_beneficiary:
            for account_number, account_name in beneficiary.items():
                if [auth.receiver_acct_num, auth.receiver_name] == account_name:
                    return True
            return False
        else:
            while True:
                print(end='\n')
                if beneficiary:
                    header()
                    print('\n')

                    for account_number, account_name in beneficiary.items():
                        print(f'{account_number} - {account_name[0]} : {account_name[1].upper()}')
                        print('    ~~~', "~" * (len(account_name[0]) + len(account_name[1])), sep='')

                    print("\nPick a Beneficiary:")
                    _input = input('>>> ')

                    if _input.isdigit():
                        if int(_input) <= len(beneficiary):
                            for key in beneficiary.keys():
                                if _input == key:
                                    return beneficiary[key]
                    elif _input.lower() == 'go back' or _input.lower() == 'goback':
                        del _input
                        time.sleep(1.5)
                        go_back('signed_in', auth=auth)
                    else:
                        continue
                else:
                    return None
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

            if _input.lower() == 'go back' or _input.lower() == 'goback':
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            elif re.search("^\\D$", _input):
                print("\n:: Digits Only")
                del _input
                time.sleep(2)
                continue
            elif verify_data('account_number', 3, _input):
                if _input != auth.account_number:
                    checking = Authentication()  # New Instance to get the name of the Recipient
                    checking.account_number = _input
                    recipient_name = checking.account_holder
                    print(f'  ::: {recipient_name.upper()} ')
                    print('\nis this the correct RECIPIENT NAME you want to send money to?')
                    print('1. Yes  |  2. No')
                    print('~~~~~~     ~~~~~')
                    checking_input = input(">>> ")

                    if checking_input == '1' or checking_input.lower() == 'yes':
                        del checking_input
                        auth.receiver_acct_num = _input
                        auth.receiver_name = recipient_name
                        break
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

            if re.search('^(goback|go back)$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            else:
                if re.search("^[0-9]$", _input):
                    print("\n:: Amount MUST be above N10")
                    del _input
                    time.sleep(3)
                    continue
                elif re.search("^[a-z]$", _input):
                    print("\n:: No Alphabets")
                    del _input
                    time.sleep(2)
                    continue
                else:
                    auth.amount = float(_input)
                    if auth.transaction_validation(transfer_limit=True)[0]:
                        if auth.transaction_validation(amount=True)[0]:
                            print(f'\nyou will be charged N{auth.charges} for this transfer')
                            print('1. Yes  |  2. No')
                            print('~~~~~~     ~~~~~')
                            checking_input = input(">>> ")

                            if checking_input == '1' or checking_input.lower() == 'yes':
                                break
                            elif checking_input.lower() == 'go back' or checking_input.lower() == 'goback':
                                del checking_input
                                del _input
                                time.sleep(1.5)
                                go_back('signed_in', auth=auth)
                            else:
                                del _input
                                del checking_input
                                time.sleep(1)
                                continue
                        else:
                            print(f"\n:: {auth.transaction_validation(amount=True)[1]}")
                            del _input
                            time.sleep(2)
                            continue
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


def transaction_pin(auth: Authentication):
    try:
        while auth.login_attempts < 3:
            header()
            print(end='\n')
            print("\nENTER TRANSACTION PIN:")
            print("~~~~~~~~~~~~~~~~~~~~~~")
            _input = input(">>> ")

            if re.search('^(goback|go back)$', _input.lower(), re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            elif re.search("^[a-z]$", _input):
                print("\n:: No Alphabets")
                del _input
                time.sleep(2)
                continue
            else:
                if _input == auth.transaction_pin:
                    break
                else:
                    auth.login_attempts = auth.login_attempts + 1
                    if auth.login_attempts == 3:
                        print("\n:: incorrect PIN.")
                        print("Account has being BLOCKED. Reset your pin.")
                        time.sleep(3)
                        del _input
                        auth.block_account()
                        go_back('script')
                    else:
                        print("\n:: incorrect PIN.")
                        print(3 - auth.login_attempts,
                              'attempts remaining.\nAccount will be BLOCKED after exhausting attempts')
                        time.sleep(3)
                        continue
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Module: transfer_money.py \nFunction: transaction_pin \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(5)
        go_back('signed_in', auth=auth)


def session_token(auth: Authentication):
    try:
        while auth.login_attempts < 3:
            header()
            print(end='\n')
            print("\nENTER SESSION TOKEN:")
            print("~~~~~~~~~~~~~~~~~~~~")
            _input = input(">>> ")

            if re.search('^(goback|go back)$', _input.lower(), re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            elif re.search("^[a-z]$", _input):
                print("\n:: No Alphabets")
                del _input
                time.sleep(2)
                continue
            elif _input == 'skip':
                break
            else:
                if _input == auth.session_token:
                    break
                else:
                    auth.login_attempts = auth.login_attempts + 1
                    if auth.login_attempts == 3:
                        print("\n:: incorrect PIN.")
                        print("Account has being BLOCKED. Reset your pin.")
                        time.sleep(3)
                        del _input
                        auth.block_account()
                        go_back('script')
                    else:
                        print("\n:: incorrect PIN.")
                        print(3 - auth.login_attempts,
                              'attempts remaining.\nAccount will be BLOCKED after exhausting attempts')
                        time.sleep(3)
                        continue
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Module: transfer_money.py \nFunction: session_token \nError: {repr(e)}')
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
                    auth.transaction_type = 'transfer'
                    transaction_pin(auth)
                    session_token(auth)
                    auth.process_transaction()

                    header()
                    countdown_timer(_register='\rProcessing Transaction', _duty='', countdown=5)
                    auth.transaction_record()
                    auth.receiver_transaction_validation()
                    # notification missing

                    header()
                    print("\n:: Money Sent Successfully")
                    print(f":: You sent N{auth.amount} to {auth.receiver_name.upper()}")

                    # print("\n:: print Receipt")
                    if beneficiaries(auth, checking_beneficiary=True) is False:
                        print(f'\nAdd {auth.receiver_name.upper()} to beneficiaries')
                        print('1. Yes  |  2. No')
                        print('~~~~~~     ~~~~~')
                        checking_input = input(">>> ")

                        if checking_input == '1' or checking_input.lower() == 'yes':
                            auth.add_beneficiaries(_account_holder=auth.receiver_name,
                                                   _account_number=auth.receiver_acct_num)

                            print("\n:: Beneficiary Added Successfully")
                        elif re.search('^(goback|go back)$', checking_input.lower(), re.IGNORECASE):
                            del checking_input
                            time.sleep(1.5)
                            go_back('signed_in', auth=auth)
                        else:
                            del checking_input
                            time.sleep(1)
                            continue
                    time.sleep(2)
                    break
                elif re.search('^2$', user_input):
                    bene = beneficiaries(auth)
                    if bene is None:
                        print('\n' + ':: You have NO Beneficiaries')
                        time.sleep(3)
                        continue
                    else:
                        auth.receiver_acct_num = bene[0]
                        auth.receiver_name = bene[1]
                        amount_to_be_transferred(auth)
                        description(auth)
                        auth.transaction_type = 'transfer'
                        transaction_pin(auth)
                        session_token(auth)
                        auth.process_transaction()

                        header()
                        countdown_timer(_register='\rProcessing Transaction', _duty='', countdown=5)
                        auth.receiver_transaction_validation()
                        # notification missing
                        # Process Transaction missing
                        # receipt

                        header()
                        print("\n:: Money Sent Successfully")
                        print(f":: You sent N{auth.amount} to {auth.receiver_name.upper()}")
                        time.sleep(2)
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
