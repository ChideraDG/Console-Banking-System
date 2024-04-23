import datetime as dt
import time
import random
from bank_processes import bvn


# from bank_processes import database


def register_bvn():
    while True:
        print("Input your First Name:")
        print("~~~~~~~~~~~~~~~~~~~~~~")
        first_name = input(">>> ")

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

    while True:
        print("\nInput your Middle Name:")
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        middle_name = input(">>> ")

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

    while True:
        print("\nInput your Last Name:")
        print("~~~~~~~~~~~~~~~~~~~~~")
        last_name = input(">>> ")

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

    print("\nInput your Address:")
    print("~~~~~~~~~~~~~~~~~~~")
    address = input(">>> ")

    max_year = 2006
    month = 12
    month_name = 'December'
    days = 31

    while True:
        print("\nInput your Year of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        year_of_birth = input(">>> ")

        if year_of_birth.isdigit() and 1900 < int(year_of_birth) <= max_year:
            break
        else:
            print('\n*ERROR*')
            if not int(year_of_birth) <= max_year:
                print("-> Age is less than 18")
            elif not 1900 < int(year_of_birth):
                print("-> Year is less than 1900")
            else:
                print("-> Year of Birth should be in digits.\nExample: 2001, 2004, etc.")
            time.sleep(3)
            continue

    while True:
        print("\nInput your Month of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        month_of_birth = input(">>> ")

        if month_of_birth.isdigit() and 0 < int(month_of_birth) <= month:
            break
        else:
            print('\n*ERROR*')
            if not 0 < int(month_of_birth) <= 12:
                print("-> Month of Birth should be between Zero(0) and Twelve(12)")
            else:
                print("-> Month of Birth should be in digits.\nExample: 2 means February, 4 means April, etc.")
            time.sleep(3)
            continue

    month = month_of_birth
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

    while True:
        print("\nInput your Day of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        day_of_birth = input(">>> ")

        if day_of_birth.isdigit() and 0 < int(day_of_birth) <= days:
            break
        else:
            print('\n*ERROR*')
            if not 0 < int(day_of_birth) <= days:
                print(f"-> Day of Birth should be within the number of days in {month_name}")
            else:
                print("-> Day of Birth should be in digits.\nExample: 2, 4, 10, etc.")
            time.sleep(3)
            continue

    while True:
        print("\nInput your E-mail:")
        print("~~~~~~~~~~~~~~~~~~")
        email = input(">>> ")

        if email[-4:] == '.com' and '@' in email:
            break
        else:
            print('*ERROR*')
            print("-> Invalid Email.\nExample: himates@gamil.com, markjames@yahoo.com etc.")
            time.sleep(3)
            continue

    while True:
        print("\nInput your Phone Number:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        phone_number = input(">>> ")

        if phone_number.isdigit() and len(phone_number) >= 11:
            break
        elif phone_number.isdigit() and phone_number[0] == '+':
            break
        else:
            print('*ERROR*')
            print("-> Phone Number should be in digits  only.\nExample: 08076542879, +2348033327493 etc.")
            time.sleep(3)
            continue

    register = bvn.BVN(first_name=first_name.title(), middle_name=middle_name.title(), last_name=last_name.title(),
                       address=address.title(), email=email.lower(), phone_number=phone_number,
                       created_date=dt.datetime.now(), date_of_birth=f'{year_of_birth}-{month_of_birth}-{day_of_birth}',
                       bvn_status='active', bvn_number=str(random.randint(100000000000, 999999999999)),
                       last_updated=dt.datetime.now())

    register.register_bvn()
