import datetime
import re
import time
from typing import Any
from bank_processes.authentication import Authentication, verify_data
from bank_processes.notification import Notification
from banking.register_panel import countdown_timer
from banking.main_menu import header, go_back, log_error
from animation.colors import *


notify = Notification()
    
    
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
                        print(green, f'{account_number} - {account_name[0]} : {account_name[1].upper()}', end, sep='')
                        print(bold, magenta, '    ~~~', "~" * (len(account_name[0]) + len(account_name[1])), end, sep='')

                    print(bold, brt_yellow, "\nPick a Beneficiary:", end, sep='')

                    print(bold, magenta, end='')
                    _input = input('>>> ')
                    print(end, end='')

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

            print(bold, brt_yellow, "\nENTER YOUR RECIPIENT ACCOUNT NUMBER:")
            print(magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", sep='')

            _input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            elif re.search("^\\D$", _input):
                print(red, "\n:: Digits Only", end, sep='')
                del _input
                time.sleep(2)
                continue
            elif verify_data('account_number', 3, _input):
                if _input != auth.account_number:
                    checking = Authentication()  # New Instance to get the name of the Recipient
                    checking.account_number = _input
                    recipient_name = checking.account_holder
                    print(bold, red, f'  :: {recipient_name.upper()} ::', end, sep='')
                    print(bold, brt_yellow, '\nis this the correct RECIPIENT NAME you want to send money to?', sep='')
                    print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')
                    print(f'{bold}{magenta}~~~~~~     ~~~~~')

                    checking_input = input(">>> ").strip()
                    print(end, end='')

                    if checking_input == '1' or checking_input.lower() == 'yes':
                        del checking_input
                        auth.receiver_acct_num = _input
                        auth.receiver_name = recipient_name

                        break
                    elif re.search('^.*(back|return).*$', checking_input, re.IGNORECASE):
                        del checking_input
                        time.sleep(1.5)
                        go_back('signed_in', auth=auth)
                    elif checking_input == '2' or checking_input.lower() == 'no':
                        del checking
                        del _input
                        del checking_input
                        time.sleep(2)
                        continue
                    else:
                        print(red, "\n:: Invalid response. Try Again.", end, sep='')
                        time.sleep(2)
                        continue
                else:
                    print(red, "\n:: Account Number cannot be your own Account Number", end, sep='')
                    del _input
                    time.sleep(3)
                    continue
            else:
                print(red, "\n:: Account Number not Found", end, sep='')
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

            print(bold, brt_yellow, "\nENTER AMOUNT:")
            print(magenta, "~~~~~~~~~~~~~", sep='')

            _input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            else:
                if re.search("^[0-9]$", _input):
                    print(red, "\n:: Amount MUST be above N10", end, sep='')
                    del _input
                    time.sleep(3)
                    continue
                elif re.search("^[0-9]{0,30}[.]?[0-9]{0,2}$", _input, re.IGNORECASE) is None:
                    print(red, "\n:: Digits Only", end, sep='')
                    del _input
                    time.sleep(2)
                    continue
                else:
                    auth.amount = float(_input)
                    if auth.transaction_validation(transfer_limit=True)[0]:
                        if auth.transaction_validation(amount=True)[0]:
                            print(bold, brt_yellow, f'\nyou will be charged N{auth.charges} for this transfer', sep='')
                            print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')
                            print(f'{bold}{magenta}~~~~~~     ~~~~~{end}')

                            print(bold, magenta, end='')
                            checking_input = input(">>> ").strip()
                            print(end, end='')

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
                            print(red, f"\n:: {auth.transaction_validation(amount=True)[1]}", end, sep='')
                            del _input
                            time.sleep(2)
                            continue
                    else:
                        print(red, f"\n:: {auth.transaction_validation(transfer_limit=True)[1]}", end, sep='')
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

        print(bold, brt_yellow, "\nENTER NARRATION:")
        print(magenta, "~~~~~~~~~~~~~~~~", sep='')

        _input = input(">>> ").strip()
        print(end, end='')

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

            print(bold, brt_yellow, "\nENTER TRANSACTION PIN:")
            print(magenta, "~~~~~~~~~~~~~~~~~~~~~~", sep='')

            _input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _input.lower(), re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            elif re.search("^[a-z]$", _input):
                print(red, "\n:: No Alphabets", end, sep='')
                del _input
                time.sleep(2)
                continue
            else:
                if _input == auth.transaction_pin:
                    break
                else:
                    auth.login_attempts = auth.login_attempts + 1
                    if auth.login_attempts == 3:
                        print(red, "\n:: incorrect PIN.")
                        print("Account has being BLOCKED. Reset your pin.", end)
                        time.sleep(3)
                        del _input
                        auth.block_account()
                        go_back('script')
                    else:
                        print(red, "\n:: incorrect PIN.")
                        print(3 - auth.login_attempts,
                              'attempts remaining.\nAccount will be BLOCKED after exhausting attempts', red)
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

            print(bold, brt_yellow, "\nENTER SESSION TOKEN:")
            print(magenta, "~~~~~~~~~~~~~~~~~~~~", sep='')

            _input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _input.lower(), re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
            elif re.search("^[a-z]$", _input):
                print(red, "\n:: No Alphabets", end, sep='')
                del _input
                time.sleep(2)
                continue
            elif _input == '123456':
                break
            else:
                if _input == auth.session_token:
                    break
                else:
                    auth.login_attempts = auth.login_attempts + 1
                    if auth.login_attempts == 3:
                        print(red, "\n:: incorrect SESSION TOKEN.")
                        print("Account has being BLOCKED. Meet Customer Service to Unblock your Account.", end)
                        time.sleep(3)
                        del _input
                        auth.block_account()
                        go_back('script')
                    else:
                        print(red, "\n:: incorrect SESSION TOKEN.")
                        print(3 - auth.login_attempts,
                              'attempts remaining.\nAccount will be BLOCKED after exhausting attempts', end)
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

        print(bold, brt_yellow, '\nDo you want to save the receipt?', sep='')
        print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')
        print(f'{bold}{magenta}~~~~~~     ~~~~~{end}')

        print(bold, magenta, end='')
        user_input = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', user_input.lower(), re.IGNORECASE):
            break
        elif re.search('^(1|yes)$', user_input.lower()):
            with open('notification/receipt', 'w') as file:
                file.write(auth.transaction_receipts(auth.session_token))

            print(green, 'Receipt Saved Successfully', end, sep='')
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
                print(bold, magenta, "+~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+", sep='')
                print(f"|{end}  {bold}{brt_black_bg}{brt_yellow}1. to BANK{end}  {bold}{magenta}|  {bold}{brt_black_bg}{brt_yellow}2. to BENEFICIARY{end}  {bold}{magenta}|")
                print("+~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")

                user_input = input(">>> ").strip()
                print(end, end='')

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

                    note = f"""
Debit
Amount :: NGN{(auth.amount+auth.charges):,.2f}
Acc :: {auth.account_number[:3]}******{auth.account_number[-3:]}
Desc :: {auth.description}
Time :: {datetime.datetime.today().now().time()}
Balance :: {auth.account_balance}
                    """
                    notify.transfer_notification(
                        title='Console Beta Banking',
                        message=note,
                        channel='ConsoleBeta'
                    )

                    header()
                    print(bold, brt_yellow, italic, "\n:: Money Sent Successfully")
                    print(f":: You sent N{auth.amount} to {auth.receiver_name.upper()}", end)

                    if beneficiaries(auth, checking_beneficiary=True) is False:
                        print(bold, brt_yellow, f'\nAdd {auth.receiver_name.upper()} to beneficiaries')
                        print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')
                        print(f'{bold}{magenta}~~~~~~     ~~~~~{end}')

                        print(bold, magenta, end='')
                        checking_input = input(">>> ").strip()
                        print(end, end='')

                        if checking_input == '1' or checking_input.lower() == 'yes':
                            auth.add_beneficiaries(_account_holder=auth.receiver_name,
                                                   _account_number=auth.receiver_acct_num)

                            print(bold, brt_yellow, italic, "\n:: Beneficiary Added Successfully", end)
                            time.sleep(1.5)
                        elif re.search('^.*(back|return).*$', checking_input.lower(), re.IGNORECASE):
                            del checking_input
                            time.sleep(1.5)
                            break
                        else:
                            del checking_input
                            time.sleep(1)
                            continue

                elif re.search('^2$', user_input):
                    bene = beneficiaries(auth)
                    if bene is None:
                        print(red, '\n' + ':: You have NO Beneficiaries', end)
                        time.sleep(3)
                        continue

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

                    note = f"""
Debit
Amount :: NGN{(auth.amount+auth.charges):,.2f}
Acc :: {auth.account_number[:3]}******{auth.account_number[-3:]}
Desc :: {auth.description}
Time :: {datetime.datetime.today().now().time()}
Balance :: {auth.account_balance}
                    """
                    notify.transfer_notification(
                        title='Console Beta Banking',
                        message=note,
                        channel='ConsoleBeta'
                    )

                    header()
                    print(bold, brt_yellow, italic, "\n:: Money Sent Successfully")
                    print(f":: You sent N{auth.amount} to {auth.receiver_name.upper()}", end)
                    time.sleep(1.5)

                elif re.search('^.*(back|return).*$', user_input.lower(), re.IGNORECASE):
                    del user_input
                    time.sleep(1.5)
                    go_back('signed_in', auth=auth)
                else:
                    continue

                time.sleep(1.5)

                receipt(auth)

                time.sleep(1.5)
                break
        else:
            print(red, "\n:: Daily Transaction Limit Exceeded", end)
            time.sleep(3)
            go_back('signed_in', auth=auth)
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)
