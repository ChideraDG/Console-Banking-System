import re
import time
from animation.colors import *
from bank_processes.authentication import Authentication
from bank_processes.notification import Notification
from banking.main_menu import go_back, header, log_error
from banking.register_panel import countdown_timer
from bank_processes.bvn import BVN


notify = Notification()


def date_of_birth() -> str:
    """Gets the date of birth of the User."""

    max_year = 2006  # Maximum allowable year for the date of birth (18 years from 2024)
    month = 12       # Maximum allowable month (December)
    month_name = 'December'  # Default month name
    days = 21        # Default number of days in the month

    while True:
        header()  # Display the header.
        print(bold, brt_yellow, "\nEnter your new Year of Birth:",)
        print(magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~", sep='')

        year_of_birth = input(">>> ").strip()  # Get the user's input for the year of birth.

        if re.search('^.*(back|return).*$', year_of_birth, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            if year_of_birth.isdigit() and 1900 < int(year_of_birth) <= max_year:
                # Check if the year is a valid number and within the acceptable range.
                break
            else:
                if year_of_birth.isdigit():
                    # Provide feedback if the year is out of range.
                    if not int(year_of_birth) <= max_year:
                        print(red, "\n:: Age is less than 18", end)
                    elif not 1900 < int(year_of_birth):
                        print(red, "\n:: Year is less than 1900", end)
                else:
                    # Provide feedback if the input is not a number.
                    print(red, "\n:: Year of Birth should be in digits.\nExample: 2001, 2004, etc.", end)
                    time.sleep(2)
                    continue

    time.sleep(1)

    while True:
        print(bold, brt_yellow, "\nEnter your new Month of Birth:")
        print(magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~", sep='')

        month_of_birth = input(">>> ").strip()  # Get the user's input for the month of birth.

        if re.search('^.*(back|return).*$', month_of_birth, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            if month_of_birth.isdigit() and 0 < int(month_of_birth) <= month:
                # Check if the month is a valid number and within the acceptable range.
                break
            else:
                if month_of_birth.isdigit():
                    # Provide feedback if the month is out of range.
                    if not 0 < int(month_of_birth) <= 12:
                        print(red, "\n:: Month of Birth should be between Zero(0) and Twelve(12)", end)
                else:
                    # Provide feedback if the input is not a number.
                    print(red, "\n:: Month of Birth should be in digits.\nExample: 2 means February, 4 means April, etc.", end)
                    time.sleep(2)
                    continue

    month = int(month_of_birth)  # Convert the month input to an integer.
    # Assign month name and days based on the month.
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
        print(bold, brt_yellow, "\nEnter your new Day of Birth:")
        print(magenta, "~~~~~~~~~~~~~~~~~~~~~~~~", sep='')

        day_of_birth = input(">>> ").strip()  # Get the user's input for the day of birth.
        print(end, end='')

        if re.search('^.*(back|return).*$', day_of_birth, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            if day_of_birth.isdigit() and 0 < int(day_of_birth) <= days:
                # Check if the day is a valid number and within the allowable range.
                break
            else:
                if day_of_birth.isdigit():
                    # Provide feedback if the day is out of range.
                    if not 0 < int(day_of_birth) <= days:
                        print(f"\n:: Day of Birth should be within the number of days in {month_name}")
                else:
                    # Provide feedback if the input is not a number.
                    print("\n:: Day of Birth should be in digits.\nExample: 2, 4, 10, etc.")
                    time.sleep(2)
                    continue

    # Return the date of birth in the format YYYY-MM-DD.
    return f'{year_of_birth}-{month_of_birth}-{day_of_birth}'


def address() -> str:
    """Gets the address of the User."""

    while True:
        header()  # Display the header.
        print(bold, brt_yellow, "\nEnter new Address:")
        print(magenta, "~~~~~~~~~~~~~~~~~~~", sep='')

        _address = input(">>> ").strip()  # Get the user's input for the address.
        print(end, end='')

        if re.search('^.*(back|return).*$', _address, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            # Return the address in title case.
            return _address.title()


def first_name() -> str:
    """Gets the first name of the User."""

    while True:
        header()  # Display the header.
        print(bold, brt_yellow, '\nEnter new First name')
        print(magenta, "~~~~~~~~~~~~~~~~~~~~~~", sep='')

        name = input('>>> ').strip().title()  # Get the user's input for the first name.
        print(end, end='')

        if re.search('^.*(back|return).*$', name, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
                # Remove spaces within the name.
                name = match.group(1) + match.group(2)

            if re.search('[a-z-]+', name, re.IGNORECASE):
                # If the name is valid, simulate a countdown and display success message.
                countdown_timer('New First name', 'in')

                header()

                print(green, '\n:: First name successfully changed', end)
                time.sleep(2)
                break
            else:
                # Provide feedback if the name contains invalid characters.
                print(red, '\n:: Name must contain only alphabet.\nExample: James, Mary, etc.', end)
                time.sleep(2)
                continue
    return name.title()  # Return the name in title case.


def middle_name() -> str:
    """Gets the middle name of the User."""

    while True:
        header()  # Display the header.
        print(bold, brt_yellow, '\nEnter new Middle name')
        print(magenta, "~~~~~~~~~~~~~~~~~~~~~~", sep='')

        name = input('>>>').strip().title()  # Get the user's input for the middle name.
        print(end, end='')

        if re.search('^.*(back|return).*$', name, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
                # Remove spaces within the name.
                name = match.group(1) + match.group(2)

            if re.search('[a-z-]+', name, re.IGNORECASE):
                # If the name is valid, simulate a countdown and display success message.
                countdown_timer('New Middle name', 'in')

                header()

                print(green, '\n:: Middle name successfully changed', end)
                time.sleep(2)
                break
            else:
                # Provide feedback if the name contains invalid characters.
                print(red, '\n:: Name must contain only alphabet.\nExample: James, Mary, etc.', end)
                time.sleep(2)
                continue
    return name.title()  # Return the name in title case.


def last_name() -> str:
    """Gets the last name of the User."""

    while True:
        header()  # Display the header.
        print(bold, brt_yellow, '\nEnter new Last name')
        print(magenta, "~~~~~~~~~~~~~~~~~~~~~~", sep='')

        name = input('>>>').strip().title()  # Get the user's input for the last name.
        print(end, end='')

        if re.search('^.*(back|return).*$', name, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            if match := re.search(r'^([a-z-]+) +([a-z-]+)$', name, re.IGNORECASE):
                # Remove spaces within the name.
                name = match.group(1) + match.group(2)

            if re.search('[a-z-]+', name, re.IGNORECASE):
                # If the name is valid, simulate a countdown and display success message.
                countdown_timer('New Last name', 'in')

                header()

                print(green, '\n:: Last name successfully changed', end)
                time.sleep(2)
                break
            else:
                # Provide feedback if the name contains invalid characters.
                print(red, '\n:: Name must contain only alphabet.\nExample: James, Mary, etc.', end)
                time.sleep(2)
                continue
    return name.title()  # Return the name in title case.


def phone_number() -> str:
    """Gets the phone number of the User."""

    while True:
        header()  # Display the header.
        print(bold, brt_yellow, '\nEnter new phone number')
        print(magenta, "~~~~~~~~~~~~~~~~~~~~~~", sep='')

        number = input('>>>').strip()  # Get the user's input for the phone number.
        print(end, end='')

        if re.search('^.*(back|return).*$', number, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            if re.search(r'^\+?[0-9]{3} ?[0-9-]{8,11}$', number) and 11 <= len(number) <= 15:
                # Check if the phone number is valid.
                countdown_timer('New Phone number', 'in')

                header()

                print(green, '\n:: Phone number successfully changed', end)
                time.sleep(2)
                break
            else:
                # Provide feedback if the phone number is invalid.
                time.sleep(1)
                print(red, ':: \nPhone Number should be in digits only.\nExample: 08076542879,+2348033327493 etc.', end)
                continue
    return number


def nationality() -> str:
    """Gets the nationality of the User."""

    while True:
        header()  # Display the header.
        print(bold, brt_yellow, "\nEnter your nationality:")
        print(magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~", sep='')

        nation = input(">>> ").strip().title()  # Get the user's input for nationality.
        print(end, end='')

        if re.search('^.*(back|return).*$', nation, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            if re.search(r'[A-Za-z]+', nation, re.IGNORECASE):
                # If the nationality is valid, simulate a countdown and display success message.
                countdown_timer('New Nationality', 'in')

                header()

                print(green, '\n:: Nationality successfully changed', end)
                time.sleep(2)
                break
            else:
                # Provide feedback if the nationality contains invalid characters.
                print(red, '\n:: Nationality must contain only alphabet.\nExample: USA, Korea, etc.', end)
                time.sleep(2)
                continue
    return nation.title()  # Return the nationality in title case.


def email() -> str:
    """Gets the email address of the User."""

    while True:
        header()  # Display the header.
        print(bold, brt_yellow, "\nInput your E-mail:")
        print(magenta, "~~~~~~~~~~~~~~~~~~", sep='')

        _email = input(">>> ").strip()  # Get the user's input for the email address.
        print(end, end='')

        if re.search('^.*(back|return).*$', _email, re.IGNORECASE):
            # If the user types 'back' or 'return', exit the function.
            return 'break'
        else:
            if re.search(r"^\w+@(\w+\.)?\w+\.(edu|com|gov|ng|org)$", _email, re.IGNORECASE):
                # Check if the email is valid.
                countdown_timer('New Email', 'in')

                header()

                print(green, '\n:: Email successfully changed', end)
                time.sleep(2)
                break
            else:
                # Provide feedback if the email is invalid.
                print(red, "\n:: Invalid Email.\nExample: himates@gamil.com, markjames@yahoo.com etc.", end)
                time.sleep(2)
                continue
    return _email.lower()  # Return the email in lowercase.


def update_bvn(auth: Authentication):
    """
    Updates the BVN details for the authenticated user.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user information.

    """

    try:
        changed_object = None
        while True:
            bvn = BVN()

            header()  # Display the header.

            print(bold, brt_yellow, '\nWhat do you want to Update?')
            print(magenta, '~~~~~~~~~~~~~~~~~~~~~~~~~~~', sep='')

            print(end='\n')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print(f'|   {brt_black_bg}{brt_yellow}1. FIRST NAME{end}   {bold}{magenta}|   {brt_black_bg}{brt_yellow}2. MIDDLE NAME{end}   {bold}{magenta}|   {brt_black_bg}{brt_yellow}3. LAST NAME{end}   {bold}{magenta}|')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print(f'|  {brt_black_bg}{brt_yellow}4. PHONE NUMBER{end}  {bold}{magenta}|  {brt_black_bg}{brt_yellow}5. DATE OF BIRTH{end}  {bold}{magenta}|   {brt_black_bg}{brt_yellow}6. ADDRESS{end}     {bold}{magenta}|')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print(f'|        {brt_black_bg}{brt_yellow}7. NATIONALITY{end}        {bold}{magenta}|          {brt_black_bg}{brt_yellow}8. EMAIL{end}          {bold}{magenta}|')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")

            user_input = input(">>> ").strip()  # Get the user's input for the field to update.
            print(end, end='')

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                # If the user types 'back' or 'return', exit the function.
                break
            elif user_input == '1':
                # Update the first name.
                name = first_name()
                if name == 'break':
                    continue
                else:
                    bvn.update_bvn(_column_name='first_name', _data=name, _id_number=auth.user_id)
                    changed_object = 'First Name'
                    break
            elif user_input == '2':
                # Update the middle name.
                name = middle_name()
                if name == 'break':
                    continue
                else:
                    bvn.update_bvn(_column_name='middle_name', _data=name, _id_number=auth.user_id)
                    changed_object = 'Middle Name'
                    break
            elif user_input == '3':
                # Update the last name.
                name = last_name()
                if name == 'break':
                    continue
                else:
                    bvn.update_bvn(_column_name='last_name', _data=name, _id_number=auth.user_id)
                    changed_object = 'Last Name'
                    break
            elif user_input == '4':
                # Update the phone number.
                number = phone_number()
                if number == 'break':
                    continue
                else:
                    bvn.update_bvn(_column_name='phone_number', _data=number, _id_number=auth.user_id)
                    changed_object = 'Phone Number'
                    break
            elif user_input == '5':
                # Update the date of birth.
                dob = date_of_birth()
                countdown_timer('New DOB', 'in')

                header()

                print(green, '\n:: Date of birth successfully changed', end)
                time.sleep(2)
                if dob == 'break':
                    continue
                else:
                    bvn.update_bvn(_column_name='date_of_birth', _data=dob, _id_number=auth.user_id)
                    changed_object = 'Date of Birth'
                    break
            elif user_input == '6':
                # Update the address.
                _address = address()
                countdown_timer('New Address', 'in')

                header()

                print(green, '\n:: Address successfully changed', end)
                time.sleep(2)
                if _address == 'break':
                    continue
                else:
                    bvn.update_bvn(_column_name='address', _data=_address, _id_number=auth.user_id)
                    changed_object = 'Address'
                    break
            elif user_input == '7':
                # Update the nationality.
                nation = nationality()
                if nation == 'break':
                    continue
                else:
                    bvn.update_bvn(_column_name='nationality', _data=nation, _id_number=auth.user_id)
                    changed_object = 'Nationality'
                    break
            elif user_input == '8':
                # Update the email.
                mail = email()
                if mail == 'break':
                    continue
                else:
                    bvn.update_bvn(_column_name='email', _data=mail, _id_number=auth.user_id)
                    changed_object = 'Email'
                    break
            else:
                # Provide feedback if the input is invalid.
                print(red, '\n:: Invalid input. Try again', end)
                time.sleep(2)
                continue

        if changed_object is not None:
            notify.update_notification(
                title='Console Beta Banking',
                message=f'Your {changed_object} has been changed successfully.',
                channel='bvn_info'
            )
    except Exception as e:
        # Log any exceptions that occur and return to the signed-in state.
        log_error(e)
        go_back('signed_in', auth=auth)
