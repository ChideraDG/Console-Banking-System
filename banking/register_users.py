import datetime as dt
import os
import time
import random
from bank_processes import bvn
from bank_processes.database import DataBase


def get_data(getter, value):
    """Validates unique values against the database to check if it exist before or not"""
    db: DataBase = DataBase()

    query = (f"""
    select {getter} from {db.db_tables[0]}
    """)

    data_from_database: tuple = db.fetch_data(query)

    flag = False
    for datas in data_from_database:
        for data in datas:
            if value == data:
                flag = True

    return flag


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


def register_bvn():
    """Registration Form"""
    print("Bank Verification Number CREATION".upper())
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("\nInstruction: Carefully fill in your details")
    print("==========================================\n")

    while True:
        print("\nInput your First Name:")
        print("~~~~~~~~~~~~~~~~~~~~~~")
        first_name = input(">>> ").strip().title()

        if '-' in first_name:
            if first_name[:first_name.index('-')].isalpha() and first_name[first_name.index('-'):].isalpha():
                break
            break
        elif first_name.isalpha():
            break
        else:
            print('\n*ERROR*')
            print("-> Names should be in letters only.\nExample: James, Mary, etc.")
            time.sleep(3)
            continue

    time.sleep(1)

    while True:
        print("\nInput your Middle Name:")
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        middle_name = input(">>> ").strip().title()

        if '-' in middle_name:
            if middle_name[:middle_name.index('-')].isalpha() and middle_name[middle_name.index('-'):].isalpha():
                break
            break
        elif middle_name.isalpha():
            break
        else:
            print('\n*ERROR*')
            print("-> Names should be in letters only.\nExample: James, Mary, etc.")
            time.sleep(3)
            continue

    time.sleep(1)

    while True:
        print("\nInput your Last Name:")
        print("~~~~~~~~~~~~~~~~~~~~~")
        last_name = input(">>> ").strip().title()

        if '-' in last_name:
            if last_name[:last_name.index('-')].isalpha() and last_name[last_name.index('-'):].isalpha():
                break
            break
        elif last_name.isalpha():
            break
        else:
            print('\n*ERROR*')
            print("-> Names should be in letters only.\nExample: James, Mary, etc.")
            time.sleep(3)
            continue

    time.sleep(1)

    while True:
        print("\nInput your Gender:")
        print("~~~~~~~~~~~~~~~~~~~~~")
        gender = input(">>> ").strip().title()

        if not gender.isalpha():
            print('\n*ERROR*')
            print("-> Gender should be in letters only.\nExample: Male, Female")
            time.sleep(3)
            continue
        elif not (gender == 'Male' or gender == 'Female'):
            print('\n*ERROR*')
            print("-> Gender should be either Male or Female only.")
            time.sleep(3)
            continue
        else:
            break

    time.sleep(1)

    print("\nInput your Address:")
    print("~~~~~~~~~~~~~~~~~~~")
    address = input(">>> ").strip().title()

    max_year = 2006
    month = 12
    month_name = 'December'
    days = 31

    time.sleep(1)

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
            time.sleep(3)
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
            time.sleep(3)
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
            time.sleep(3)
            continue

    time.sleep(1)

    while True:
        print("\nInput your E-mail:")
        print("~~~~~~~~~~~~~~~~~~")
        email = input(">>> ").strip().lower()

        if get_data('email', email):
            print('\n*ERROR*')
            print("-> Email already exist")
            time.sleep(3)
            continue

        if email[-4:] == '.com' and '@' in email:
            break
        else:
            print('\n*ERROR*')
            print("-> Invalid Email.\nExample: himates@gamil.com, markjames@yahoo.com etc.")
            time.sleep(3)
            continue

    time.sleep(1)

    while True:
        print("\nInput your Phone Number:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        phone_number = input(">>> ").strip()

        if get_data('phone_number', phone_number):
            print('\n*ERROR*')
            print("-> Phone Number already exist")
            time.sleep(3)
            continue

        if phone_number.isdigit() and 11 <= len(phone_number) <= 15:
            break
        elif phone_number[1:].isdigit() and phone_number[0] == '+':
            break
        else:
            print('\n*ERROR*')
            print("-> Phone Number should be in digits  only.\nExample: 08076542879, +2348033327493 etc.")
            time.sleep(3)
            continue

    created_bvn = str(random.randint(100000000000, 999999999999))
    while get_data('bvn_number', created_bvn):
        created_bvn = str(random.randint(100000000000, 999999999999))

    register = bvn.BVN(first_name=first_name.title(), middle_name=middle_name.title(), last_name=last_name.title(),
                       gender=gender, address=address.title(), email=email.lower(), phone_number=phone_number,
                       created_date=dt.datetime.now(), date_of_birth=f'{year_of_birth}-{month_of_birth}-{day_of_birth}',
                       bvn_status='active', bvn_number=created_bvn, last_updated=dt.datetime.now())

    register.register_bvn()

    countdown_timer('BVN')
    time.sleep(1)
    header()

    print("\nBank Verification Number Successfully Created.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"\nUser: {register.last_name} {register.first_name} {register.middle_name}")
    print(f"BVN NUMBER: {register.bvn_number}")
