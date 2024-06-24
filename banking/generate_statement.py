import re
import time
from datetime import datetime
from bank_processes.authentication import Authentication
from bank_processes.notification import Notification
from banking.register_panel import countdown_timer
from banking.main_menu import header, log_error, go_back, findDate
from banking.trans_history import by_date, by_month
from animation.colors import *


notify = Notification()


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
                print(green, ":: You don't have any transaction within this time frame.", end, sep='')
                time.sleep(5)  # Wait for 5 seconds before continuing.
                break

        elif criteria == 'month':
            # Generate a transaction statement for the specified month and year.
            trans = auth.transaction_statement(month=month, year=year, is_month=True)

            if trans is True:
                # If no transactions are found for the specified month, notify the user and exit the loop.
                print(green, f":: You don't have any transaction in the month of {month.title()}, {year}", end, sep='')
                time.sleep(5)  # Wait for 5 seconds before continuing.
                break

        elif criteria == 'all':
            # Generate a transaction statement for all available transactions.
            trans = auth.transaction_statement()
            if trans is True:
                # If no transactions are found, notify the user and exit the loop.
                print(green, ":: You don't have any transaction on your account.", end, sep='')
                time.sleep(5)  # Wait for 5 seconds before continuing.
                break

        # Display a countdown timer while the statement is being generated.
        countdown_timer(_register='\rGetting your', _duty='Statement', countdown=5)

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

            print(bold, brt_yellow, '\nChoose a Criteria:')
            print(magenta, '~~~~~~~~~~~~~~~~~~', sep='')
            print("\n+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")
            print(
                f"|     {brt_black_bg}{brt_yellow}1. BY DATE{end}     {bold}{magenta}|     {brt_black_bg}{brt_yellow}2. BY MONTH{end}     {bold}{magenta}|")
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
                print(red, "\n:: Invalid input, please try again.", end)
                time.sleep(2)  # Wait for 2 seconds before retrying.

    except Exception as e:
        log_error(e)  # Log any exceptions.
        go_back('signed_in', auth=auth)  # Return to the previous menu.
