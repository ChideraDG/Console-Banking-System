import datetime
import re
import time
import random
from animation.colors import *
from bank_processes.authentication import Authentication, verify_data
from bank_processes.notification import Notification
from banking.register_panel import countdown_timer
from banking.main_menu import go_back, header, log_error
from banking.transfer_money import session_token, transaction_pin


notify = Notification()


def get_month(month: int) -> tuple[str, int]:
    """
    Generates the month name and days within that month according to the month number received.

    Args:
        month (int): The number of the month you want.

    Returns:
        tuple[str, int]: The name of the month and the number of days in that month.
    """

    while month > 12:
        month -= 12

    year = 2006

    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    days_in_month = {
        1: 31, 2: 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28,
        3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    month_name = month_names.get(month)
    days = days_in_month.get(month)

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
    elif 11 <= day <= 13:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')


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
    interest:   float = (principal * rate_per_year * days) / 36500

    rate_of_interest: float = (interest * 100) / principal

    return interest, rate_of_interest


def payback_date(current_year: int, current_month: int, current_day: int, start_day: int, end_day: int,
                 auth: Authentication, percentage_rate: float, deposit_amount: float):
    """
    Displays the list of days for the User to select their Payback date.

    Parameters
    ----------
    current_year : int
        The current year.
    current_month : int
        The current month.
    current_day : int
        The current day.
    start_day : int
        The start day of the user periodic choice.
    end_day : int
        The end day of the user periodic choice.
    auth : Authentication
        Contains the entire details of the user.
    percentage_rate : float
        The interest rate with respect to the start day and end day.
    deposit_amount : float
        The amount the user wants to deposit.
    """
    try:
        while True:
            header()  # Call the function to print the header.
            print(bold, brt_yellow, "\nChoose Payback Date")
            print(f"{magenta}~~~~~~~~~~~~~~~~~~~{end}\n")

            dates: dict = {}  # Dictionary to store the payback date options.
            start = start_day  # Initialize the start day for calculating dates.

            # Calculate the starting payback date.
            while start != 0:
                _month, _days = get_month(current_month)  # Get the current month and the number of days in it.
                current_day += 1
                start -= 1

                # Check if the current day exceeds the number of days in the month.
                if current_day > _days:
                    if current_month == 12:
                        current_year += 1
                        current_month = 0

                    current_month += 1
                    current_day = 1

            # Display the range of payback date options.
            for i, day in enumerate(range(start_day, end_day + 1)):
                # Calculate interest and rate of interest for each day.
                interest, rate_of_interest = calculate_interest(
                    principal=deposit_amount,
                    rate_per_year=percentage_rate,
                    days=day
                )

                _month, _days = get_month(current_month)  # Get the current month and the number of days in it.

                # Check if the current day exceeds the number of days in the month.
                if current_day > _days:
                    if current_month == 12:
                        current_month = 0
                        current_year += 1

                    current_month += 1
                    current_day = 1

                _month, _days = get_month(current_month)  # Get the updated month and the number of days in it.

                # Print the payback date option with the interest rate.
                print(f'{bold}{green}[{day}]{green} {magenta}-> {brt_yellow}{current_day}/{_month}/{current_year} {magenta}- {brt_yellow}{rate_of_interest:.2f}%{end}', end='\t\t\t\t\t')

                # Store the date information in the dictionary.
                dates[f'{day}'] = [
                    f'{rate_of_interest:.3f}%',
                    f'{interest:.3f}',
                    f'{current_day}{get_ordinal_suffix(current_day)} {_month} {current_year}',
                    f'{current_year}-{current_month}-{current_day}'
                ]

                current_day += 1  # Move to the next day.

                # Print a newline after every third option.
                if i % 3 == 2:
                    print()

            while True:
                print(bold, magenta, end='')
                _input = input("\n>>> ")  # Get user input.
                print(end, end='')

                # Check if the user wants to go back.
                if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                    del _input
                    time.sleep(1.5)
                    go_back('signed_in', auth=auth)
                    break
                else:
                    # Validate the user input.
                    if not _input.isdigit():
                        print(red, "\n:: Numbers Only", end)
                        del _input
                        time.sleep(3)
                        continue
                    elif start_day <= int(_input) <= end_day:
                        return dates[_input], f'{int(_input)} days', 'Beta Account Balance'
                    else:
                        print(red, "\n:: Wrong Input", end)
                        del _input
                        time.sleep(3)
                        continue
            break
    except Exception as e:
        log_error(error=e)
        go_back('signed_in', auth=auth)


def safelock(auth: Authentication) -> tuple[float, str]:
    """
    Filling the form for Amount to Deposit.

    Parameters
    ----------
    auth : Authentication
        Contains the entire details of the User.

    Returns
    -------
    tuple[float, str]
        Amount to be deposited and the deposition title.
    """
    try:
        while True:
            header()  # Display the header.
            print(bold, brt_yellow, "\nAmount to Deposit: (must be Greater than N1000)")
            print(magenta, "~~~~~~~~~~~~~~~~~~", sep='')

            deposit_amount = input(">>> ").strip()
            print(end, end='')

            # Check if the user wants to go back.
            if re.search('^.*(back|return).*$', deposit_amount, re.IGNORECASE):
                del deposit_amount
                time.sleep(1.5)
                go_back('signed_in', auth=auth)
                break
            else:
                # Validate the deposit amount input.
                if re.search("^[0-9]{0,30}[.]?[0-9]{0,2}$", deposit_amount, re.IGNORECASE) is None:
                    print(red, "\n:: Digits Only", end)
                    del deposit_amount
                    time.sleep(2)
                    continue
                elif float(deposit_amount) < 1000:
                    print(red, "\n:: Amount MUST be above N1000", end)
                    del deposit_amount
                    time.sleep(3)
                    continue
                else:
                    auth.amount = float(deposit_amount)
                    # Validate the transaction against the transfer limit.
                    if auth.transaction_validation(transfer_limit=True)[0]:
                        # Validate the transaction amount.
                        if auth.transaction_validation(amount=True)[0]:
                            auth.initial_deposit = float(deposit_amount)
                        else:
                            print(red, f"\n:: {auth.transaction_validation(amount=True)[1]}", end)
                            del deposit_amount
                            time.sleep(2)
                            continue
                    else:
                        print(red, f"\n:: {auth.transaction_validation(transfer_limit=True)[1]}", end)
                        del deposit_amount
                        time.sleep(3)
                        go_back('signed_in', auth=auth)
                        break

                    # Prompt for the title of the deposit.
                    while True:
                        header()
                        print(bold, brt_yellow, "\nTitle of Deposit")
                        print(magenta, "~~~~~~~~~~~~~~~~", sep='')

                        deposit_title = input(">>> ").strip()
                        print(end, end='')

                        # Check if the user wants to go back.
                        if re.search('^.*(back|return).*$', deposit_title, re.IGNORECASE):
                            del deposit_title
                            time.sleep(1.5)
                            go_back('signed_in', auth=auth)
                            break
                        else:
                            # Validate the length of the deposit title.
                            if len(deposit_title) > 29:
                                print(red, "\n:: Title can't be more than 30 characters", end)
                                del deposit_title
                                time.sleep(3)
                                continue
                            else:
                                return float(deposit_amount), deposit_title
    except Exception as e:
        # Log any exceptions to a file and navigate back to the main script.
        log_error(error=e)
        go_back('signed_in', auth=auth)


def preview_safelock(safelock_title: str, amount_to_lock: float, interest: str, interest_to_earn: float,
                     maturity_date: str, lock_duration: str, maturity_location: str, maturity_date_in_date: str,
                     auth: Authentication):
    """
    Previews the details of a Fixed Deposit before the Deposit is documented into the database.
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
            header()  # Display the header
            print(bold, brt_yellow, "\nPreview your Fixed Deposit slip")
            print(f"{magenta}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{end}\n")

            # Displaying details for the user to review
            print(bold, brt_yellow, 'Fixed Deposit Title', sep='')
            print(green, safelock_title, sep='')
            print(bold, brt_yellow, '\nInitial Deposit                             Interest')
            print(green, f'N{amount_to_lock}{' ' * (43 - len(str(amount_to_lock)))}{interest}', sep='')
            print(bold, brt_yellow, '\nInterest To Earn                            Maturity Date')
            print(green, f'N{interest_to_earn}{' ' * (43 - len(str(interest_to_earn)))}{maturity_date}', sep='')
            print(bold, brt_yellow, '\nLock Duration                               Matures Into Your')
            print(green, f'{lock_duration}{' ' * (44 - len(lock_duration))}{maturity_location}', sep='', end='\n\n')

            # Calculate and display the payback time
            if _time.hour > 12:
                payback_time = f'{(_time.hour - 12)}:{_time.minute} PM'
            else:
                payback_time = f'{_time.hour}:{_time.minute} AM'

            # Display an authorization message
            print(bold, brt_yellow, f'I authorize Console Beta Banking to SafeLock {amount_to_lock} immediately and return it in full on'
                  f'\nthe {maturity_date} by {payback_time} to my Beta Account Balance. \n'
                  f'I confirm and approve this transaction.', sep='')
            print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')
            print(f'{bold}{magenta}~~~~~~     ~~~~~')

            _input = input(">>> ").strip()
            print(end, end='')

            # Check if the user wants to go back
            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
                break
            else:
                if re.search('^(1|yes)$', _input, re.IGNORECASE):
                    print()
                    print(bold, brt_yellow, f'I hereby acknowledge that this Fixed Deposit Account CANNOT be broken once it has been '
                          f'created', sep='')
                    print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')
                    print(f'{bold}{magenta}~~~~~~     ~~~~~')

                    _input = input(">>> ").strip()
                    print(end, end='')
                    
                    if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                        del _input
                        time.sleep(1.5)
                        break
                    else:
                        if re.search('^(1|yes)$', _input, re.IGNORECASE):
                            transaction_pin(auth)  # Prompt user for transaction pin
                            session_token(auth)  # Generate a session token

                            countdown_timer(_register='fixed deposit', countdown=5)  # Show countdown timer

                            # Generate a unique deposit ID
                            _id = 'cbb' + str(random.randint(100000000, 999999999))
                            auth.deposit_id = _id
                            while verify_data('deposit_id', 4, _id):
                                _id = 'cbb' + str(random.randint(100000000, 999999999))
                                auth.deposit_id = _id

                            # Set various attributes of the auth object
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
                            auth.process_transaction(fixed_deposit=True)  # Process the transaction
                            auth.transaction_record(fixed_deposit=True)  # Record the transaction

                            note = f"""
Debit
Amount :: NGN{auth.amount:,.2f}
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

                            # Process the transaction whereby Fixed Interest is deposited into the account immediately
                            auth.description = f'FIXED_DEPOSIT/CBB/INTEREST DEPOSIT TO {auth.account_holder}'
                            auth.receiver_acct_num = auth.account_number
                            auth.amount = float(interest_to_earn)

                            auth.process_transaction(deposit=True)
                            auth.transaction_record(deposit=True)
                            auth.receiver_transaction_validation()

                            note = f"""
Credit
Amount :: NGN{auth.amount:,.2f}
Acc :: {auth.account_number[:3]}******{auth.account_number[-3:]}
Desc :: {auth.description}
Time :: {datetime.datetime.today().now().time()}
Balance :: {auth.account_balance}
                            """

                            # Trigger a deposit notification with the formatted note
                            notify.deposit_notification(
                                title='Console Beta Banking',
                                message=note,
                                channel='ConsoleBeta'
                            )

                            # Process the transaction whereby the Locked Amount is deposited into the Central Bank.
                            auth.description = f'FIXED_DEPOSIT/CBB/DEPOSIT TO CENTRAL BANK'
                            auth.receiver_acct_num = '1000000009'
                            auth.amount = float(amount_to_lock)

                            auth.process_transaction(central_bank=True)
                            auth.transaction_record(central_bank=True)

                            # Open the fixed deposit account
                            auth.open_fixed_deposit_account()

                            header()

                            print(green, f'\n:: Congrats. \n:: Fixed Deposit Successfully Created.', end)

                            notify.fixed_deposit_creation_notification(
                                title='Console Beta Banking',
                                message=f'Fixed Deposit Successfully Created.\nDeposit ID :: {auth.deposit_id}\n'
                                        f'Deposit Title :: {auth.deposit_title}'
                                        f'Deposit Amount :: {auth.initial_deposit:,.2f}',
                                channel='ConsoleBeta'
                            )

                            time.sleep(3)

                            break
                        elif re.search('^(2|no)$', _input, re.IGNORECASE):
                            del _input
                            time.sleep(1.5)
                            break
                        else:
                            print(red, "\n:: Wrong Input", end)
                            del _input
                            time.sleep(3)
                            continue
                elif re.search('^(2|no)$', _input, re.IGNORECASE):
                    del _input
                    time.sleep(1.5)
                    break
                else:
                    print(red, "\n:: Wrong Input", end)
                    del _input
                    time.sleep(3)
                    continue
    except Exception as e:
        # Log any exceptions to a file and navigate back to the main script
        log_error(error=e)
        go_back('signed_in', auth=auth)


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
        print(bold, brt_yellow, '\nMessage from the CUSTOMER SERVICE OFFICER:::')
        print(magenta, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', end, sep='')
        print(bold, brt_yellow, "'You want a new Fixed Deposit Account. Let's Create one for You.'", end, sep='')
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
            print(bold, brt_yellow, "\nHow long do you want to lock funds?")
            print(magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", sep='')
            print(f"{green}[1]{green} {magenta}-: {brt_yellow}10 - 30 days\t\t\t\t\tat {magenta}~ {brt_yellow}8% p.a")
            print(f"{green}[2]{green} {magenta}-: {brt_yellow}31 - 60 days\t\t\t\t\tat {magenta}~ {brt_yellow}9% p.a")
            print(f"{green}[3]{green} {magenta}-: {brt_yellow}61 - 90 days\t\t\t\t\tat {magenta}~ {brt_yellow}11% p.a")
            print(f"{green}[4]{green} {magenta}-: {brt_yellow}91 - 180 days\t\t\t\t\tat {magenta}~ {brt_yellow}11.5% p.a")
            print(f"{green}[5]{green} {magenta}-: {brt_yellow}181 - 270 days\t\t\t\t\tat {magenta}~ {brt_yellow}13.5% p.a")
            print(f"{green}[6]{green} {magenta}-: {brt_yellow}271 - 365 days\t\t\t\t\tat {magenta}~ {brt_yellow}14% p.a")
            print(f"{green}[7]{green} {magenta}-: {brt_yellow}Above 1 - 2 years\t\t\t\tat {magenta}~ {brt_yellow}14.5% p.a")
            print(f"{green}[8]{green} {magenta}-: {brt_yellow}Above 2 years\t\t\t\t\tat {magenta}~ {brt_yellow}15% p.a")

            print(bold, magenta, end='')
            _input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                time.sleep(1.5)
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
                print(red, "\n:: Wrong Input", end)
                time.sleep(2)
    except Exception as e:
        log_error(error=e)
        go_back('signed_in', auth=auth)


days_left: int = 0
deposit_id, deposit, interest_earned = ('', 0.0, 0.0)
upfront_interest = 0


def top_up_deposit(auth: Authentication, pay_back_date: str, pay_back_time: time):
    """Allows the user to top up an existing Fixed Deposit with additional funds.

    Parameters
    ----------
    auth : Authentication
        Contains the entire details of the User.
    pay_back_date : str
        The date when the deposit will mature.
    pay_back_time : time
        The time of day when the deposit will mature.
    """
    try:
        global days_left
        global deposit_id, deposit, interest_earned
        global upfront_interest

        while True:
            # Duration options mapping to their respective upfront interest rates
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

            # Determine the upfront interest rate based on the days left
            for key, value in duration_options.items():
                if value[0] <= days_left <= value[1]:
                    upfront_interest = value[2]
                elif 10 > days_left:
                    upfront_interest = 8

            header()

            print(bold, brt_yellow, "\nAmount to Deposit: (must be Greater than N1000)")
            print(magenta, "~~~~~~~~~~~~~~~~~~", sep='')

            deposit_amount = input(">>> ").strip()
            print(end, end='')

            # Check for back or return commands
            if re.search('^.*(back|return).*$', deposit_amount, re.IGNORECASE):
                del deposit_amount
                time.sleep(1.5)
                break
            else:
                # Check for invalid input
                if not deposit_amount.isdigit() or float(deposit_amount) < 1000:
                    print(red, "\n:: Amount MUST be above N1000 and should be a valid number", end)
                    time.sleep(3)
                    continue
                else:
                    auth.amount = float(deposit_amount)
                    # Validate transaction limits and amounts
                    if not auth.transaction_validation(transfer_limit=True)[0]:
                        print(red, f"\n:: {auth.transaction_validation(transfer_limit=True)[1]}", end)
                        time.sleep(3)
                        break

                    if not auth.transaction_validation(amount=True)[0]:
                        print(red, f"\n:: {auth.transaction_validation(amount=True)[1]}", end)
                        time.sleep(2)
                        continue

                    auth.initial_deposit = float(deposit_amount)
                    # Calculate interest
                    interest, rate_of_interest = calculate_interest(auth.initial_deposit, upfront_interest, days_left)

                    # Display calculated interest and confirmation prompt
                    print(bold, brt_yellow, f"\nYou will earn an upfront interest of {rate_of_interest:.2f}% on any amount you add into "
                          f"\nthis Fixed Deposit, because it has {days_left} days left. Safelock can't be broken, and "
                          f"\nfunds in this particular Safelock can't be accessed until {pay_back_date} "
                          f"by {pay_back_time}.\n")

                    print(f"You will earn N {interest:,.2f} upfront interest on your {auth.initial_deposit:,} naira "
                          f"addition to this Safelock")

                    print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')
                    print(f'{bold}{magenta}~~~~~~     ~~~~~')

                    _input = input(">>> ").strip()
                    print(end, end='')

                    if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                        del _input
                        time.sleep(1.5)
                        break
                    elif re.search('^(1|yes)$', _input, re.IGNORECASE):
                        # Update deposit details and process transaction
                        auth.initial_deposit += float(deposit)
                        auth.total_interest_earned = float(interest_earned) + interest

                        _id = 'cbb' + str(random.randint(100000000, 999999999))
                        auth.deposit_id = _id
                        while verify_data('deposit_id', 4, _id):
                            _id = 'cbb' + str(random.randint(100000000, 999999999))
                            auth.deposit_id = _id

                        auth.description = f'FIXED_DEPOSIT/CBB/{auth.deposit_id}/TOP UP DEPOSIT'
                        auth.process_transaction(fixed_deposit=True)
                        auth.transaction_record(fixed_deposit=True)

                        note = f"""
Debit
Amount :: NGN{auth.amount:,.2f}
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

                        # Process the transaction whereby Fixed Interest is deposited into the account immediately
                        auth.description = f'FIXED_DEPOSIT/CBB/INTEREST DEPOSIT TO {auth.account_holder}'
                        auth.receiver_acct_num = auth.account_number
                        auth.amount = float(interest)

                        auth.process_transaction(deposit=True)
                        auth.transaction_record(deposit=True)
                        auth.receiver_transaction_validation()

                        note = f"""
Credit
Amount :: NGN{auth.amount:,.2f}
Acc :: {auth.account_number[:3]}******{auth.account_number[-3:]}
Desc :: {auth.description}
Time :: {datetime.datetime.today().now().time()}
Balance :: {auth.account_balance}
                        """

                        # Trigger a deposit notification with the formatted note
                        notify.deposit_notification(
                            title='Console Beta Banking',
                            message=note,
                            channel='ConsoleBeta'
                        )

                        # Process the transaction whereby the Locked Amount is deposited into the Central Bank.
                        auth.description = f'FIXED_DEPOSIT/CBB/DEPOSIT TO CENTRAL BANK'
                        auth.receiver_acct_num = '1000000009'
                        auth.amount = float(auth.initial_deposit)

                        auth.process_transaction(central_bank=True)
                        auth.transaction_record(central_bank=True)

                        auth.update_deposit(deposit_id)

                        countdown_timer(_register='Top Up', _duty='deposit', countdown=5)

                        header()
                        print(green, "\n:: Deposit Successfully Topped Up.", end)

                        notify.fixed_deposit_top_up_notification(
                            title='Console Beta Banking',
                            message=f'Deposit Successfully Topped Up.\nDeposit ID :: {auth.deposit_id}\n'
                                    f'Deposit Amount :: {auth.initial_deposit:,.2f}',
                            channel='ConsoleBeta'
                        )

                        time.sleep(2)
                        break
                    elif re.search('^(2|no)$', _input, re.IGNORECASE):
                        time.sleep(1)
                        break
                    else:
                        print(red, "\n:: Wrong Input", end)
                        del _input
                        time.sleep(3)
                        continue
    except Exception as e:
        log_error(error=e)
        go_back('signed_in', auth=auth)


def ongoing_display_deposits(auth: Authentication, data: list, _details: list, _key: int):
    """ Displays details of a specific ongoing deposit

    Parameters
    ----------
    auth : Authentication
        Contains the entire details of the User.
    data : list
        Contains the details of the Deposit in a database format
    _details : list
        Contains the details of the Deposit in a structured pictorial format
    _key : int
        Number of the selected Deposit
    """
    try:
        # Extract the payback time for the selected deposit
        payback_time: datetime.time = data[_key][8]

        # Extract the start and payback dates
        start_day = data[_key][6].day
        payback_day = data[_key][7].day
        start_suffix = get_ordinal_suffix(start_day)
        payback_suffix = get_ordinal_suffix(payback_day)

        # Format the start and payback dates
        start_date = f'{start_day}{start_suffix} {get_month(data[_key][6].month)[0]} {data[_key][6].year}'
        payback_date = f'{payback_day}{payback_suffix} {get_month(data[_key][7].month)[0]} {data[_key][7].year}'

        while True:
            header()

            # Display the details in a structured format
            print('\n', _details[_key], sep='')

            print(bold, brt_yellow, f"\n                 FIXED DEPOSIT DETAILS                    ", end, sep='')
            print(bold, magenta, f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+", sep='')
            print(f'| {brt_yellow}Initial Deposit                  Total Interest Earned {magenta}|')
            print(
                f'| {green}N{data[_key][3]}{" " * (32 - len(str(data[_key][3])))}N{data[_key][5]}'
                f'{" " * (21 - len(str(data[_key][5])))}{magenta}|')
            print(f"|                                                        |")
            print(f'| {brt_yellow}Start Date                       Payback Date          {magenta}|')
            print(f'| {green}{start_date}{" " * (33 - len(start_date))}{payback_date}{" " * (22 - len(payback_date))}{magenta}|')
            print(f"|                                                        |")
            print(f'| {brt_yellow}Payback Time                     Safelock ID           {magenta}|')
            print(f'| {green}{payback_time}{" " * (33 - 8)}{data[_key][0]}{" " * (22 - len(data[_key][0]))}{magenta}|')
            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+\n')

            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|      {brt_black_bg}{brt_yellow}1. TOP UP DEPOSIT{end}      {bold}{magenta}|        {brt_black_bg}{brt_yellow}2. RETURN{end}         {bold}{magenta}|')
            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', user_input.strip().lower()):
                pass
            elif re.search('^1$', user_input):
                top_up_deposit(auth, payback_date, payback_time)
                break
            elif re.search('^2$', user_input):
                break
            else:
                print(red, "\n:: Digits only.", end)
                time.sleep(2)
                continue

    except Exception as e:
        log_error(error=e)
        go_back('signed_in', auth=auth)


def paid_display_deposits(data: list, _details: list, _key: int):
    """ Displays details of a specific paid-back deposit

    Parameters
    ----------
    data : list
        Contains the details of the Deposit in a database format
    _details : list
        Contains the details of the Deposit in a structured pictorial format
    _key : int
        Number of the selected Deposit
    """
    try:
        # Extract the payback time for the selected deposit
        payback_time: datetime.time = data[_key][8]

        # Extract the start and payback dates
        start_day = data[_key][6].day
        payback_day = data[_key][7].day
        start_suffix = get_ordinal_suffix(start_day)
        payback_suffix = get_ordinal_suffix(payback_day)

        # Format the start and payback dates
        start_date = f'{start_day}{start_suffix} {get_month(data[_key][6].month)[0]} {data[_key][6].year}'
        payback_date = f'{payback_day}{payback_suffix} {get_month(data[_key][7].month)[0]} {data[_key][7].year}'

        while True:
            header()

            # Display the details in a structured format
            print('\n', _details[_key], sep='')

            print(bold, brt_yellow, f"\n                 FIXED DEPOSIT DETAILS                    ", end, sep='')
            print(bold, magenta, f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+", sep='')
            print(f'| {brt_yellow}Initial Deposit                  Total Interest Earned {magenta}|')
            print(
                f'| {green}N{data[_key][3]}{" " * (32 - len(str(data[_key][3])))}N{data[_key][5]}'
                f'{" " * (21 - len(str(data[_key][5])))}{magenta}|')
            print(f"|                                                        |")
            print(f'| {brt_yellow}Start Date                       Payback Date          {magenta}|')
            print(f'| {green}{start_date}{" " * (33 - len(start_date))}{payback_date}{" " * (22 - len(payback_date))}{magenta}|')
            print(f"|                                                        |")
            print(f'| {brt_yellow}Payback Time                     Safelock ID           {magenta}|')
            print(f'| {green}{payback_time}{" " * (33 - 8)}{data[_key][0]}{" " * (22 - len(data[_key][0]))}{magenta}|')
            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+\n')

            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|                       {brt_black_bg}{brt_yellow}1. RETURN{end}                        {bold}{magenta}|')
            print(f'+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', user_input.strip().lower()):
                break
            elif re.search('^(1|return)$', user_input):
                break
            else:
                print(red, "\n:: Digits only.", end)
                time.sleep(2)
                continue
    except Exception as e:
        log_error(error=e)
        go_back('script')


def ongoing_deposits(auth: Authentication):
    """ Displays the User's fixed deposits that are still running active.

    Parameters
    ----------
    auth : Authentication
        Contains the entire details of the User.
    """
    try:
        while True:
            # Fetch active (ongoing) deposit details
            data, balance, days, days_remaining = auth.get_active()
            details = []
            global days_left
            global deposit_id, deposit, interest_earned

            header()

            print(bold, brt_yellow, "\nONGOING DEPOSITS")
            print(f"{magenta}~~~~~~~~~~~~~~~~{end}\n")

            if data:
                for key, value in enumerate(data):
                    # Determine space based on length of days_remaining
                    space = '  ' if len(str(days_remaining[key])) == 2 else ' ' if len(
                        str(days_remaining[key])) == 3 else '   '

                    # Calculate progress bar lengths
                    bar_length = 46
                    progress_length = 0 if days_remaining[key] == 0 else bar_length // days[key]
                    progress = progress_length * (days[key] - days_remaining[key])
                    remaining = bar_length - progress
                    if days_remaining[key] == 0:
                        progress, remaining = 46, 0

                    # Format each deposit detail for display
                    detail = (f"{bold}{magenta}+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+\n"
                              f"|                                                              |\n"
                              f"|   {brt_yellow}{key + 1}. {data[key][2]}{' ' * (47 - len(str(data[key][2])))}         {magenta}|\n"
                              f"|      {green}N{data[key][3]:,}{' ' * (48 - len(str(data[key][3])))}      {magenta}|\n"
                              f"|      {brt_yellow}Locked{' ' * (50 - len('locked'))}      {magenta}|\n"
                              f"|                                                              |\n"
                              f"| {brt_blue_bg}{' ' * progress}{brt_white_bg}{' ' * remaining}{end} "
                              f"{bold}{brt_yellow}{days_remaining[key]} days left{space}{magenta}|\n"
                              f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+{end}")

                    details.append(detail)
                    print(detail, '\n')

                # Get user input
                print(bold, magenta, end='')
                user_input = input(">>> ").strip()
                print(end, end='')

                if re.search('^.*(back|return).*$', user_input.strip().lower()):
                    break  # Go back to the previous menu
                elif user_input.isdigit():
                    user_selection = int(user_input)
                    if user_selection > len(data):
                        print(red, "\n:: Digits within the list only", end)
                        time.sleep(2)
                    else:
                        days_left = days_remaining[user_selection - 1]
                        deposit_id, deposit, interest_earned = (
                            data[user_selection - 1][0], data[user_selection - 1][3], data[user_selection - 1][5])
                        ongoing_display_deposits(auth, data, details, user_selection - 1)
                        continue
                else:
                    print(red, "\n:: Digits only.", end)
                    time.sleep(2)
            else:
                print(green, "\n:: You don't have any Ongoing Deposit", end)
                time.sleep(5)
                break
    except Exception as e:
        log_error(error=e)
        go_back('signed_in', auth=auth)


def paid_back_deposits(auth: Authentication):
    """ Displays the deposits that have been completed and returned to the User.

    Parameters
    ----------
    auth : Authentication
          Contains the entire details of the User.
    """
    try:
        # Fetch inactive (paid back) deposit details
        data = auth.get_inactive()
        details = []

        while True:
            header()

            print(bold, brt_yellow, "\nPAID BACK DEPOSITS")
            print(f"{magenta}~~~~~~~~~~~~~~~~~~{end}\n")

            if data:
                for key, value in enumerate(data):
                    # Format each deposit detail for display
                    detail = (f"{bold}{magenta}+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+\n"
                              f"|                                                         |\n"
                              f"|   {brt_yellow}{key + 1}. {data[key][2]}{' ' * (47 - len(str(data[key][2])))}    {magenta}|\n"
                              f"|      {brt_yellow}N{data[key][3]:,}{' ' * (48 - len(str(data[key][3])))} {magenta}|\n"
                              f"|      {brt_yellow}Unlocked{' ' * (50 - len('Unlocked'))} {magenta}|\n"
                              f"|                                                         |\n"
                              f"| {brt_blue_bg}{' ' * 48} {end}  Paid {magenta}|\n"
                              f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+{end}")

                    details.append(detail)
                    print(detail, '\n')

                # Get user input
                print(bold, magenta, end='')
                user_input = input(">>> ").strip()
                print(end, end='')

                if re.search('^.*(back|return).*$', user_input.strip().lower()):
                    break  # Go back to the previous menu
                elif user_input.isdigit():
                    user_selection = int(user_input)
                    if user_selection > len(data):
                        print(red, "\n:: Digits within the list only", end)
                        time.sleep(2)
                    else:
                        paid_display_deposits(data, details, user_selection - 1)
                else:
                    print(red, "\n:: Digits only.", end)
                    time.sleep(2)
            else:
                print(red, "\n:: You don't have any Paid Back Deposit", end)
                time.sleep(3.5)
                break
    except Exception as e:
        log_error(error=e)
        go_back('signed_in', auth=auth)


def access_safelock(auth: Authentication):
    """ To display the homepage for a fixed deposit user, providing options to view balance, ongoing deposits,
    paid back deposits, and create new fixed deposits.

    Parameters
    ---------
    auth : Authentication
          Contains the entire details of the User.
    """
    try:
        # Fetch active fixed deposit details
        data, balance, days, days_remaining = auth.get_active()
        sl_balance = f'N{balance:,.2f}'  # Format the balance for display
        eye = 'HIDE'  # Initial state to show the balance

        while True:
            # Display the header and fixed deposit information
            header()
            print(f"{bold}{brt_black_bg}{brt_red}\n8% - 15% per annum{end}")

            print(f"{bold}{brt_black_bg}{brt_yellow}")
            print(f"Fixed Deposit Balance{end}")

            print(f'{bold}{green}{sl_balance}\n')
            print(f"{magenta}+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print(f"|                   {brt_black_bg}{brt_yellow}1. {eye} BALANCE{end}                       {bold}{magenta}|")
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print(f"|    {brt_black_bg}{brt_yellow}2. ONGOING DEPOSITS{end}    {bold}{magenta}|    {brt_black_bg}{brt_yellow}3. PAID BACK DEPOSITS{end}    {bold}{magenta}|")
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            print(f"|              {brt_black_bg}{brt_yellow}4. CREATE A NEW FIXED DEPOSIT{end}              {bold}{magenta}|")
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

            # Get user input
            user_input = input(">>> ").strip()
            print(end, end='')

            if re.search('^1$', user_input):
                # Toggle balance visibility
                if eye == 'SHOW':
                    eye = 'HIDE'
                    sl_balance = f'N{balance:,.2f}'  # Show balance
                else:
                    sl_balance = ' * * * * *'  # Hide balance
                    eye = 'SHOW'
                continue
            elif re.search('^2$', user_input):
                ongoing_deposits(auth)  # View ongoing deposits
                continue
            elif re.search('^3$', user_input):
                paid_back_deposits(auth)  # View paid back deposits
                continue
            elif re.search('^4$', user_input):
                create_safelock(auth)  # Create a new fixed deposit
                continue
            elif re.search('^.*(back|return).*$', user_input.strip().lower()):
                pass  # Go back to the signed-in menu
            else:
                print(red, "\n:: Invalid input, please try again.", end)
                time.sleep(2)
                continue
            break  # Exit loop after handling the input
    except Exception as e:
        log_error(error=e)
        go_back('signed_in', auth=auth)
