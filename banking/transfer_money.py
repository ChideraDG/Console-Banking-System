import os
import re
import sys
import time
from typing import Any
from bank_processes.authentication import Authentication, verify_data
from banking.register_panel import countdown_timer
from banking.script import header, go_back


def log_error(error: Exception):
    """Logs errors to a file."""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    with open('notification/error.txt', 'w') as file:
        file.write(f'{exc_type}, \n{os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]}, \n{exc_tb.tb_lineno}, '
                   f'\nError: {repr(error)}')
    print(f'\nError: {repr(error)}')
    time.sleep(3)
    
    
def beneficiaries(auth: Authentication, checking_beneficiary: bool = False) -> Any | None:
    """
    Retrieves the list of beneficiaries or checks if a specific beneficiary exists.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user information.
    checking_beneficiary : bool, optional
        Flag to indicate if the function should check for an existing beneficiary (default is False).

    Returns
    -------
    Any or None
        Returns True if the beneficiary exists when checking_beneficiary is True,
        otherwise returns None or the selected beneficiary.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the signed-in menu.

    Notes
    -----
    The function performs two main tasks:
    1. If checking_beneficiary is True, it checks if the specified beneficiary exists in the user's beneficiary list.
    2. If checking_beneficiary is False, it displays the list of beneficiaries and allows the user to select one.
    """
    try:
        beneficiary = auth.beneficiaries

        if checking_beneficiary:
            # Check if the beneficiary exists
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

                    # Display the list of beneficiaries
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
                    elif re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                        del _input
                        time.sleep(1.5)
                        go_back('signed_in', auth=auth)
                    else:
                        continue
                else:
                    return None
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def recipient_account_number(auth: Authentication):
    """
    Prompts the user to enter the recipient's account number and validates it.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user information.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the signed-in menu.

    Notes
    -----
    This function performs the following tasks:
    1. Prompts the user to enter the recipient's account number.
    2. Validates the entered account number.
    3. Confirms the recipient's name with the user.
    4. Sets the recipient's account number and name in the authentication object.
    """
    try:
        while True:
            header()
            print(end='\n')
            print("\nENTER YOUR RECIPIENT ACCOUNT NUMBER:")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            _input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
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
                    checking_input = input(">>> ").strip()

                    if checking_input == '1' or checking_input.lower() == 'yes':
                        del checking_input
                        auth.receiver_acct_num = _input
                        auth.receiver_name = recipient_name

                        break
                    elif re.search('^.*(back|return).*$', _input, re.IGNORECASE):
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
                    print("\n:: Account Number cannot be your own Account Number")
                    del _input
                    time.sleep(3)
                    continue
            else:
                print("\n:: Account Number not Found")
                del _input
                time.sleep(2)
                continue
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def amount_to_be_transferred(auth: Authentication):
    """
    Prompts the user to enter the amount to be transferred and validates it.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user information.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the signed-in menu.

    Notes
    -----
    This function performs the following tasks:
    1. Prompts the user to enter the amount to be transferred.
    2. Validates the entered amount.
    3. Confirms the transaction charges with the user.
    4. Set the amount in the authentication object if the user confirms.
    """
    try:
        while True:
            header()
            print(end='\n')
            print("\nENTER AMOUNT:")
            print("~~~~~~~~~~~~~")
            _input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            else:
                if re.search("^[0-9]$", _input):
                    print("\n:: Amount MUST be above N10")
                    del _input
                    time.sleep(3)
                    continue
                elif re.search("^[0-9]{0,30}[.]?[0-9]{0,2}$", _input, re.IGNORECASE) is None:
                    print("\n:: Digits Only")
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
                            checking_input = input(">>> ").strip()

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
                        time.sleep(2)
                        go_back('signed_in', auth=auth)
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def description(auth):
    """
    Prompts the user to enter a narration for the transaction.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user information.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the signed-in menu.

    Notes
    -----
    This function prompts the user to enter a narration for the transaction. The narration typically describes the purpose
    or details of the transaction. It then assigns the narration to the authentication object.
    """
    try:
        header()
        print(end='\n')
        print("\nENTER NARRATION:")
        print("~~~~~~~~~~~~~~~~~~")
        _input = input(">>> ").strip()

        if re.search('^.*(back|return).*$', _input.lower(), re.IGNORECASE):
            del _input
            time.sleep(1.5)
            go_back('signed_in', auth=auth)
        else:
            # auth.description = _input
            pass
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def transaction_pin(auth: Authentication):
    """
    Prompts the user to enter the transaction PIN for authentication.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user information.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the signed-in menu.

    Notes
    -----
    This function prompts the user to enter the transaction PIN for authentication.
    It allows a maximum of 3 attempts to enter the correct PIN. If the correct PIN is
    not entered within 3 attempts, the account is blocked, and the user is prompted
    to reset their PIN.
    """
    try:
        while auth.login_attempts < 3:
            header()
            print("\nENTER TRANSACTION PIN:")
            print("~~~~~~~~~~~~~~~~~~~~~~")
            _input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', _input.lower(), re.IGNORECASE):
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
        log_error(e)
        go_back('signed_in', auth=auth)


