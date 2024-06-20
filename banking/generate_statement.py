import re
import time
from datetime import datetime, date
from typing import Any
from bank_processes.authentication import Authentication
from bank_processes.notification import Notification
from banking.register_panel import countdown_timer
from banking.script import header, log_error, go_back, findDate


notify = Notification()


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

            print(f"\n{title.upper()} DATE:")  # Print the title in uppercase.
            print(f"~~~~~~{'~' * len(title)}")  # Print a decorative line.

            while True:
                # Get the year from the user.
                print("\nInput the Year:")
                print("~~~~~~~~~~~~~~~")
                year = input(">>> ").strip()  # Prompt user input and strip whitespace.

                if re.search('^.*(back|return).*$', year, re.IGNORECASE):
                    return 'break'  # If the user types 'back' or 'return', break the loop.
                if year.isdigit() and 1900 < int(year) <= current_year:
                    break  # If the year is valid, break the loop.
                else:
                    if not year.isdigit():
                        print(f"\n:: {title.title()} Year should be in digits.\nExample: 2001, 2004, etc.")
                    elif int(year) <= 1900:
                        print("\n:: Invalid input\n:: Year is less than 1900")
                    elif int(year) > current_year:
                        print(f"\n:: Invalid input\n:: Year is greater than {current_year}")
                    time.sleep(2)  # Wait for 2 seconds before retrying.

            while True:
                # Get the month from the user.
                print("\nInput the Month:")
                print("~~~~~~~~~~~~~~~~")
                month = input(">>> ").strip()  # Prompt user input and strip whitespace.

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
                            print("\n:: Invalid input\n:: Month is less than 1")
                        elif int(month) > current_month:
                            print(f"\n:: Invalid input\n:: Month is greater than {current_month}")
                else:
                    print(f"\n:: {title.title()} Month should be in digits.\nExample: 1, 4, etc.")
                time.sleep(2)  # Wait for 2 seconds before retrying.

            while True:
                # Get the day from the user.
                print("\nInput the Day:")
                print("~~~~~~~~~~~~~~")
                day = input(">>> ").strip()  # Prompt user input and strip whitespace.

                if re.search('^.*(back|return).*$', day, re.IGNORECASE):
                    return 'break'  # If the user types 'back' or 'return', break the loop.
                if day.isdigit():
                    if year == str(current_year):
                        current_day = datetime.today().day  # Get the current day.
                    else:
                        current_day = get_month_details(int(month))[1]  # Get the number of days in the month.
                    if 0 < int(day) <= current_day:
                        break  # If the day is valid, break the loop.
                    else:
                        print(f"\n:: Day of Birth should be within the number of days in "
                              f"{get_month_details(int(month))[0]} in {year}.")
                else:
                    print(f"\n:: {title.title()} Day should be in digits.\nExample: 1, 4, etc.")
                time.sleep(2)  # Wait for 2 seconds before retrying.

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
            print("\n:: Start Date cannot be greater than End Date")
            time.sleep(2)  # Wait for 2 seconds before retrying.

            by_date(current_year=datetime.today().year)  # Retry getting dates.

        return start_date, end_date  # Return the start and end dates.
    except Exception as e:
        log_error(e)  # Log any exceptions.
        go_back('script')  # Return to the previous menu.


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

        print("\nYEAR AND MONTH TIME FRAME")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")

        while True:
            # Get the year from the user.
            print("\nInput the Year of the Month:")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            year = input(">>> ").strip()  # Prompt user input and strip whitespace.

            if re.search('^.*(back|return).*$', year, re.IGNORECASE):
                return 'break'  # If the user types 'back' or 'return', break the loop.
            if year.isdigit() and 1900 < int(year) <= current_year:
                break  # If the year is valid, break the loop.
            else:
                if not year.isdigit():
                    print(f"\n:: Year should be in digits.\nExample: 2001, 2004, etc.")
                elif int(year) <= 1900:
                    print("\n:: Invalid input\n:: Year is less than 1900")
                elif int(year) > current_year:
                    print(f"\n:: Invalid input\n:: Year is greater than {current_year}")
                time.sleep(2)  # Wait for 2 seconds before retrying.

        while True:
            # Get the month from the user.
            print("\nInput the Month:")
            print("~~~~~~~~~~~~~~~~")
            month = input(">>> ").strip()  # Prompt user input and strip whitespace.

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
                        print("\n:: Invalid input\n:: Month is less than 1")
                    elif int(month) > current_month:
                        print(f"\n:: Invalid input\n:: Month is greater than {current_month}")
            else:
                print(f"\n:: Month should be in digits.\nExample: 1, 4, etc.")
            time.sleep(2)  # Wait for 2 seconds before retrying.

        return int(year), get_month_details(int(month))[0]  # Return the year and month name.
    except Exception as e:
        log_error(e)  # Log any exceptions.
        go_back('script')  # Return to the previous menu.


