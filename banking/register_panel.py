import datetime as dt
import re
import time
import random
from bank_processes.bvn import BVN
from bank_processes.user import User
from bank_processes.account import Account
from bank_processes.authentication import verify_data
from banking.script import header, go_back

user = User()
bvn = BVN()
account = Account()


def countdown_timer(_register, _duty: str = 'creation', countdown: int = 3):
    """Countdown for the bank or bvn creation. It enhances users' experience."""
    print()
    while countdown != 0:
        print(f"processing {_register} {_duty}... {countdown}", end='')
        countdown -= 1
        time.sleep(1)
        print(end='\r')


def first_name() -> str:
    """Gets the first name of the User."""
    while True:
        print("\nInput your First Name:")
        print("~~~~~~~~~~~~~~~~~~~~~~")
        name = input(">>> ").strip()

        if re.search('^(goback|go back)$', name, re.IGNORECASE):
            del name
            go_back('script')
        else:
            if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
                name = match.group(1) + match.group(2)

            if re.search('^[a-z-]+$', name, re.IGNORECASE):
                break
            else:
                print("\n:: Names should be in letters only.\nExample: James, Mary, etc.")
                time.sleep(2)
                continue

    return name.title()


def middle_name() -> str:
    """Gets the middle name of the User."""
    while True:
        print("\nInput your Middle Name:")
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        name = input(">>> ").strip()

        if re.search('^(goback|go back)$', name, re.IGNORECASE):
            del name
            go_back('script')
        else:
            if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
                name = match.group(1) + match.group(2)

            if re.search('[a-z-]+', name, re.IGNORECASE):
                break
            else:
                print("\n:: Names should be in letters only.\nExample: James, Mary, etc.")
                time.sleep(2)
                continue

    return name.title()


def last_name() -> str:
    """Gets the last name of the User."""
    while True:
        print("\nInput your Last Name:")
        print("~~~~~~~~~~~~~~~~~~~~~")
        name = input(">>> ").strip()

        if re.search('^(goback|go back)$', name, re.IGNORECASE):
            del name
            go_back('script')
        else:
            if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
                name = match.group(1) + match.group(2)

            if re.search('[a-z-]+', name, re.IGNORECASE):
                break
            else:
                print("\n:: Names should be in letters only.\nExample: James, Mary, etc.")
                time.sleep(2)
                continue

    return name.title()


def gender() -> str:
    """Gets the gender of the User."""
    while True:
        print("\nInput your Gender:")
        print("~~~~~~~~~~~~~~~~~~~~~")
        _gender = input(">>> ").strip()

        if re.search('^(goback|go back)$', _gender, re.IGNORECASE):
            del _gender
            go_back('script')
        else:
            if not re.search('^(male|female)$', _gender, re.IGNORECASE):
                print("\n:: Gender should be either Male or Female only.")
                time.sleep(2)
                continue
            else:
                break

    return _gender.title()


