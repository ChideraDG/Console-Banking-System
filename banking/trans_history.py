import re
import time
from datetime import datetime, date
from typing import Tuple, Any
from bank_processes.authentication import Authentication
from banking.main_menu import log_error, go_back, header
from animation.colors import *
from banking.register_panel import countdown_timer


def get_month_details(month_of_birth: int):
    """
    Returns the month name and the number of days in that month for a given year.

    Parameters
    ----------
    month_of_birth : int
        The month number (1 for January, 2 for February, etc.).

    Returns
    -------
    tuple
        A tuple containing the name of the month and the number of days in that month.
    """

    # Dictionary mapping month numbers to tuples of (month name, number of days)
    months = {
        1: ('January', 31),
        2: ('February', 29 if (2006 % 4 == 0 and 2006 % 100 != 0) or (2006 % 400 == 0) else 28),
        3: ('March', 31),
        4: ('April', 30),
        5: ('May', 31),
        6: ('June', 30),
        7: ('July', 31),
        8: ('August', 31),
        9: ('September', 30),
        10: ('October', 31),
        11: ('November', 30),
        12: ('December', 31)
    }

    # Retrieve and return the tuple (month name, number of days) for the given month
    return months[month_of_birth]


def by_date(*, current_year) -> str | tuple[str, str]:
    """
    Get start and end dates from the user for a specific time frame.

    Parameters
    ----------
    current_year : int
        The current year to validate the input year.

    Returns
    -------
    tuple of str
        A tuple containing start and end dates in 'YYYY-MM-DD' format if successful.
    str
        'break' if the user opts to return at any point.
    """
    try:
        def get_dates(title: str) -> str:
            """
            Get date input from the user.

            Parameters
            ----------
            title : str
                'start' or 'end' to specify the date type.

            Returns
            -------
            str
                The date in 'YYYY-MM-DD' format or 'break' if the user opts to return.
            """
            header()  # Call the header function to display the header.

            print(bold, brt_yellow, f"\n{title.upper()} DATE:")
            print(magenta, f"~~~~~~{'~' * len(title)}", end, sep='')

            while True:
                # Get the year from the user.
                print(bold, brt_yellow, "\nInput the Year:")
                print(magenta, "~~~~~~~~~~~~~~~", sep='')

                year = input(">>> ").strip()
                print(end, end='')

                if re.search('^.*(back|return).*$', year, re.IGNORECASE):
                    return 'break'  # If the user types 'back' or 'return', break the loop.
                if year.isdigit() and 1900 < int(year) <= current_year:
                    break
                else:
                    if not year.isdigit():
                        print(red, f"\n:: {title.title()} Year should be in digits.\nExample: 2001, 2004, etc.", end)
                    elif int(year) <= 1900:
                        print(red, "\n:: Invalid input\n:: Year is less than 1900", end)
                    elif int(year) > current_year:
                        print(red, f"\n:: Invalid input\n:: Year is greater than {current_year}", end)
                    time.sleep(2)

            while True:
                # Get the month from the user.
                print(bold, brt_yellow, "\nInput the Month:")
                print(magenta, "~~~~~~~~~~~~~~~~", sep='')

                month = input(">>> ").strip()
                print(end, end='')

                if re.search('^.*(back|return).*$', month, re.IGNORECASE):
                    return 'break'  # If the user types 'back' or 'return', break the loop.
                if month.isdigit():
                    if year == str(current_year):
                        current_month = datetime.today().month  # Get the current month.
                    else:
                        current_month = 12  # Set to December for past years.
                    if 0 < int(month) <= current_month:
                        break
                    else:
                        if not 0 < int(month):
                            print(red, "\n:: Invalid input\n:: Month is less than 1", end)
                        elif int(month) > current_month:
                            print(red, f"\n:: Invalid input\n:: Month is greater than {current_month}", end)
                else:
                    print(red, f"\n:: {title.title()} Month should be in digits.\nExample: 1, 4, etc.", end)
                time.sleep(2)

            while True:
                # Get the day from the user.
                print(bold, brt_yellow, "\nInput the Day:")
                print(magenta, "~~~~~~~~~~~~~~", sep='')

                day = input(">>> ").strip()
                print(end, end='')

                if re.search('^.*(back|return).*$', day, re.IGNORECASE):
                    return 'break'  # If the user types 'back' or 'return', break the loop.
                if day.isdigit():
                    if year == str(current_year):
                        current_day = datetime.today().day  # Get the current day.
                    else:
                        current_day = get_month_details(int(month))[1]  # Get the number of days in the month.
                    if 0 < int(day) <= current_day:
                        break
                    else:
                        print(red, f"\n:: Day of Birth should be within the number of days in "
                              f"{get_month_details(int(month))[0]} in {year}.", end)
                else:
                    print(red, f"\n:: {title.title()} Day should be in digits.\nExample: 1, 4, etc.", end)
                time.sleep(2)

            return f'{year}-{month}-{day}'  # Return the date in 'YYYY-MM-DD' format.

        start_date = get_dates('start')  # Get the start date from the user.
        if start_date == 'break':
            return 'break'  # If 'break' is returned, exit the function.

        end_date = get_dates('end')  # Get the end date from the user.
        if end_date == 'break':
            return 'break'  # If 'break' is returned, exit the function.

        if (date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]),
                 day=int(start_date.split('-')[2])) >
                date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]),
                     day=int(end_date.split('-')[2]))):
            print(red, "\n:: Start Date cannot be greater than End Date", end)
            time.sleep(2)

            by_date(current_year=datetime.today().year)  # Retry getting dates.

        return start_date, end_date  # Return the start and end dates.
    except Exception as e:
        log_error(e)  # Log any exceptions.
        go_back('script')  # Return to the main menu.