def process_generate_statement(*, auth: Authentication, criteria: str = 'all', start_date: str = None,
                               end_date: str = None, month: str = None, year: int = None):
    """
    Process and generate a transaction statement based on specified criteria.

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class used to authenticate the user and access transaction data.
    criteria : str, optional
        The criteria for generating the statement. It can be 'all', 'date', or 'month'. Defaults to 'all'.
    start_date : str, optional
        The start date for transactions when criteria is 'date'. Format should be 'YYYY-MM-DD'. Defaults to None.
    end_date : str, optional
        The end date for transactions when criteria is 'date'. Format should be 'YYYY-MM-DD'. Defaults to None.
    month : str, optional
        The month for transactions when criteria is 'month'. Format should be the month's name (e.g., 'January'). Defaults to None.
    year : int, optional
        The year for transactions when criteria is 'month'. Defaults to None.

    Notes
    -----
    The function will repeatedly prompt the user until a valid transaction statement is generated or a break condition is met.
    """

    while True:
        header()  # Call the header function to display the header.
        print()  # Print a blank line for spacing.

        trans = None
        if criteria == 'date':
            # Parse the start and end dates from the input strings and generate a statement for the date range.
            trans = auth.transaction_statement(
                start_date=datetime(int(start_date.split('-')[0]), int(start_date.split('-')[1]),
                                    int(start_date.split('-')[2]), 0, 0, 0),
                end_date=datetime(int(end_date.split('-')[0]), int(end_date.split('-')[1]),
                                  int(end_date.split('-')[2]), 23, 59, 59), time_period=True)

            if trans is True:
                # If no transactions are found within the specified date range, notify the user and exit the loop.
                print(":: You don't have any transaction within this time frame.")
                time.sleep(5)  # Wait for 5 seconds before continuing.
                break

        elif criteria == 'month':
            # Generate a transaction statement for the specified month and year.
            trans = auth.transaction_statement(month=month, year=year, is_month=True)

            if trans is True:
                # If no transactions are found for the specified month, notify the user and exit the loop.
                print(f":: You don't have any transaction in the month of {month.title()}, {year}")
                time.sleep(5)  # Wait for 5 seconds before continuing.
                break

        elif criteria == 'all':
            # Generate a transaction statement for all available transactions.
            trans = auth.transaction_statement()
            if trans is True:
                # If no transactions are found, notify the user and exit the loop.
                print(":: You don't have any transaction on your account.")
                time.sleep(5)  # Wait for 5 seconds before continuing.
                break

        # Display a countdown timer while the statement is being generated.
        countdown_timer(_register='\rGenerating', _duty='Statement', countdown=5)

        # Get the current date and time.
        today_date = findDate(f'{datetime.today().year}-{datetime.today().month}-{datetime.today().day}')
        today_time = f'{datetime.today().time()}'

        # Prepare a notification message with the statement details.
        note = (f"Your Transaction Statement has been sent to your INBOX.\nDate: "
                f"{today_date[0]}, {today_date[1]} {today_date[2]}, {today_date[3]}\nTime: {today_time[:5]}")

        # Send a notification with the transaction statement details.
        notify.statement_notification(
            title='Console Beta Banking',
            message=note,
            channel='ConsoleBeta'
        )

        # Append the transaction statement details to a file.
        with open('notification/account_statement.txt', 'a') as file:
            file.write(f'\nTransaction Statement for {auth.account_holder}. Date: {today_date[0]}, {today_date[1]} '
                       f'{today_date[2]}, {today_date[3]} ' + '\n' + str(trans) + '\n')

        break  # Exit the loop after processing the statement.


def generate_statement(auth: Authentication):
    try:
        while True:
            header()  # Call the header function to display the header.

            print('\nChoose a Criteria:\n~~~~~~~~~~~~~~~~~~\n')
            print("+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")
            print("|     1. BY DATE     |     2. BY MONTH     |")
            print("+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")
            print("|         3. ALL TRANSACTION HISTORY       |")
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            user_input = input(">>> ").strip()  # Prompt user input and strip whitespace.

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                time.sleep(1)  # Wait for 1 second before breaking.
                break
            elif re.search('^1$', user_input):
                dates = by_date(current_year=datetime.today().year)  # Get the start and end dates.
                if dates == 'break':
                    continue  # Continue to the next iteration if 'break' is returned.

                process_generate_statement(
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

                process_generate_statement(
                    auth=auth,
                    criteria='month',
                    month=month[1],
                    year=month[0]
                )
                break

            elif re.search('^3$', user_input):
                process_generate_statement(auth=auth)  # Get all transaction history.
                break

            else:
                print("\n:: Invalid input, please try again.")
                time.sleep(2)  # Wait for 2 seconds before retrying.

    except Exception as e:
        log_error(e)  # Log any exceptions.
        go_back('signed_in', auth=auth)  # Return to the previous menu.
