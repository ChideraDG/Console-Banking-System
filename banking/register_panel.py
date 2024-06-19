import datetime as dt
import re
import time
import random
from bank_processes.bvn import BVN
from bank_processes.notification import Notification
from bank_processes.user import User
from bank_processes.account import Account
from bank_processes.authentication import verify_data
from banking.script import header, go_back, log_error
from animation.colors import *

user = User()
bvn = BVN()
account = Account()
notify = Notification()
    
    
def countdown_timer(_register, _duty: str = 'creation', countdown: int = 3):
    """Countdown for any bank process.
    It enhances users' experience.

    Parameters
    ----------
    _register : str
        A variable that holds some identifier or name related to the process being executed.
    _duty : str
        A variable that holds the task or duty related to the process being executed.
    countdown : int
        A variable that starts with a certain value
        and is decremented until it reaches 0. Represents the time remaining.
    """

    print()
    while countdown != 0:
        print(bold, brt_black_bg, brt_blue, end='')  # coloring
        print(f"processing {_register} {_duty}... {countdown}", end='')
        print(end, end='')  # coloring

        countdown -= 1
        time.sleep(1)

        # Move the cursor to the beginning of the line without adding a new line
        print(end='\r')


def first_name() -> str:
    """To prompt the user to input their first name,
    ensure the input is valid, and return the name formatted in title case.

    Returns
    -------
    str:
        A string representing the user's first name in title case.

    """
    while True:
        print(bold, brt_yellow, "\nInput your First Name:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~", end, sep='')

        print(bold, brt_yellow, end='')
        name = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', name, re.IGNORECASE):
            del name
            go_back('script')
        else:
            if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
                name = match.group(1) + match.group(2)

            if re.search('^[a-z-]+$', name, re.IGNORECASE):
                break
            else:
                print(red, "\n:: Names should be in letters only.\nExample: James, Mary, etc.", end, sep='')
                time.sleep(2)
                continue

    return name.title()


def middle_name() -> str:
    """Gets the middle name of the User.

    Returns
    --------
    str:
        Middle name of the User

    """
    while True:
        print(bold, brt_yellow, "\nInput your Middle Name:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~", end, sep='')

        print(bold, brt_yellow, end='')
        name = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', name, re.IGNORECASE):
            del name
            go_back('script')
        else:
            if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
                name = match.group(1) + match.group(2)

            if re.search('[a-z-]+', name, re.IGNORECASE):
                break
            else:
                print(red, "\n:: Names should be in letters only.\nExample: James, Mary, etc.", end, sep='')
                time.sleep(2)
                continue

    return name.title()


def last_name() -> str:
    """Gets the last name of the User."""
    while True:
        print(bold, brt_yellow, "\nInput your Last Name:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~", end, sep='')

        print(bold, brt_yellow, end='')
        name = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', name, re.IGNORECASE):
            del name
            go_back('script')
        else:
            if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
                name = match.group(1) + match.group(2)

            if re.search('[a-z-]+', name, re.IGNORECASE):
                break
            else:
                print(red, "\n:: Names should be in letters only.\nExample: James, Mary, etc.", end, sep='')
                time.sleep(2)
                continue

    return name.title()


def gender() -> str:
    """Gets the gender of the User."""
    while True:
        print(bold, brt_yellow, "\nInput your Gender:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~", end, sep='')

        print(bold, brt_yellow, end='')
        _gender = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', _gender, re.IGNORECASE):
            del _gender
            go_back('script')
        else:
            if not re.search('^(male|female)$', _gender, re.IGNORECASE):
                print(red, "\n:: Gender should be either Male or Female only.", end, sep='')
                time.sleep(2)
                continue
            else:
                break

    return _gender.title()


def address() -> str:
    """Gets the address of the User."""
    print(bold, brt_yellow, "\nInput your Address:", end, sep='')
    print(bold, magenta, "~~~~~~~~~~~~~~~~~~~", end, sep='')

    print(bold, brt_yellow, end='')
    _address = input(">>> ").strip()
    print(end, end='')

    if re.search('^.*(back|return).*$', _address, re.IGNORECASE):
        del _address
        go_back('script')
    else:
        return _address.title()


