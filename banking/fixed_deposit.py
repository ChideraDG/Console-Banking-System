import datetime
import re
import time
import random

from bank_processes.authentication import Authentication, verify_data
from banking.register_panel import countdown_timer
from banking.script import go_back, header
#
# auth = Authentication()
# auth.account_number = 1513500889


def get_month(month):
    max_year = 2006
    month_name = None
    days = None

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

    return month_name, days


def calculate_interest(principal: float, rate_per_year: int, days: int):
    interest: float = (principal * rate_per_year * days) / 36500

    rate_of_interest: float = (interest * 100) / principal

    return interest, rate_of_interest


def payback_date(current_year: int, current_month: int, current_day: int, start_day: int, end_day: int,
                 auth: Authentication, percentage_rate: float, deposit_amount: float):
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

                if str(current_day)[-1] == 1:
                    dates[f'{day}'] = [f'{rate_of_interest:.3f}%', f'{interest:.3f}',
                                       f'{current_day}st {_month} {current_year}',
                                       f'{current_year}-{current_month}-{current_day}']
                elif str(current_day)[-1] == 2:
                    dates[f'{day}'] = [f'{rate_of_interest:.3f}%', f'{interest:.3f}',
                                       f'{current_day}nd {_month} {current_year}',
                                       f'{current_year}-{current_month}-{current_day}']
                elif str(current_day)[-1] == 3:
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

            if re.search('^(goback|go back)$', _input, re.IGNORECASE):
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
        with open('error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: fixed_deposit \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def safelock(auth: Authentication):
    try:
        while True:
            header()
            print("\nAmount to Deposit: (must be Greater than N1000)")
            print("~~~~~~~~~~~~~~~~~~")
            deposit_amount = input(">>> ")

            if re.search('^(goback|go back)$', deposit_amount, re.IGNORECASE):
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
                elif int(deposit_amount) < 1000:
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
                        deposit_title = input(">>> ")

                        if re.search('^(goback|go back)$', deposit_title, re.IGNORECASE):
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
        with open('error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: fixed_deposit \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def preview_safelock(safelock_title: str, amount_to_lock: float, interest: str, interest_to_earn: float,
                     maturity_date: str, lock_duration: str, maturity_location: str, maturity_date_in_date: str,
                     auth: Authentication):
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
                payback_time = f'{(_time.hour - 12)} : {_time.minute} PM'
            else:
                payback_time = f'{_time.hour} : {_time.minute} AM'

            print(f'I authorize Console Beta Banking to SafeLock {amount_to_lock} immediately and return it in full on'
                  f'\nthe {maturity_date} by {payback_time} to my Beta Account Balance. \n'
                  f'I confirm and approve this transaction.')
            print('1. Yes  |  2. No')
            print('~~~~~~     ~~~~~')
            _input = input(">>> ")

            if re.search('^(goback|go back)$', _input, re.IGNORECASE):
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
                    _input = input(">>> ")
                    if re.search('^(goback|go back)$', _input, re.IGNORECASE):
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

                            auth.open_fixed_deposit_account()
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
        with open('error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: preview_safelock \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def fixed_deposit(auth: Authentication):
    try:
        while True:
            header()
            print("\nHow long do you want to lock funds?")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("[1] -: 10 - 30 days", "\t\t\t\t\t", "at ~ 8% p.a\n", sep='')
            print("[2] -: 31 - 60 days", "\t\t\t\t\t", "at ~ 9% p.a\n", sep='')
            print("[3] -: 61 - 90 days", "\t\t\t\t\t", "at ~ 11% p.a\n", sep='')
            print("[4] -: 91 - 180 days", "\t\t\t\t\t", "at ~ 11.5% p.a\n", sep='')
            print("[5] -: 181 - 270 days", "\t\t\t\t\t", "at ~ 13.5% p.a\n", sep='')
            print("[6] -: 271 - 365 days", "\t\t\t\t\t", "at ~ 14% p.a\n", sep='')
            print("[7] -: Above 1 - 2 years", "\t\t\t\t", "at ~ 14.5% p.a\n", sep='')
            print("[8] -: Above 2 years", "\t\t\t\t\t", "at ~ 15% p.a\n", sep='')
            _input = input(">>> ")

            if re.search('^(goback|go back)$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
                break
            else:
                if re.search('^[1-8]$', _input) is None:
                    print("\n:: Wrong Input")
                    time.sleep(2)
                    continue
                else:
                    date = datetime.datetime.today()
                    if _input == '1':
                        start_day = 10
                        end_day = 30
                        deposit_amount, deposit_title = safelock(auth)
                        dates, lock_duration, maturity_location = (
                            payback_date(
                                date.year, date.month, date.day, start_day, end_day,
                                auth, deposit_amount=deposit_amount, percentage_rate=8
                            )
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
                    elif _input == '2':
                        start_day = 31
                        end_day = 60
                        deposit_amount, deposit_title = safelock(auth)
                        dates, lock_duration, maturity_location = (
                            payback_date(
                                date.year, date.month, date.day, start_day, end_day,
                                auth, deposit_amount=deposit_amount, percentage_rate=9
                            )
                        )
                        print(deposit_title, deposit_amount, dates, lock_duration, maturity_location)
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
                    elif _input == '3':
                        start_day = 61
                        end_day = 90
                        deposit_amount, deposit_title = safelock(auth)
                        dates, lock_duration, maturity_location = (
                            payback_date(
                                date.year, date.month, date.day, start_day, end_day,
                                auth, deposit_amount=deposit_amount, percentage_rate=11
                            )
                        )
                        print(deposit_title, deposit_amount, dates, lock_duration, maturity_location)
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
                    elif _input == '4':
                        start_day = 91
                        end_day = 180
                        deposit_amount, deposit_title = safelock(auth)
                        dates, lock_duration, maturity_location = (
                            payback_date(
                                date.year, date.month, date.day, start_day, end_day,
                                auth, deposit_amount=deposit_amount, percentage_rate=11.5
                            )
                        )
                        print(deposit_title, deposit_amount, dates, lock_duration, maturity_location)
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
                    elif _input == '5':
                        start_day = 181
                        end_day = 270
                        deposit_amount, deposit_title = safelock(auth)
                        dates, lock_duration, maturity_location = (
                            payback_date(
                                date.year, date.month, date.day, start_day, end_day,
                                auth, deposit_amount=deposit_amount, percentage_rate=13.5
                            )
                        )
                        print(deposit_title, deposit_amount, dates, lock_duration, maturity_location)
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
                    elif _input == '6':
                        start_day = 270
                        end_day = 365
                        deposit_amount, deposit_title = safelock(auth)
                        dates, lock_duration, maturity_location = (
                            payback_date(
                                date.year, date.month, date.day, start_day, end_day,
                                auth, deposit_amount=deposit_amount, percentage_rate=14
                            )
                        )
                        print(deposit_title, deposit_amount, dates, lock_duration, maturity_location)
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
                    elif _input == '7':
                        start_day = 366
                        end_day = 730
                        deposit_amount, deposit_title = safelock(auth)
                        dates, lock_duration, maturity_location = (
                            payback_date(
                                date.year, date.month, date.day, start_day, end_day,
                                auth, deposit_amount=deposit_amount, percentage_rate=14.5
                            )
                        )
                        print(deposit_title, deposit_amount, dates, lock_duration, maturity_location)
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
                    elif _input == '8':
                        start_day = 731
                        end_day = 1000
                        deposit_amount, deposit_title = safelock(auth)
                        dates, lock_duration, maturity_location = (
                            payback_date(
                                date.year, date.month, date.day, start_day, end_day,
                                auth, deposit_amount=deposit_amount, percentage_rate=15
                            )
                        )
                        print(deposit_title, deposit_amount, dates, lock_duration, maturity_location)
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
            break
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Module: fixed_deposit.py \nFunction: fixed_deposit \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')

#
# fixed_deposit(auth=auth)
