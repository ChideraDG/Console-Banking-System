import re
import time
from animation.colors import *
from banking.script import go_back
from banking.register_panel import countdown_timer


def date_of_birth() -> str:
    """Gets the date of birth of the User."""
    max_year = 2006
    month = 12
    month_name = 'December'
    days = 21

    while True:
        print("\nEnter Your New Year of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        year_of_birth = input(">>> ").strip()

        if re.search('^.*(back|return).*$', year_of_birth, re.IGNORECASE):
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
        print("\nEnter your New Month of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        month_of_birth = input(">>> ").strip()

        if re.search('^.*(back|return).*$', month_of_birth, re.IGNORECASE):
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
        print("\nEnter your New Day of Birth:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        day_of_birth = input(">>> ").strip()

        if re.search('^.*(back|return).*$', day_of_birth, re.IGNORECASE):
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


def address() -> str:
    while True:
        """Gets the address of the User."""
        print("\nEnter New Address:")
        print("~~~~~~~~~~~~~~~~~~~")
        _address = input(">>> ").strip()

        if re.search('^.*(back|return).*$', _address, re.IGNORECASE):
            del _address
            break
        else:
            return _address.title()


def first_name() -> str:
    print()
    while True:
        print('Enter new first name')
        print("~~~~~~~~~~~~~~~~~~~~~~")
        print()
        name = input('>>> ').strip().title()

        if re.search('^.*(back|return).*$', name, re.IGNORECASE):
            break

        else:
            if re.fullmatch(r'[A-Za-z]+', name):
                countdown_timer('3')
                print('First name successfully change')
                time.sleep(2)
                break

            else:
                time.sleep(1)
                print('\n:: Name must contain only alphabet.\nExample: James, Mary, etc.')
                print()
                continue
    return name.title()


def second_name() -> str:
    print()
    while True:
        print('Enter new second name')
        print("~~~~~~~~~~~~~~~~~~~~~~")
        print()
        name = input('>>>').strip().title()

        if re.search('^.*(back|return).*$', name, re.IGNORECASE):
            break

        else:
            if re.fullmatch(r'[A-Za-z]+', name):
                countdown_timer('3')
                print('Second name successfully change')
                time.sleep(2)
                break

            else:
                time.sleep(1)
                print('\n:: Name must contain only alphabet.\nExample: James, Mary, etc.')
                print()
                continue
    return name.title()


def last_name() -> str:
    print()
    while True:
        print('Enter new Last name')
        print("~~~~~~~~~~~~~~~~~~~~~~")
        print()
        name = input('>>>').strip().title()

        if re.search('^.*(back|return).*$', name, re.IGNORECASE):
            break

        else:
            if re.fullmatch(r'[A-Za-z]+', name):
                countdown_timer('3')
                print('Last name successfully change')
                time.sleep(2)
                break

            else:
                time.sleep(1)
                print('\n:: Name must contain only alphabet.\nExample: James, Mary, etc.')
                print()
                continue
    return name.title()


def phone_number() -> str:
    print()
    while True:
        print('Enter new phone number')
        print("~~~~~~~~~~~~~~~~~~~~~~")
        print()
        number = input('>>>').strip()

        if re.search('^.*(back|return).*$', number, re.IGNORECASE):
            break

        else:
            if re.search(r'^\+?[0-9]{3} ?[0-9-]{8,11}$', number) and 11 <= len(number) <= 15:
                countdown_timer('3')
                print('Phone number successfully change')
                time.sleep(2)
                break

            else:
                time.sleep(1)
                print()
                print(':: Phone Number should be in digits only.\nExample: 08076542879,+2348033327493 etc.')
                print()
                continue
    return number


def nationality() -> str:
    while True:
        print("\nEnter your nationality:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        nation = input(">>> ").strip().title()

        if re.search('^.*(back|return).*$', nation, re.IGNORECASE):
            break

        else:
            if re.fullmatch(r'[A-Za-z]+', nation):
                countdown_timer('3')
                print('Nationality successfully change')
                time.sleep(2)
                break

            else:
                time.sleep(1)
                print('\n:: Nationality must contain only alphabet.\nExample: USA, Korea, etc.')
                print()
                continue
    return nation.title()


def email() -> str:
    while True:
        print("\nInput your E-mail:")
        print("~~~~~~~~~~~~~~~~~~")
        _email = input(">>> ").strip()

        if re.search('^.*(back|return).*$', _email, re.IGNORECASE):
            break

        else:
            if re.search(r"^\w+@(\w+\.)?\w+\.(edu|com|gov|ng|org)$", _email, re.IGNORECASE):
                countdown_timer('3')
                print('Email successfully change')
                time.sleep(2)
                break

            else:
                print("\n:: Invalid Email.\nExample: himates@gamil.com, markjames@yahoo.com etc.")
                time.sleep(2)
                print()
                continue
    return _email.lower()


def update_bvn():
    try:
        while True:
            print('\nEnter what to update ')
            time.sleep(1)
            print(end='\n')
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print('|        1. FIRST NAME      |       2. SECOND NAME             |         3. LAST NAME             |')
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print('|        4. PHONE NUMBER    |       5. DATE OF BIRTH           |         6. ADDRESS               |')
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print('|                    7. NATIONALITY          |                8. EMAIL                            |')
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            time.sleep(1)
            user_input = input("\n>>> ").strip()

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                break

            elif user_input == '1':
                name = first_name()
                break

            elif user_input == '2':
                name = second_name()
                break

            elif user_input == '3':
                name = last_name()
                break

            elif user_input == '4':
                number = phone_number()
                break

            elif user_input == '5':
                dob = date_of_birth()
                countdown_timer('3')
                print('Date of birth successfully changed')
                time.sleep(2)
                break

            elif user_input == '6':
                _address = address()
                countdown_timer('3')
                print('Address successfully change')
                time.sleep(2)
                break

            elif user_input == '7':
                nation = nationality()
                break

            elif user_input == '8':
                mail = email()
                break

            else:
                print('invalid input. Try again')
                print()
                time.sleep(2)

    except Exception as e:
        print('An error occurred: ', e)


update_bvn()