def date_of_birth() -> str:
    """Gets the date of birth of the User."""
    max_year = 2006
    month = 12
    month_name = 'December'
    days = 21

    while True:
        print(bold, brt_yellow, "\nInput your Year of Birth:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~", end, sep='')

        print(bold, brt_yellow, end='')
        year_of_birth = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', year_of_birth, re.IGNORECASE):
            del year_of_birth
            go_back('script')
        else:
            if year_of_birth.isdigit() and 1900 < int(year_of_birth) <= max_year:
                break
            else:
                if year_of_birth.isdigit():
                    if not int(year_of_birth) <= max_year:
                        print(red, "\n:: Age is less than 18", end, sep='')
                    elif not 1900 < int(year_of_birth):
                        print(red, "\n:: Year is less than 1900", end, sep='')
                else:
                    print(red, "\n:: Year of Birth should be in digits.\nExample: 2001, 2004, etc.", end, sep='')
                time.sleep(2)
                continue

    time.sleep(1)

    while True:
        print(bold, brt_yellow, "\nInput your Month of Birth:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~", end, sep='')

        print(bold, brt_yellow, end='')
        month_of_birth = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', month_of_birth, re.IGNORECASE):
            del month_of_birth
            go_back('script')
        else:
            if month_of_birth.isdigit() and 0 < int(month_of_birth) <= month:
                break
            else:
                if month_of_birth.isdigit():
                    if not 0 < int(month_of_birth) <= 12:
                        print(red, "\n:: Month of Birth should be between Zero(0) and Twelve(12)", end, sep='')
                else:
                    print(red, "\n:: Month of Birth should be in digits.\nExample: 2 means February, "
                               "4 means April, etc.", end, sep='')
                time.sleep(2)
                continue

    month = int(month_of_birth)
    if month == 1:
        month_name = 'January'
        days = 31
    elif month == 2:
        month_name = 'February'
        if (max_year % 4 == 0 and max_year % 100 != 0) or (max_year % 400 == 0):
            days = 29
        else:
            days = 28
    elif month == 3:
        month_name = 'March'
        days = 31
    elif month == 4:
        month_name = 'April'
        days = 30
    elif month == 5:
        month_name = 'May'
        days = 31
    elif month == 6:
        month_name = 'June'
        days = 30
    elif month == 7:
        month_name = 'July'
        days = 31
    elif month == 8:
        month_name = 'August'
        days = 30
    elif month == 9:
        month_name = 'September'
        days = 30
    elif month == 10:
        month_name = 'October'
        days = 31
    elif month == 11:
        month_name = 'November'
        days = 30
    elif month == 12:
        month_name = 'December'
        days = 31

    time.sleep(1)

    while True:
        print(bold, brt_yellow, "\nInput your Day of Birth:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~", end, sep='')

        print(bold, brt_yellow, end='')
        day_of_birth = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', day_of_birth, re.IGNORECASE):
            del day_of_birth
            go_back('script')
        else:
            if day_of_birth.isdigit() and 0 < int(day_of_birth) <= days:
                break
            else:
                if day_of_birth.isdigit():
                    if not 0 < int(day_of_birth) <= days:
                        print(red, f"\n:: Day of Birth should be within the number of days in {month_name}", end,sep='')
                else:
                    print(red, "\n:: Day of Birth should be in digits.\nExample: 2, 4, 10, etc.", end, sep='')
                time.sleep(2)
                continue

    return f'{year_of_birth}-{month_of_birth}-{day_of_birth}'


def e_mail() -> str:
    """Gets the E-mail of the User."""
    while True:
        print(bold, brt_yellow, "\nInput your E-mail:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~", end, sep='')

        print(bold, brt_yellow, end='')
        email = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', email, re.IGNORECASE):
            del email
            go_back('script')
        else:
            if verify_data('email', 0, email):
                print(red, "\n:: Email already exist", end, sep='')
                time.sleep(2)
                continue

            if re.search(r"^\w+@(\w+\.)?\w+\.(edu|com|gov|ng|org)$", email, re.IGNORECASE):
                break
            else:
                print(red, "\n:: Invalid Email.\nExample: himates@gamil.com, markjames@yahoo.com etc.", end, sep='')
                time.sleep(2)
                continue

    return email.lower()


def phone_number() -> str:
    """Gets the phone number of the User."""
    while True:
        print(bold, brt_yellow, "\nInput your Phone Number:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~", end, sep='')

        print(bold, brt_yellow, end='')
        phoneNumber = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', phoneNumber, re.IGNORECASE):
            del phoneNumber
            go_back('script')
        else:
            if verify_data('phone_number', 0, phoneNumber):
                print(red, "\n:: Phone Number already exist", end, sep='')
                time.sleep(3)
                continue

            if re.search(r'^\+?[0-9]{3} ?[0-9-]{8,11}$', phoneNumber) and 11 <= len(phoneNumber) <= 15:
                break
            else:
                print(red, "\n:: Phone Number should be in digits  only.\nExample: "
                           "08076542879, +2348033327493 etc.", end, sep='')
                time.sleep(2)
                continue

    return phoneNumber