def address() -> str:
    """Gets the address of the User."""
    print("\nInput your Address:")
    print("~~~~~~~~~~~~~~~~~~~")
    _address = input(">>> ").strip()

    if re.search('^(goback|go back)$', _address, re.IGNORECASE):
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
        print("\nInput your Year of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        year_of_birth = input(">>> ").strip()

        if re.search('^(goback|go back)$', year_of_birth, re.IGNORECASE):
            del year_of_birth
            go_back('script')
        else:
            if year_of_birth.isdigit() and 1900 < int(year_of_birth) <= max_year:
                break
            else:
                if year_of_birth.isdigit():
                    if not int(year_of_birth) <= max_year:
                        print("\n:: Age is less than 18")
                    elif not 1900 < int(year_of_birth):
                        print("\n:: Year is less than 1900")
                else:
                    print("\n:: Year of Birth should be in digits.\nExample: 2001, 2004, etc.")
                time.sleep(2)
                continue

    time.sleep(1)

    while True:
        print("\nInput your Month of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        month_of_birth = input(">>> ").strip()

        if re.search('^(goback|go back)$', month_of_birth, re.IGNORECASE):
            del month_of_birth
            go_back('script')
        else:
            if month_of_birth.isdigit() and 0 < int(month_of_birth) <= month:
                break
            else:
                if month_of_birth.isdigit():
                    if not 0 < int(month_of_birth) <= 12:
                        print("\n:: Month of Birth should be between Zero(0) and Twelve(12)")
                else:
                    print("\n:: Month of Birth should be in digits.\nExample: 2 means February, 4 means April, etc.")
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
        print("\nInput your Day of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        day_of_birth = input(">>> ").strip()

        if re.search('^(goback|go back)$', day_of_birth, re.IGNORECASE):
            del day_of_birth
            go_back('script')
        else:
            if day_of_birth.isdigit() and 0 < int(day_of_birth) <= days:
                break
            else:
                if day_of_birth.isdigit():
                    if not 0 < int(day_of_birth) <= days:
                        print(f"\n:: Day of Birth should be within the number of days in {month_name}")
                else:
                    print("\n:: Day of Birth should be in digits.\nExample: 2, 4, 10, etc.")
                time.sleep(2)
                continue

    return f'{year_of_birth}-{month_of_birth}-{day_of_birth}'


def e_mail() -> str:
    """Gets the E-mail of the User."""
    while True:
        print("\nInput your E-mail:")
        print("~~~~~~~~~~~~~~~~~~")
        email = input(">>> ").strip()

        if re.search('^(goback|go back)$', email, re.IGNORECASE):
            del email
            go_back('script')
        else:
            if verify_data('email', 0, email):
                print('\n*ERROR*')
                print("-> Email already exist")
                time.sleep(2)
                continue

            if re.search(r"^\w+@(\w+\.)?\w+\.(edu|com|gov|ng|org)$", email, re.IGNORECASE):
                break
            else:
                print("\n:: Invalid Email.\nExample: himates@gamil.com, markjames@yahoo.com etc.")
                time.sleep(2)
                continue

    return email.lower()


def phone_number() -> str:
    """Gets the phone number of the User."""
    while True:
        print("\nInput your Phone Number:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        phoneNumber = input(">>> ").strip()

        if re.search('^(goback|go back)$', phoneNumber, re.IGNORECASE):
            del phoneNumber
            go_back('script')
        else:
            if verify_data('phone_number', 0, phoneNumber):
                print("\n:: Phone Number already exist")
                time.sleep(3)
                continue

            if re.search(r'^\+?[0-9]{3} ?[0-9-]{8,11}$', phoneNumber) and 11 <= len(phoneNumber) <= 15:
                break
            else:
                print("\n:: Phone Number should be in digits  only.\nExample: 08076542879, +2348033327493 etc.")
                time.sleep(2)
                continue

    return phoneNumber


def account_type() -> str:
    """Gets the account type of the User."""
    while True:
        print("\nWhat is your desired Account Type:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print('1 -> Saving \n2 -> Current')
        accountType = input('>>> ')

        if re.search('^(goback|go back)$', accountType, re.IGNORECASE):
            del accountType
            go_back('script')
        else:
            if re.search('^(1|Saving)$', accountType, re.IGNORECASE):
                accountType = 'Savings'
                break
            elif re.search('^(2|Current)$', accountType, re.IGNORECASE):
                accountType = 'Current'
                break
            else:
                print("\n:: Choose between Saving or Current or Fixed Deposit")
                time.sleep(2)
                continue

    return accountType.lower()


def account_password() -> str:
    """Gets the account password of the User."""
    while True:
        print("\nEnter a new Bank Application Password:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("\nEnter Password:")
        accountPassword = input(">>> ").strip()

        if re.search('^(goback|go back)$', accountPassword, re.IGNORECASE):
            del accountPassword
            go_back('script')
        else:
            if re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$. #!%*?&])[A-Za-z\d@$!#% *?.&]{8,}$", accountPassword):
                while True:
                    print("\nRe-enter Password:")
                    second_input = input(">>> ").strip()
                    if accountPassword == second_input:
                        break
                    else:
                        print("\n:: Passwords are not the same")
                        time.sleep(2)
                        continue
                break
            else:
                print("\n:: Password must be more than 8 characters.")
                print(":: Password should contain a number, a lowercase letter, and uppercase letter and a symbol.")
                time.sleep(2)
                continue

    return accountPassword


def transaction_pin():
    """Gets the transaction pin of the User."""
    while True:
        print("\nEnter your new Transaction Pin: (A Four-digit Number)")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "~"*len(' (A Four-digit Number)'), sep="")
        print("\nEnter Transaction Pin:")
        transactionPin = input(">>> ").strip()

        if re.search('^(goback|go back)$', transactionPin, re.IGNORECASE):
            del transactionPin
            go_back('script')
        else:
            if re.search(r"^\d{4}$", transactionPin):
                while True:
                    print("\nRe-Enter Transaction Pin:")
                    second_input = input(">>> ").strip()
                    if transactionPin == second_input:
                        break
                    else:
                        print("\n:: Passwords are not the same")
                        time.sleep(2)
                        continue
                break
            else:
                print("\n:: Transaction Pin must be only 4 digits.")
                time.sleep(2)
                continue

    return transactionPin


def register_bvn_account():
    """Registration Form"""

    header()
    print('\nMessage from the CUSTOMER SERVICE OFFICER:::')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print("'You will need to Create your BVN first, then Create your Bank Account'. ")
    time.sleep(3)

    # BVN Form
    try:
        header()

        print("\nBank Verification Number Creation".upper())
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        print("\nInstruction: Carefully fill in your details")
        print("==========================================")

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

        print("\nBank Verification Number Successfully Created.")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"\nUser: {bvn.last_name} {bvn.first_name} {bvn.middle_name}")
        print(f"BVN NUMBER: {bvn.bvn_number}")
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: register_panel.py \nFunction: register_bvn_account \nError: {repr(e)}')
        print(f"\n*ERROR*\nError Creating BVN")
        go_back('script')

    time.sleep(5)

    # Bank Account Form
    try:
        header()

        print("\nBank Account Details Creation".upper())
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        print("\nInstruction: Carefully fill in your details")
        print("==========================================")

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

        print("\nBank Account Successfully Created.")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"\nUSERNAME: {user.username}")
        print(f"ACCOUNT NUMBER: {account.account_number}")
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: register_panel.py \nFunction: register_panel \nError: {repr(e)}')
        print(f"\n*ERROR*\nError Creating Bank Account")
        go_back('script')