def by_month(*, current_year: int) -> str | tuple[int, Any]:
    """
    Get a specific month and year from the user.

    Parameters
    ----------
    current_year : int
        The current year to validate the input year.

    Returns
    -------
    tuple of (int, str)
        A tuple containing the year and the name of the month if successful.
    str
        'break' if the user opts to return at any point.
    """
    try:
        header()  # Call the header function to display the header.

        print(bold, brt_yellow, "\nYEAR AND MONTH TIME FRAME")
        print(magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~", end, sep='')

        while True:
            # Get the year from the user.
            print(bold, brt_yellow, "\nInput the Year of the Month:")
            print(magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~", sep='')

            year = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', year, re.IGNORECASE):
                return 'break'  # If the user types 'back' or 'return', break the loop.
            if year.isdigit() and 1900 < int(year) <= current_year:
                break  # If the year is valid, break the loop.
            else:
                if not year.isdigit():
                    print(red, f"\n:: Year should be in digits.\nExample: 2001, 2004, etc.", end)
                elif int(year) <= 1900:
                    print(red, "\n:: Invalid input\n:: Year is less than 1900", end)
                elif int(year) > current_year:
                    print(red, f"\n:: Invalid input\n:: Year is greater than {current_year}", end)
                time.sleep(2)

        while True:
            # Get the month from the user.
            print("\nInput the Month:")
            print("~~~~~~~~~~~~~~~~")
            month = input(">>> ").strip()

            if re.search('^.*(back|return).*$', month, re.IGNORECASE):
                return 'break'  # If the user types 'back' or 'return', break the loop.
            if month.isdigit():
                if year == str(current_year):
                    current_month = datetime.today().month  # Get the current month.
                else:
                    current_month = 12  # Set to December for past years.
                if 0 < int(month) <= current_month:
                    break  # If the month is valid, break the loop.
                else:
                    if not 0 < int(month):
                        print(red, "\n:: Invalid input\n:: Month is less than 1", end)
                    elif int(month) > current_month:
                        print(red, f"\n:: Invalid input\n:: Month is greater than {current_month}", end)
            else:
                print(red, f"\n:: Month should be in digits.\nExample: 1, 4, etc.", end)
            time.sleep(2)

        return int(year), get_month_details(int(month))[0]  # Return the year and month name.
    except Exception as e:
        log_error(e)  # Log any exceptions.
        go_back('script')  # Return to the previous menu.


def process_transaction_history(*, auth: Authentication, criteria: str = 'all', start_date: str = None,
                                end_date: str = None, month: str = None, year: int = None):
    """
    Process and display transaction history based on given criteria.

    Parameters
    ----------
    auth : Authentication
        The authentication object for accessing transaction history.
    criteria : str
        The criteria for fetching the transaction history ('all', 'date', 'month').
    start_date : str, optional
        The start date for the 'date' criteria.
    end_date : str, optional
        The end date for the 'date' criteria.
    month : str, optional
        The month name for the 'month' criteria.
    year : int, optional
        The year for the 'month' criteria.
    """
    while True:
        header()  # Call the header function to display the header.
        print()  # Print a blank line for spacing.

        trans = None
        if criteria == 'date':
            trans = auth.transaction_history(
                start_date=datetime(int(start_date.split('-')[0]), int(start_date.split('-')[1]),
                                    int(start_date.split('-')[2]), 0, 0, 0),
                end_date=datetime(int(end_date.split('-')[0]), int(end_date.split('-')[1]),
                                  int(end_date.split('-')[2]), 23, 59, 59), time_period=True)

            if trans is True:
                print(green, ":: You don't have any transaction within this time frame.", end, sep='')
                time.sleep(5)  # Wait for 5 seconds before continuing.
                break

        elif criteria == 'month':
            trans = auth.transaction_history(month=month, year=year, is_month=True)

            if trans is True:
                print(green, f":: You don't have any transaction in the month of {month.title()}, {year}", end, sep='')
                time.sleep(5)  # Wait for 5 seconds before continuing.
                break

        elif criteria == 'all':
            trans = auth.transaction_history()
            if trans is True:
                print(green, ":: You don't have any transaction on your account.", end, sep='')
                time.sleep(5)  # Wait for 5 seconds before continuing.
                break

        countdown_timer(_register='\rGetting your', _duty='Transaction History', countdown=5)
        header()

        print(bold, brt_yellow, "\nTransaction History")
        print(f"{magenta}~~~~~~~~~~~~~~~~~~~{end}\n")

        print(trans)  # Print the transaction history.
        time.sleep(3)  # Wait for 3 seconds before continuing.

        print(green, end='')
        input("\nTO RETURN -+- PRESS ENTER  ")  # Prompt the user to press Enter to return.
        print(end, end='')
        break


def transaction_history(auth: Authentication):
    """
    Display the menu for selecting transaction history criteria and process the selection.

    Parameters
    ----------
    auth : Authentication
        The authentication object for accessing transaction history.
    """
    try:
        while True:
            header()  # Call the header function to display the header.

            print(bold, brt_yellow, '\nChoose a Criteria:')
            print(magenta, '~~~~~~~~~~~~~~~~~~', sep='')
            print("\n+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")
            print(f"|     {brt_black_bg}{brt_yellow}1. BY DATE{end}     {bold}{magenta}|     {brt_black_bg}{brt_yellow}2. BY MONTH{end}     {bold}{magenta}|")
            print("+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")
            print(f"|         {brt_black_bg}{brt_yellow}3. ALL TRANSACTION HISTORY{end}       {bold}{magenta}|")
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

            user_input = input(">>> ").strip()  # Prompt user input and strip whitespace.
            print(end, end='')

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                time.sleep(1)  # Wait for 1 second before breaking.
                break
            elif re.search('^1$', user_input):
                dates = by_date(current_year=datetime.today().year)  # Get the start and end dates.
                if dates == 'break':
                    continue  # Continue to the next iteration if 'break' is returned.

                process_transaction_history(
                    auth=auth,
                    criteria='date',
                    start_date=dates[0],
                    end_date=dates[1]
                )
                break

            elif re.search('^2$', user_input):
                month = by_month(current_year=datetime.today().year)  # Get the year and month.
                if month == 'break':
                    continue  # Continue to the next iteration if 'break' is returned.

                process_transaction_history(
                    auth=auth,
                    criteria='month',
                    month=month[1],
                    year=month[0]
                )
                break

            elif re.search('^3$', user_input):
                process_transaction_history(auth=auth)  # Get all transaction history.
                break

            else:
                print(red, "\n:: Invalid input, please try again.", end)
                time.sleep(2)  # Wait for 2 seconds before retrying.

    except Exception as e:
        log_error(e)  # Log any exceptions.
        go_back('signed_in', auth=auth)  # Return to the previous menu.

