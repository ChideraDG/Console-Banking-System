import datetime
import re
import time
import random
from animation.colors import *
from bank_processes.authentication import Authentication, verify_data
from banking.register_panel import countdown_timer
from banking.script import go_back, header


def go_back_here(return_place, auth: Authentication = None):
    if return_place == 'access_safelock':
        access_safelock(auth)


def get_month(month: int) -> tuple[str, int]:
    """Generates the month name and days within that month according to the month number received.

    Args:
        month (int): the number of the month you want.

    Returns:
        tuple[str, int]: month_name, days within the month
    """
    year = 2006
    month_name = None
    days = None

    if month == 1:
        month_name = 'January'
        days = 31
    elif month == 2:
        month_name = 'February'
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
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

    return month_name, days


def get_ordinal_suffix(day: int) -> str:
    """Determine the ordinal suffix for the start and payback dates

    Parameters
    ----------
    day : int
        day of the month

    Returns
    -------
    str:
        the ordinal suffix of the day

    """
    if 10 <= day % 100 <= 20:
        return 'th'
    elif day % 10 == 1:
        return 'st'
    elif day % 10 == 2:
        return 'nd'
    elif day % 10 == 3:
        return 'rd'
    else:
        return 'th'


def calculate_interest(principal: float, rate_per_year: float, days: int):
    """Calculate the interest accrued over a period of days using the formula

    Parameters
    ----------
    principal : float
        The initial amount of money being invested
    rate_per_year : float
        The annual interest rate as a percentage.
    days : int
        The number of days the money is invested.
    """
    interest: float = (principal * rate_per_year * days) / 36500

    rate_of_interest: float = (interest * 100) / principal

    return interest, rate_of_interest