def session_token(auth: Authentication):
    """
    Prompts the user to enter the session token for authentication.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user information.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the signed-in menu.

    Notes
    -----
    This function prompts the user to enter the session token for authentication.
    It allows a maximum of 3 attempts to enter the correct token. If the correct
    token is not entered within 3 attempts, the account is blocked, and the user
    is prompted to reset their pin. The user can also choose to skip this step
    by entering 'skip'.
    """
    try:
        while auth.login_attempts < 3:
            header()
            print("\nENTER SESSION TOKEN:")
            print("~~~~~~~~~~~~~~~~~~~~")
            _input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', _input.lower(), re.IGNORECASE):
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
        log_error(e)
        go_back('signed_in', auth=auth)


def receipt(auth: Authentication):
    while True:
        header()

        print(end='\n')

        auth.transaction_receipts(auth.session_token)

        print('\nDo you want to save the receipt?')
        print('1. Yes  |  2. No')
        print('~~~~~~     ~~~~~')
        user_input = input(">>> ").strip()

        if re.search('^.*(back|return).*$', user_input.lower(), re.IGNORECASE):
            break
        elif re.search('^(1|yes)$', user_input.lower()):
            with open('notification/receipt', 'w') as file:
                file.write(auth.transaction_receipts(auth.session_token))

            print('Receipt Saved Successfully')
            time.sleep(2)
            break
        elif re.search('^(2|no)$', user_input.lower()):
            break
        else:
            continue


def process_transfer(auth: Authentication):
    """
    Handles the process of transferring money either to a bank account or to a beneficiary.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user information and methods for transaction processing.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the signed-in menu.

    Notes
    -----
    This function prompts the user to choose whether to transfer money to a bank account or a beneficiary.
    It then follows a series of steps to complete the transaction, including entering the recipient's account
    number, the amount to be transferred, a description, and validating the transaction with a PIN and session
    token.
    If the transaction is successful, the user is given the option to add the recipient to their
    list of beneficiaries.
    If the daily transaction limit is exceeded, the function exits and prompts the
    user to try again the next day.
    """
    try:
        if auth.transaction_limit > 0:
            while True:
                header()

                print(end='\n')
                print("+~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")
                print("|  1. to BANK  |  2. to BENEFICIARY  |")
                print("+~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")
                user_input = input(">>> ").strip()

                if re.search('^1$', user_input):
                    recipient_account_number(auth)
                    amount_to_be_transferred(auth)
                    description(auth)
                    auth.transaction_type = 'transfer'
                    auth.description = f'TRF/CBB/FROM {auth.account_holder.upper()} TO {auth.receiver_name.upper()}'
                    transaction_pin(auth)
                    session_token(auth)
                    auth.process_transaction(transfer=True)

                    header()
                    countdown_timer(_register='\rProcessing Transaction', _duty='', countdown=5)
                    auth.transaction_record(transfer=True)
                    auth.receiver_transaction_validation()
                    # TODO:
                    #  notification missing
                    #  receipt

                    header()
                    print("\n:: Money Sent Successfully")
                    print(f":: You sent N{auth.amount} to {auth.receiver_name.upper()}")

                    if beneficiaries(auth, checking_beneficiary=True) is False:
                        print(f'\nAdd {auth.receiver_name.upper()} to beneficiaries')
                        print('1. Yes  |  2. No')
                        print('~~~~~~     ~~~~~')
                        checking_input = input(">>> ").strip()

                        if checking_input == '1' or checking_input.lower() == 'yes':
                            auth.add_beneficiaries(_account_holder=auth.receiver_name,
                                                   _account_number=auth.receiver_acct_num)

                            print("\n:: Beneficiary Added Successfully")
                        elif re.search('^.*(back|return).*$', checking_input.lower(), re.IGNORECASE):
                            del checking_input
                            time.sleep(1.5)
                            go_back('signed_in', auth=auth)
                        else:
                            del checking_input
                            time.sleep(1)
                            continue

                    receipt(auth)

                    time.sleep(3)
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
                        auth.description = f'TRF/CBB/FROM {auth.account_holder.upper()} TO {auth.receiver_name.upper()}'
                        transaction_pin(auth)
                        session_token(auth)
                        auth.process_transaction(transfer=True)

                        header()
                        countdown_timer(_register='\rProcessing Transaction', _duty='', countdown=5)
                        auth.transaction_record(transfer=True)
                        auth.receiver_transaction_validation()
                        # TODO:
                        #  notification missing
                        #  receipt

                        header()
                        print("\n:: Money Sent Successfully")
                        print(f":: You sent N{auth.amount} to {auth.receiver_name.upper()}")

                        receipt(auth)

                        time.sleep(3)
                        break
                elif re.search('^.*(back|return).*$', user_input.lower(), re.IGNORECASE):
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
        log_error(e)
        go_back('signed_in', auth=auth)