def account_type() -> str:
    """Gets the account type of the User."""
    while True:
        print(bold, brt_yellow, "\nWhat is your desired Account Type:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", end, sep='')
        print(bold, brt_yellow, '1 -> Savings \n2 -> Current', end, sep='')

        print(bold, brt_yellow, end='')
        accountType = input('>>> ')
        print(end, end='')

        if re.search('^.*(back|return).*$', accountType, re.IGNORECASE):
            del accountType
            go_back('script')
        else:
            if re.search('^(1|Savings)$', accountType, re.IGNORECASE):
                accountType = 'Savings'
                break
            elif re.search('^(2|Current)$', accountType, re.IGNORECASE):
                accountType = 'Current'
                break
            else:
                print(red, "\n:: Choose between Savings or Current", end, sep='')
                time.sleep(2)
                continue

    return accountType.lower()


def account_password() -> str:
    """Gets the account password of the User."""
    while True:
        print(bold, brt_yellow, "\nEnter a new Bank Application Password:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", end, sep='')
        print(bold, brt_yellow, "\nEnter Password:", end, sep='')

        print(bold, brt_yellow, end='')
        accountPassword = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', accountPassword, re.IGNORECASE):
            del accountPassword
            go_back('script')
        else:
            if re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$. #!%*?&])[A-Za-z\d@$!#% *?.&]{8,}$", accountPassword):
                while True:
                    print(bold, brt_yellow, "\nRe-enter Password:", end, sep='')

                    print(bold, brt_yellow, end='')
                    second_input = input(">>> ").strip()
                    print(end, end='')

                    if accountPassword == second_input:
                        break
                    else:
                        print(red, "\n:: Passwords are not the same", end, sep='')
                        time.sleep(2)
                        continue
                break
            else:
                print(red, "\n:: Password must be more than 8 characters.", end, sep='')
                print(red, ":: Password should contain a number, a lowercase letter, and uppercase letter and a symbol.", end, sep='')
                time.sleep(2)
                continue

    return accountPassword


def transaction_pin():
    """Gets the transaction pin of the User."""
    while True:
        print(bold, brt_yellow, "\nEnter your new Transaction Pin: (A Four-digit Number)", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "~"*len(' (A Four-digit Number)'), end, sep="")
        print(bold, brt_yellow, "\nEnter Transaction Pin:", end, sep='')

        print(bold, brt_yellow, end='')
        transactionPin = input(">>> ").strip()
        print(end, end='')

        if re.search('^.*(back|return).*$', transactionPin, re.IGNORECASE):
            del transactionPin
            go_back('script')
        else:
            if re.search(r"^\d{4}$", transactionPin):
                while True:
                    print(bold, brt_yellow, "\nRe-Enter Transaction Pin:", end, sep='')

                    print(bold, brt_yellow, end='')
                    second_input = input(">>> ").strip()
                    print(end, end='')

                    if transactionPin == second_input:
                        break
                    else:
                        print(red, "\n:: Passwords are not the same", end, sep='')
                        time.sleep(2)
                        continue
                break
            else:
                print(red, "\n:: Transaction Pin must be only 4 digits.", end, sep='')
                time.sleep(2)
                continue

    return transactionPin


