import datetime as dt
import os
import re
import time
import random
from bank_processes.bvn import BVN
from bank_processes.database import DataBase


def get_data(get_column: str, table_number: int, _object: str) -> bool:
    """Validates unique values against the database to check if it exists before or not"""
    db: DataBase = DataBase()

    query = (f"""
    select {get_column} from {db.db_tables[table_number]}
    """)

    datas: tuple = db.fetch_data(query)

    for datas in datas:
        if (_object,) == datas:
            return True

    return False


def clear():
    """Helps Clear the Output Console"""
    os.system('clear')


def header():
    """Clears the output and adds the bank header"""
    clear()
    today_date = dt.datetime.now().date()
    time_now = dt.datetime.now().time()

    print(f"BETA BANKING {today_date} {time_now}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


def countdown_timer(register):
    """Countdown for the bank or bvn creation. It enhances users' experience."""
    print()
    countdown = 3
    while countdown != 0:
        print(f"processing {register} creation...{countdown}", end='')
        countdown -= 1
        time.sleep(1)
        print(end='\r')


def first_name() -> str:
    while True:
        print("\nInput your First Name:")
        print("~~~~~~~~~~~~~~~~~~~~~~")
        name = input(">>> ").strip()

        if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
            name = match.group(1) + match.group(2)
        print(name)
        if re.search('^[a-z-]+$', name, re.IGNORECASE):
            break
        else:
            print('\n*ERROR*')
            print("-> Names should be in letters only.\nExample: James, Mary, etc.")
            time.sleep(2)
            continue

    return name.title()


def middle_name() -> str:
    while True:
        print("\nInput your Middle Name:")
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        name = input(">>> ").strip()

        if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
            name = match.group(1) + match.group(2)

        if re.search('[a-z-]+', name, re.IGNORECASE):
            break
        else:
            print('\n*ERROR*')
            print("-> Names should be in letters only.\nExample: James, Mary, etc.")
            time.sleep(2)
            continue

    return name.title()


def last_name() -> str:
    while True:
        print("\nInput your Last Name:")
        print("~~~~~~~~~~~~~~~~~~~~~")
        name = input(">>> ").strip()

        if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
            name = match.group(1) + match.group(2)

        if re.search('[a-z-]+', name, re.IGNORECASE):
            break
        else:
            print('\n*ERROR*')
            print("-> Names should be in letters only.\nExample: James, Mary, etc.")
            time.sleep(2)
            continue

    return name.title()


def gender() -> str:
    while True:
        print("\nInput your Gender:")
        print("~~~~~~~~~~~~~~~~~~~~~")
        _gender = input(">>> ").strip()

        if not re.search('^(male|female)$', _gender, re.IGNORECASE):
            print('\n*ERROR*')
            print("-> Gender should be either Male or Female only.")
            time.sleep(2)
            continue
        else:
            break

    return _gender.title()


def address() -> str:
    print("\nInput your Address:")
    print("~~~~~~~~~~~~~~~~~~~")
    _address = input(">>> ").strip()

    return _address.title()


def date_of_birth() -> str:
    max_year = 2006
    month = 12
    month_name = 'December'
    days = 21

    while True:
        print("\nInput your Year of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        year_of_birth = input(">>> ").strip()

        if year_of_birth.isdigit() and 1900 < int(year_of_birth) <= max_year:
            break
        else:
            print('\n*ERROR*')
            if year_of_birth.isdigit():
                if not int(year_of_birth) <= max_year:
                    print("-> Age is less than 18")
                elif not 1900 < int(year_of_birth):
                    print("-> Year is less than 1900")
            else:
                print("-> Year of Birth should be in digits.\nExample: 2001, 2004, etc.")
            time.sleep(2)
            continue

    time.sleep(1)

    while True:
        print("\nInput your Month of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        month_of_birth = input(">>> ").strip()

        if month_of_birth.isdigit() and 0 < int(month_of_birth) <= month:
            break
        else:
            print('\n*ERROR*')
            if month_of_birth.isdigit():
                if not 0 < int(month_of_birth) <= 12:
                    print("-> Month of Birth should be between Zero(0) and Twelve(12)")
            else:
                print("-> Month of Birth should be in digits.\nExample: 2 means February, 4 means April, etc.")
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

        if day_of_birth.isdigit() and 0 < int(day_of_birth) <= days:
            break
        else:
            print('\n*ERROR*')
            if day_of_birth.isdigit():
                if not 0 < int(day_of_birth) <= days:
                    print(f"-> Day of Birth should be within the number of days in {month_name}")
            else:
                print("-> Day of Birth should be in digits.\nExample: 2, 4, 10, etc.")
            time.sleep(2)
            continue

    return f'{year_of_birth}-{month_of_birth}-{day_of_birth}'


def e_mail() -> str:
    while True:
        print("\nInput your E-mail:")
        print("~~~~~~~~~~~~~~~~~~")
        email = input(">>> ").strip()

        if get_data('email', 0, email):
            print('\n*ERROR*')
            print("-> Email already exist")
            time.sleep(2)
            continue

        if re.search(r"^\w+@(\w+\.)?\w+\.(edu|com|gov|ng|org)$", email, re.IGNORECASE):
            break
        else:
            print('\n*ERROR*')
            print("-> Invalid Email.\nExample: himates@gamil.com, markjames@yahoo.com etc.")
            time.sleep(2)
            continue

    return email.lower()


def phone_number() -> str:
    while True:
        print("\nInput your Phone Number:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        phoneNumber = input(">>> ").strip()

        if get_data('phone_number', 0, phoneNumber):
            print('\n*ERROR*')
            print("-> Phone Number already exist")
            time.sleep(3)
            continue

        if re.search(r'^\+?[0-9]{3} ?[0-9-]{8,11}$', phoneNumber) and 11 <= len(phoneNumber) <= 15:
            break
        else:
            print('\n*ERROR*')
            print("-> Phone Number should be in digits  only.\nExample: 08076542879, +2348033327493 etc.")
            time.sleep(2)
            continue

    return phoneNumber


def account_type():
    while True:
        print("What is your desired Account Type:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print('1 -> Saving \n2 -> Current \n3 -> Fixed Deposit')
        _input = input('>>> ')

        if re.search('^(1|Saving)$', _input, re.IGNORECASE):
            _input = 'Savings'
            break
        elif re.search('^(2|Current)$', _input, re.IGNORECASE):
            _input = 'Current'
            break
        elif re.search('^(3|Fixed Deposit)$', _input, re.IGNORECASE):
            _input = 'Fixed Deposit'
            break
        else:
            print('\n*ERROR*')
            print("-> Choose between Saving or Current or Fixed Deposit")
            time.sleep(2)
            continue


def check_password(passwords: str) -> set:
    number, upper_letters, lower_letters, symbols = False, False, False, False
    alphabets = 'abcdefghijklmnopqrstuvwxyyz'

    if len(passwords) > 8:
        number = {
            True for password in list(passwords) if password.isdigit() if int(password) in list(range(0, 10))
        }

        lower_letters = {
            True for password in list(passwords) if password in list(alphabets)
        }

        upper_letters = {
            True for password in list(passwords) if password in list(alphabets.upper())
        }

        symbols = {
            True for password in list(passwords) if password in list('!@#$%&*()_+-{}[]|?.,<>;:~\'')
        }

        return number and upper_letters and lower_letters and symbols
    else:
        return {False}


def account_password():
    while True:
        print("\nEnter a new Bank Application Password:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        print("First Input:")
        first_input = input(">>> ").strip()

        if check_password(first_input) == {True}:
            while True:
                print("\nSecond Input:")
                second_input = input(">>> ").strip()
                if first_input == second_input:
                    break
                else:
                    print('\n*ERROR*')
                    print("-> Passwords not the same")
                    time.sleep(2)
                    continue
            break
        else:
            print('\n*ERROR*')
            print("-> Password must be more than 8 characters.")
            print("-> Password should contain a number, a lowercase letter, and uppercase letter and a symbol.")
            time.sleep(2)
            continue


def register_bvn():
    """Registration Form"""

    try:
        print("Bank Verification Number Creation".upper())
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        print("\nInstruction: Carefully fill in your details")
        print("==========================================\n")

        time.sleep(1)

        _firstname = first_name()

        time.sleep(1)

        _middlename = middle_name()

        time.sleep(1)

        _lastname = last_name()

        time.sleep(1)

        _gender = gender()

        time.sleep(1)

        _address = address()

        time.sleep(1)

        _dob = date_of_birth()

        time.sleep(1)

        _email = e_mail()

        time.sleep(1)

        _phoneNumber = phone_number()

        created_bvn = str(random.randint(100000000000, 999999999999))
        while get_data('bvn_number', 0, created_bvn):
            created_bvn = str(random.randint(100000000000, 999999999999))

        register = BVN(first_name=_firstname.title(), middle_name=_middlename.title(), last_name=_lastname.title(),
                       gender=_gender.title(), address=_address.title(), email=_email.lower(),
                       phone_number=_phoneNumber, created_date=dt.datetime.now(), date_of_birth=_dob,
                       bvn_status='active', bvn_number=created_bvn, last_updated=dt.datetime.now())

        # register.register_bvn()

        countdown_timer('BVN')
        time.sleep(1)
        header()

        print("\nBank Verification Number Successfully Created.")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"\nUser: {register.last_name} {register.first_name} {register.middle_name}")
        print(f"BVN NUMBER: {register.bvn_number}")
    except Exception:
        print(f"\n*ERROR*\nError registering BVN")


def register_account():
    """Account Form"""

    print("Bank Account Details Creation".upper())
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("\nInstruction: Carefully fill in your details")
    print("==========================================\n")

    account_number = str(random.randint(1000000000, 9999999999))
    while get_data('account_number', 1, account_number):
        account_number = str(random.randint(100000000000, 999999999999))

    time.sleep(1)

    account_type()

    time.sleep(1)

    account_password()