def payback_date(current_year: int, current_month: int, current_day: int, start_day: int, end_day: int,
                 auth: Authentication, percentage_rate: float, deposit_amount: float):
    """Displays the list of days for the User to select their Payback date.

    Parameters
    ----------
    current_year : int
        The Current year
    current_month : int
        The Current month
    current_day : int
         The Current day
    start_day : int
        The Start day of the User periodic choice.
    end_day : int
        The End day of the User periodic choice.
    auth : Authentication
        Contains the entire details of the User.
    percentage_rate : float
        The Interest rate with respect to the Start day and End day.
    deposit_amount : float
        The Amount the user wants to deposit.
    """
    try:
        while True:
            header()
            print("\nChoose Payback Date")
            print("~~~~~~~~~~~~~~~~~~~\n")

            dates: dict = {}
            start = start_day

            while start != 0:
                _month, _days = get_month(current_month)
                current_day += 1
                start -= 1

                if current_day > _days:
                    if current_month == 12:
                        current_year += 1
                        current_month = 0

                    current_month += 1
                    current_day = 1

            for i, day in enumerate(range(start_day, end_day + 1)):

                interest, rate_of_interest = calculate_interest(
                    principal=deposit_amount,
                    rate_per_year=percentage_rate,
                    days=day
                )

                _month, _days = get_month(current_month)

                if current_day > _days:
                    if current_month == 12:
                        current_month = 0
                        current_year += 1

                    current_month += 1
                    current_day = 1

                _month, _days = get_month(current_month)

                print(f'[{day}] -> {current_day}/{_month}/{current_year} - {rate_of_interest:.2f}%', end='\t\t\t\t\t')

                if str(current_day)[-1] == '1':
                    dates[f'{day}'] = [f'{rate_of_interest:.3f}%', f'{interest:.3f}',
                                       f'{current_day}st {_month} {current_year}',
                                       f'{current_year}-{current_month}-{current_day}']
                elif str(current_day)[-1] == '2':
                    dates[f'{day}'] = [f'{rate_of_interest:.3f}%', f'{interest:.3f}',
                                       f'{current_day}nd {_month} {current_year}',
                                       f'{current_year}-{current_month}-{current_day}']
                elif str(current_day)[-1] == '3':
                    dates[f'{day}'] = [f'{rate_of_interest:.3f}%', f'{interest:.3f}',
                                       f'{current_day}rd {_month} {current_year}',
                                       f'{current_year}-{current_month}-{current_day}']
                else:
                    dates[f'{day}'] = [f'{rate_of_interest:.3f}%', f'{interest:.3f}',
                                       f'{current_day}th {_month} {current_year}',
                                       f'{current_year}-{current_month}-{current_day}']

                current_day += 1

                if i % 3 == 2:
                    print()

            _input = input("\n>>> ")

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
                break
            else:
                if not _input.isdigit():
                    print("\n:: Numbers Only")
                    del _input
                    time.sleep(3)
                    continue
                elif start_day <= int(_input) <= end_day:
                    return dates[_input], f'{int(_input)} days', 'Beta Account Balance'
                else:
                    print("\n:: Wrong Input")
                    del _input
                    time.sleep(3)
                    continue
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: fixed_deposit \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def safelock(auth: Authentication):
    """ Filling the form for Amount to Deposit.

    Parameters
    ----------
    auth : Authentication
        Contains the entire details of the User.
    """
    try:
        while True:
            header()
            print("\nAmount to Deposit: (must be Greater than N1000)")
            print("~~~~~~~~~~~~~~~~~~")
            deposit_amount = input(">>> ").strip()

            if re.search('^.*(back|return).*$', deposit_amount, re.IGNORECASE):
                del deposit_amount
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
                break
            else:
                if re.search("^[a-z]$", deposit_amount):
                    print("\n:: No Alphabets")
                    del deposit_amount
                    time.sleep(2)
                    continue
                elif float(deposit_amount) < 1000:
                    print("\n:: Amount MUST be above N1000")
                    del deposit_amount
                    time.sleep(3)
                    continue
                else:
                    auth.amount = float(deposit_amount)
                    if auth.transaction_validation(transfer_limit=True)[0]:
                        if auth.transaction_validation(amount=True)[0]:
                            auth.initial_deposit = float(deposit_amount)
                        else:
                            print(f"\n:: {auth.transaction_validation(amount=True)[1]}")
                            del deposit_amount
                            time.sleep(2)
                            continue
                    else:
                        print(f"\n:: {auth.transaction_validation(transfer_limit=True)[1]}")
                        del deposit_amount
                        time.sleep(3)
                        go_back('signed_in', auth=auth)
                        break

                    while True:
                        header()
                        print("\nTitle of Deposit")
                        print("~~~~~~~~~~~~~~~~")
                        deposit_title = input(">>> ").strip()

                        if re.search('^.*(back|return).*$', deposit_title, re.IGNORECASE):
                            del deposit_title
                            time.sleep(1.5)
                            go_back('signed_in', auth=auth)
                            break
                        else:
                            if len(deposit_title) > 29:
                                print("\n:: Title can't be more than 30 characters")
                                del deposit_title
                                time.sleep(3)
                                continue
                            else:
                                return float(deposit_amount), deposit_title
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: safelock \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def preview_safelock(safelock_title: str, amount_to_lock: float, interest: str, interest_to_earn: float,
                     maturity_date: str, lock_duration: str, maturity_location: str, maturity_date_in_date: str,
                     auth: Authentication):
    """ Previews the details of a Fixed Deposit before the Deposit is documented into the database.
    A Safelock is a Fixed Deposit that is locked.

    Parameters
    ----------
    safelock_title : str
        Title of the safelock.
    amount_to_lock : float
        Amount the user wants to lock away for a certain period.
    interest : str
        Rate of Interest used to process the amount with respect to the period.
    interest_to_earn : float
        Amount of money to earn with respect to the interest allocated.
    maturity_date : str
        Maturity Date of the Fixed Deposit in (27th September 2024) format.
    lock_duration : str
        Amount of Days the Fixed Deposit will be locked.
    maturity_location : str
        Maturity Location of the funds after the lock duration is exhausted.
    maturity_date_in_date : str
        Maturity Date of the Fixed Deposit in (2024-09-27) format.
    auth : Authentication
        Contains the entire details of the User.
    """
    try:
        _time = datetime.datetime.today().now().time()
        while True:
            header()
            print("\nPreview your Fixed Deposit slip")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

            print('Fixed Deposit Title')
            print(safelock_title, '\n')
            print('Initial Deposit                             Interest')
            print(f'N{amount_to_lock}{' ' * (43 - len(str(amount_to_lock)))}{interest}\n')
            print('Interest To Earn                            Maturity Date')
            print(f'N{interest_to_earn}{' ' * (43 - len(str(interest_to_earn)))}{maturity_date}\n')
            print('Lock Duration                               Matures Into Your')
            print(f'{lock_duration}{' ' * (44 - len(lock_duration))}{maturity_location}\n')

            if _time.hour > 12:
                payback_time = f'{(_time.hour - 12)}:{_time.minute} PM'
            else:
                payback_time = f'{_time.hour}:{_time.minute} AM'

            print(f'I authorize Console Beta Banking to SafeLock {amount_to_lock} immediately and return it in full on'
                  f'\nthe {maturity_date} by {payback_time} to my Beta Account Balance. \n'
                  f'I confirm and approve this transaction.')
            print('1. Yes  |  2. No')
            print('~~~~~~     ~~~~~')
            _input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
                break
            else:
                if re.search('^(1|yes)$', _input, re.IGNORECASE):
                    print()
                    print(f'I hereby acknowledge that this Fixed Deposit Account CANNOT be broken once it has been '
                          f'created')
                    print('1. Yes  |  2. No')
                    print('~~~~~~     ~~~~~')
                    _input = input(">>> ").strip()
                    if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                        del _input
                        time.sleep(1.5)
                        go_back('signed_in', auth=auth)
                        break
                    else:
                        if re.search('^(1|yes)$', _input, re.IGNORECASE):

                            countdown_timer(_register='fixed deposit', countdown=5)
                            print('\rFixed Deposit Account Successfully Created.')

                            _id = 'cbb' + str(random.randint(100000000, 999999999))
                            auth.deposit_id = _id
                            while verify_data('deposit_id', 4, _id):
                                _id = 'cbb' + str(random.randint(100000000, 999999999))
                                auth.deposit_id = _id

                            auth.deposit_title = safelock_title
                            auth.initial_deposit = float(amount_to_lock)
                            auth.interest_rate = interest
                            auth.total_interest_earned = float(interest_to_earn)
                            auth.start_date = datetime.datetime.today().date()

                            year, month, day = maturity_date_in_date.split('-')
                            auth.payback_date = datetime.date(int(year), int(month), int(day))
                            auth.payback_time = _time
                            auth.status = 'active'
                            auth.description = f'FIXED_DEPOSIT/CBB/{auth.deposit_id}/{auth.deposit_title.upper()}'
                            auth.process_transaction(fixed_deposit=True)
                            auth.transaction_record(fixed_deposit=True)
                            auth.open_fixed_deposit_account()

                            header()

                            print(f'\n:: Congrats. \n:: Fixed Deposit Successfully Created.')
                            time.sleep(5)
                            break
                        elif re.search('^(2|no)$', _input, re.IGNORECASE):
                            del _input
                            time.sleep(1.5)
                            go_back('signed_in', auth=auth)
                            break
                        else:
                            print("\n:: Wrong Input")
                            del _input
                            time.sleep(3)
                            continue
                elif re.search('^(2|no)$', _input, re.IGNORECASE):
                    del _input
                    time.sleep(1.5)
                    go_back('signed_in', auth=auth)
                    break
                else:
                    print("\n:: Wrong Input")
                    del _input
                    time.sleep(3)
                    continue
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: preview_safelock \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def create_safelock(auth: Authentication):
    """Creates a Fixed Deposit for a User.

    Parameters
    ----------
    auth : Authentication
        Contains the entire details of the User.
    """
    try:
        time.sleep(1)
        header()
        print('\nMessage from the CUSTOMER SERVICE OFFICER:::')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print("'You want a new Fixed Deposit Account. Let's Create one for You.'")
        time.sleep(3)

        duration_options = {
            '1': (10, 30, 8),
            '2': (31, 60, 9),
            '3': (61, 90, 11),
            '4': (91, 180, 11.5),
            '5': (181, 270, 13.5),
            '6': (271, 365, 14),
            '7': (366, 730, 14.5),
            '8': (731, 1000, 15),
        }

        while True:
            header()
            print("\nHow long do you want to lock funds?")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("[1] -: 10 - 30 days\t\t\t\t\tat ~ 8% p.a")
            print("[2] -: 31 - 60 days\t\t\t\t\tat ~ 9% p.a")
            print("[3] -: 61 - 90 days\t\t\t\t\tat ~ 11% p.a")
            print("[4] -: 91 - 180 days\t\t\t\t\tat ~ 11.5% p.a")
            print("[5] -: 181 - 270 days\t\t\t\t\tat ~ 13.5% p.a")
            print("[6] -: 271 - 365 days\t\t\t\t\tat ~ 14% p.a")
            print("[7] -: Above 1 - 2 years\t\t\t\tat ~ 14.5% p.a")
            print("[8] -: Above 2 years\t\t\t\t\tat ~ 15% p.a")
            _input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
                break
            elif _input in duration_options:
                start_day, end_day, percentage_rate = duration_options[_input]
                date = datetime.datetime.today()
                deposit_amount, deposit_title = safelock(auth)
                dates, lock_duration, maturity_location = payback_date(
                    date.year, date.month, date.day, start_day, end_day,
                    auth, deposit_amount=deposit_amount, percentage_rate=percentage_rate
                )
                preview_safelock(
                    safelock_title=deposit_title,
                    amount_to_lock=deposit_amount,
                    interest=dates[0],
                    interest_to_earn=float(dates[1]),
                    maturity_date=dates[2],
                    lock_duration=lock_duration,
                    maturity_location=maturity_location,
                    maturity_date_in_date=dates[3],
                    auth=auth,
                )
                access_safelock(auth)
                break
            else:
                print("\n:: Wrong Input")
                time.sleep(2)
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: create_safelock \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def ongoing_display_deposits(data: list, _details: list, _key: int):
    """ Displays details of a specific ongoing deposit

    Parameters
    ----------
    data : list
        Contains the details of the Deposit in a database format
    _details : list
        Contains the details of the Deposit in a structured pictorial format
    _key : int
        Gets the number of the selected Deposit
    """
    try:
        payback_time: datetime.time = data[_key][8]

        start_day = data[_key][6].day
        payback_day = data[_key][7].day
        start_suffix = get_ordinal_suffix(start_day)
        payback_suffix = get_ordinal_suffix(payback_day)

        # Format the start and payback dates
        start_date = f'{start_day}{start_suffix} {get_month(data[_key][6].month)} {data[_key][6].year}'
        payback_date = f'{payback_day}{payback_suffix} {get_month(data[_key][7].month)} {data[_key][7].year}'

        while True:
            header()

            print('\n', _details[_key])
            print('\n')

            print(f"                 FIXED DEPOSIT DETAILS                    ")
            print(f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print(f'| Initial Deposit                  Total Interest Earned |')
            print(
                f'| N{data[_key][3]}{" " * (32 - len(str(data[_key][3])))}N{data[_key][5]}'
                f'{" " * (21 - len(str(data[_key][5])))}|')
            print(f"|                                                        |")
            print(f'| Start Date                       Payback Date          |')
            print(f'| {start_date}{" " * (33 - len(start_date))}{payback_date}{" " * (22 - len(payback_date))}|')
            print(f"|                                                        |")
            print(f'| Payback Time                     Safelock ID           |')
            print(f'| {payback_time}{" " * (33 - 8)}{data[_key][0]}{" " * (22 - len(data[_key][0]))}|')
            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+\n')

            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|      1. TOP UP DEPOSIT      |        2. RETURN         |')
            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', user_input.strip().lower()):
                pass
            elif re.search('^1$', user_input):
                # top up
                pass
            elif re.search('^2$', user_input):
                break
            else:
                print(":: Digits only.")
                time.sleep(2)
                continue

    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: display_deposits \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def paid_display_deposits(data: list, _details: list, _key: int):
    """ Displays details of a specific paid-back deposit

    Parameters
    ----------
    data : list
        Contains the details of the Deposit in a database format
    _details : list
        Contains the details of the Deposit in a structured pictorial format
    _key : int
        number of the selected Deposit
    """
    try:
        payback_time: datetime.time = data[_key][8]

        start_day = data[_key][6].day
        payback_day = data[_key][7].day
        start_suffix = get_ordinal_suffix(start_day)
        payback_suffix = get_ordinal_suffix(payback_day)

        # Format the start and payback dates
        start_date = f'{start_day}{start_suffix} {get_month(data[_key][6].month)} {data[_key][6].year}'
        payback_date = f'{payback_day}{payback_suffix} {get_month(data[_key][7].month)} {data[_key][7].year}'

        while True:
            header()

            print('\n', _details[_key])

            print(f"/n                 FIXED DEPOSIT DETAILS                    ")
            print(f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print(f'| Initial Deposit                  Total Interest Earned |')
            print(
                f'| N{data[_key][3]}{" " * (32 - len(str(data[_key][3])))}N{data[_key][5]}'
                f'{" " * (21 - len(str(data[_key][5])))}|')
            print(f"|                                                        |")
            print(f'| Start Date                       Payback Date          |')
            print(f'| {start_date}{" " * (33 - len(start_date))}{payback_date}{" " * (22 - len(payback_date))}|')
            print(f"|                                                        |")
            print(f'| Payback Time                     Safelock ID           |')
            print(f'| {payback_time}{" " * (33 - 8)}{data[_key][0]}{" " * (22 - len(data[_key][0]))}|')
            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+\n')

            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|                       1. RETURN                        |')
            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', user_input.strip().lower()):
                pass
            elif re.search('^(1|return)$', user_input):
                break
            else:
                print(":: Digits only.")
                time.sleep(2)
                continue
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: display_deposits \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def ongoing_deposits(auth: Authentication):
    """ Displays the User's fixed deposits that are still running active.

    Parameters
    ----------
    auth : Authentication
          Contains the entire details of the User.
    """
    try:
        data, balance, days, days_remaining = auth.get_active()
        details = []

        while True:
            header()

            print("\nONGOING DEPOSITS")
            print("~~~~~~~~~~~~~~~~\n")

            if data:
                for key, value in enumerate(data):
                    space = '  ' if len(str(days_remaining[key])) == 2 else ' ' \
                        if len(str(days_remaining[key])) == 3 else '   '
                    bar_length = 46

                    if days_remaining[key] == 0:
                        progress_length = 0
                    else:
                        progress_length = bar_length // days[key]

                    progress = progress_length * (days[key] - days_remaining[key])
                    remaining = bar_length - progress

                    detail = (f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+\n"
                              f"|                                                         |\n"
                              f"|   {key + 1}. {data[key][2]}{' ' * (47 - len(str(data[key][2])))}    |\n"
                              f"|      N{data[key][3]:,}{' ' * (48 - len(str(data[key][3])))} |\n"
                              f"|      Locked{' ' * (50 - len('locked'))} |\n"
                              f"|                                                         |\n"
                              f"| {brt_blue_bg}{' ' * progress}{brt_white_bg}{' ' * remaining}{end} "
                              f"{days_remaining[key]} days{space}|\n"
                              f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

                    details.append(detail)
                    print(detail, '\n')

                user_input = input(">>> ").strip()

                if re.search('^.*(back|return).*$', user_input.strip().lower()):
                    del user_input
                    go_back_here('access_safelock', auth)
                elif user_input.isdigit():
                    if int(user_input) > len(data):
                        print("\n:: Digits within the list only")
                        time.sleep(2)
                        continue
                    else:
                        ongoing_display_deposits(data, details, int(user_input) - 1)
                        continue
                else:
                    print("\n:: Digits only.")
                    time.sleep(2)
                    continue
            else:
                print("You don't have any Ongoing Deposit")
                time.sleep(5)
                go_back_here('access_safelock', auth)
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: ongoing_deposits \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def paid_back_deposits(auth: Authentication):
    """ Displays the deposits that have been completed and returned to the User.

    Parameters
    ----------
    auth : Authentication
          Contains the entire details of the User.
    """
    try:
        data = auth.get_inactive()
        details = []

        while True:
            header()

            print("\nPAID BACK DEPOSITS")
            print("~~~~~~~~~~~~~~~~~~\n")

            if data:
                for key, value in enumerate(data):
                    detail = (f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+\n"
                              f"|                                                         |\n"
                              f"|   {key + 1}. {data[key][2]}{' ' * (47 - len(str(data[key][2])))}    |\n"
                              f"|      N{data[key][3]:,}{' ' * (48 - len(str(data[key][3])))} |\n"
                              f"|      Unlocked{' ' * (50 - len('Unlocked'))} |\n"
                              f"|                                                         |\n"
                              f"| {brt_blue_bg}{' ' * 48} {end}  Paid |\n"
                              f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

                    details.append(detail)
                    print(detail, '\n')

                user_input = input(">>> ").strip()

                if re.search('^.*(back|return).*$', user_input.strip().lower()):
                    del user_input
                    go_back_here('access_safelock', auth)
                elif user_input.isdigit():
                    if int(user_input) > len(data):
                        print("\n:: Digits within the list only")
                        time.sleep(2)
                        continue
                    else:
                        paid_display_deposits(data, details, int(user_input) - 1)
                        continue
                else:
                    print("\n:: Digits only.")
                    time.sleep(2)
                    continue
            else:
                print("You don't have any Paid Back Deposit")
                time.sleep(5)
                go_back_here('access_safelock', auth)
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: paid_back_deposits \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def access_safelock(auth: Authentication):
    """ To display the homepage for a fixed deposit user, providing options to view balance, ongoing deposits,
    paid back deposits, and create new fixed deposits.

    Parameters
    ---------
    auth : Authentication
          Contains the entire details of the User.
    """
    try:
        data, balance, days, days_remaining = auth.get_active()
        sl_balance = f'N{balance:,.2f}'
        eye = 'HIDE'
        while True:
            header()
            print(f"{bold}{brt_black_bg}{brt_red}" + f"\n8% - 15% per annum{end}")

            print(f"{bold}{brt_black_bg}{brt_yellow}")
            print("Fixed Deposit Balance" + f"{end}")

            print(f'{bold}{sl_balance}{end} \n')
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print(f"|                   1. {eye} BALANCE                       |")
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print("|    2. ONGOING DEPOSITS    |    3. PAID BACK DEPOSITS    |")
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print("|              4. CREATE A NEW FIXED DEPOSIT              |")
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

            user_input = input(">>> ").strip()

            if re.search('^1$', user_input):
                if eye == 'SHOW':
                    eye = 'HIDE'
                    sl_balance = f'N{balance:,.2f}'
                else:
                    sl_balance = ' * * * * *'
                    eye = 'SHOW'

                continue
            elif re.search('^2$', user_input):
                ongoing_deposits(auth)
            elif re.search('^3$', user_input):
                paid_back_deposits(auth)
            elif re.search('^4$', user_input):
                create_safelock(auth)
            elif re.search('^.*(back|return).*$', user_input.strip().lower()):
                del user_input
                go_back('signed_in', auth)
            else:
                del user_input
                continue
            break
    except Exception as e:
        with open('notification/error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: access_safelock \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')