def register_bvn_account():
    """
    Registration form for creating a Bank Verification Number (BVN) and a bank account.

    Notes
    -----
    This function guides the user through the process of creating a BVN first, followed by creating a bank account.
    The BVN form collects personal details such as name, gender, address, date of birth, email, and phone number.
    After successfully creating the BVN, the function proceeds to create a bank account, where it sets up account
    details like account type, balance, minimum balance, fees, and limits. The user is also prompted to create a
    password and a transaction PIN. Finally, the function confirms the successful creation of both the BVN and the
    bank account, displaying the relevant details to the user.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the main script.
    """

    header()
    print(f'{brt_blue}\nMessage from the CUSTOMER SERVICE OFFICER:::{end}')
    print(f'{magenta}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{end}')
    print(f"{brt_blue}'You will need to Create your BVN first, then Create your Bank Account'.{end}")
    time.sleep(3)

    # BVN Form
    try:
        header()

        print(bold, brt_yellow, f"\nBank Verification Number Creation".upper(), end, sep='')
        print(f"{magenta}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{end}")

        print(f"{bold}{red}\nInstruction: Carefully fill in your details{end}")
        print(f"{bold}{magenta}==========================================={end}")

        time.sleep(1)

        bvn.first_name = first_name().title()

        time.sleep(1)

        bvn.middle_name = middle_name().title()

        time.sleep(1)

        bvn.last_name = last_name().title()

        time.sleep(1)

        bvn.gender = gender().title()

        time.sleep(1)

        bvn.address = address().title()

        time.sleep(1)

        bvn.date_of_birth = date_of_birth()

        time.sleep(1)

        bvn.email = e_mail().lower()

        time.sleep(1)

        bvn.phone_number = phone_number()

        bvn.bvn_number = str(random.randint(100000000000, 999999999999))
        while verify_data('bvn_number', 0, bvn.bvn_number):
            bvn.bvn_number = str(random.randint(100000000000, 999999999999))

        bvn.created_date = dt.datetime.now()

        bvn.bvn_status = 'active'

        bvn.last_updated = dt.datetime.now()

        bvn.register_bvn()

        countdown_timer('BVN')
        time.sleep(1)
        header()

        print(bold, brt_yellow, f"\nBank Verification Number Successfully Created.", end, sep='')
        print(f"{bold}{magenta}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{end}")
        print(f"{bold}{brt_black_bg}{brt_yellow}\nUser: {bvn.last_name} {bvn.first_name} {bvn.middle_name}{end}")
        print(f"{bold}{brt_black_bg}{brt_yellow}BVN NUMBER: {bvn.bvn_number}{end}")

        notify.bvn_creation_notification(
            title='Console Beta Banking',
            message=f"{bvn.last_name} {bvn.first_name} {bvn.middle_name} \nBVN NUMBER: {bvn.bvn_number}",
            channel='Console_Beta_BVN'
        )
    except Exception as e:
        log_error(e)

    time.sleep(5)

    # Bank Account Form
    try:
        header()

        print(bold, brt_yellow, f"\nBank Account Details Creation".upper(), end, sep='')
        print(f"{magenta}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{end}")

        print(f"{bold}{red}\nInstruction: Carefully fill in your details{end}")
        print(f"{bold}{magenta}=========================================={end}")

        time.sleep(1)

        # Account Section
        account.account_type = account_type()

        account.account_balance = 0.0
        account.minimum_balance = 0.0
        account.account_fee = 0.0
        account.transaction_limit = 0
        account.transfer_limit = 0.0
        account.maximum_balance = 0.0

        if account.account_type.lower() == 'savings':
            account.account_balance = 500.50
            account.minimum_balance = 50.0
            account.account_fee = 100.0
            account.transaction_limit = 10
            account.transfer_limit = 50000
            account.maximum_balance = 300000
        elif account.account_type.lower() == 'current':
            account.account_balance = 5000.50
            account.minimum_balance = 500.0
            account.account_fee = 500.0
            account.transaction_limit = 50
            account.transfer_limit = 500000
            account.maximum_balance = 3000000

        time.sleep(1)

        user.password = account_password()

        time.sleep(1)

        account.transaction_pin = transaction_pin()

        time.sleep(1)

        account.account_holder = f'{bvn.last_name} {bvn.first_name} {bvn.middle_name}'
        account.account_status = 'active'
        account.overdraft_protection = 'No'
        account.account_tier = 'Tier 1'

        account.account_number = str(random.randint(1000000000, 9999999999))
        while verify_data('account_number', 3, account.account_number):
            account.account_number = str(random.randint(100000000000, 999999999999))

        account.open_account()

        # User Section
        user.first_name = bvn.first_name
        user.middle_name = bvn.middle_name
        user.last_name = bvn.last_name
        user.gender = bvn.gender
        user.email = bvn.email
        user.phone_number = bvn.phone_number
        user.address = bvn.address
        user.date_of_birth = bvn.date_of_birth
        user.linked_accounts = []
        user.last_login_timestamp = dt.datetime.now()
        user.account_open_date = dt.datetime.now()

        user.username = user.first_name.upper() + user.middle_name.upper()
        while verify_data('username', 1, user.username):
            user.username = user.first_name.upper() + user.middle_name.upper() + str(random.randint(1, 1000))

        if '-' in user.username:
            username_list = list(user.username)
            del username_list[username_list.index('-')]
            user.username = ''.join(username_list)
            del username_list

        user.register()

        countdown_timer('Bank Account')
        time.sleep(1)
        header()

        print(f"{bold}{brt_yellow}\nBank Account Successfully Created.{end}")
        print(f"{magenta}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{end}")
        print(f"{bold}{brt_black_bg}{brt_yellow}\nUSERNAME: {user.username}{end}")
        print(f"{bold}{brt_black_bg}{brt_yellow}ACCOUNT NUMBER: {account.account_number}{end}")

        notify.account_creation_notification(
            title='Console Beta Banking',
            message=f"USERNAME: {user.username} \nACCOUNT NUMBER: {account.account_number}",
            channel='Account_Creation'
        )
    except Exception as e:
        log_error(e)
        go_back('script')
