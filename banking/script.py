import datetime
import calendar
import os
import re
import sys
import time
from bank_processes.authentication import Authentication
from animation.colors import *


def log_error(error: Exception):
    """Logs errors to a file."""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    with open('notification/error.txt', 'w') as file:
        file.write(f'{exc_type}, \n{os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]}, \n{exc_tb.tb_lineno}, '
                   f'\nError: {repr(error)}')
    print(f'\nError: {repr(error)}')
    time.sleep(3)
    
    
def clear():
    """
    Clears the output console.

    This function uses the `os.system` command to clear the console.
    It checks the operating system type and executes the appropriate command:
    - For Windows (`nt`), it uses `cls`.
    - For Unix/Linux/Mac (`posix`), it uses `clear`.
    """
    os.system('cls') if os.name == 'nt' else os.system('clear')


def findDate(date):
    """
    Function to determine the day of the week for a given date and return the day of the week,
    day, month name, and year.

    Parameters
    ---------
    date : str
        Date string in the format 'YYYY-MM-DD'.

    Returns
    -------
    tuple:
        A tuple containing the day of the week (str), day (str), month name (str), and year (str).
    """

    # Split the input date string into year, month, and day, then convert them to integers
    year, month, day = (int(i) for i in date.split('-'))

    # Calculate the day of the week as an integer (0=Monday, 6=Sunday)
    dayNumber = calendar.weekday(year, month, day)

    # Get the current month number (1=January, 12=December)
    monthNumber = datetime.datetime.now().month

    # List of days of the week where index 0 is Monday and index 6 is Sunday
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # List of month names where index 0 is January and index 11 is December
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    # Return the day of the week, day of the month, month name, and year
    # Note: The month name should be based on the input date's month, not the current month
    return days[dayNumber], str(day), months[monthNumber - 1], str(year)


def header():
    """
    Function to clear the console and display a header with the current date and time,
    formatted with specific styles.
    """

    # Clear the console (function definition for clear() is assumed to be elsewhere)
    clear()

    # Get the current time
    time_now = datetime.datetime.now().time()

    # Get the current date
    date = datetime.datetime.today().date()

    # Extract day of the week, day, month, and year from the current date
    day_in_words, day, month, year = findDate(str(date))

    # Print the header information with specific styling
    print(bold, end='')  # Start with bold text
    print(brt_black_bg, end='')  # Set background to bright black
    print(brt_yellow, end='')  # Set text color to bright yellow
    print(
        f"CONSOLE BETA BANKING   :: {day_in_words}, {day} {month} {year} ::   :: {time_now} ::")  # Print formatted date and time
    print(end, end='')  # Reset the styling

    # Print a separator line with dynamic length based on the lengths of the date and time strings
    print(f"{magenta}{bold}~~~~~~~~~~~~~~~~~~~~   ~~~~~~~~~~",
          "~" * (len(day_in_words) + len(day) + len(month) + len(year)),
          "   ~~~~~~", "~" * len(str(time_now)), sep='')
    print(end, end='')  # Reset the styling


def go_back(return_place, auth: Authentication = None):
    """Placeholder function to handle going back to a previous step.
        This should be defined elsewhere in the actual implementation.

    Args:
        return_place (str): The place to return to ('script' or 'signed_in').
        auth (Authentication, optional): The authentication object. Defaults to None.
    """
    if return_place == 'script':
        signing_in()
    if return_place == 'signed_in':
        signed_in(auth)


def signing_in():
    from banking.login_panel import login
    from banking.register_panel import register_bvn_account

    while True:
        header()

        print(end='\n')

        print(f'{bold}{brt_black_bg}{brt_yellow}' + 'Welcome, what can we do for you today?' + f'{end}\n')
        print(f'{magenta}+~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+')
        print(f"|  {brt_black_bg}{brt_yellow}1. NEW USER{end}  {magenta}|  "
              f"{brt_black_bg}{brt_yellow}2. EXISTING USER{end}  {magenta}|")
        print(f"+~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+")
        print(f"|         {brt_black_bg}{brt_yellow}3. UNBLOCK ACCOUNT{end}         {magenta}|")
        print(f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

        print(magenta, bold, end='')
        user_input = input(">>> ").strip()
        print(end, end='')

        if re.search('^1$', user_input):
            register_bvn_account()
            time.sleep(5)
            login()
            continue
        elif re.search('^2$', user_input):
            login()
            continue
        elif re.search('^3$', user_input):
            continue
        else:
            del user_input
            continue


def signed_in_header(auth: Authentication, account_balance_display: bool = True):
    """
    Function to display the signed-in header for the user, including a personalized greeting
    and optionally the account balance. The display changes based on the time of the day.

    Args:
        auth (Authentication): The authentication object containing user details.
        account_balance_display (bool): Flag to indicate if the account balance should be displayed.

    Returns:
        str: Returns 'HIDE' if the account balance is displayed, otherwise returns 'SHOW'.
    """
    try:
        # Determine the time of the day and set the appropriate greeting
        current_time = datetime.datetime.now().time()
        if datetime.time(0, 0, 0) < current_time < datetime.time(12, 0, 0):
            time_of_the_day = 'Morning'
        elif datetime.time(12, 0, 0) < current_time < datetime.time(17, 0, 0):
            time_of_the_day = 'Afternoon'
        elif datetime.time(17, 0, 0) < current_time < datetime.time(22, 0, 0):
            time_of_the_day = 'Evening'
        else:
            time_of_the_day = 'Night'

        # Call the header function to display the general header
        header()

        # Check if account balance should be displayed
        if account_balance_display:
            display_name = 'HIDE'
            print(end='\n')
            # Print personalized greeting with account balance
            print(f"Good {time_of_the_day}, {auth.first_name}"
                  f"{' ' * (28 - len(auth.first_name + time_of_the_day))}"
                  f"{auth.account_balance} Naira"
                  f"{' ' * (24 - len(str(auth.account_balance)))}"
                  f"Session Token: {auth.session_token}")

            # Print separator line with dynamic length
            print(f"~" * 7, "~" * len(time_of_the_day), "~" * len(auth.first_name),
                  " " * (28 - len(auth.first_name + time_of_the_day)), "~" * 6,
                  "~" * len(str(auth.account_balance)), " " * (24 - len(str(auth.account_balance))), "~~~~~~~~~~~~~~~",
                  "~" * len(auth.session_token), sep='')
        else:
            display_name = 'SHOW'
            print(end='\n')
            # Print personalized greeting without account balance
            print(f"Good {time_of_the_day}, {auth.first_name}"
                  f"{' ' * (58 - len(auth.first_name + time_of_the_day))}"
                  f"Session Token: {auth.session_token}")

            # Print separator line with dynamic length
            print(f"~~~~~~~", "~" * len(time_of_the_day), "~" * len(auth.first_name),
                  ' ' * (58 - len(auth.first_name + time_of_the_day)),
                  "~~~~~~~~~~~~~~~", "~" * len(auth.session_token), sep='')

        return display_name
    except Exception as e:
        # Handle any exceptions by logging the error and navigating back
        log_error(e)
        go_back('script')


def signed_in(auth: Authentication):
    """Function to sign in Users with a Savings or Current account"""
    from banking.transfer_money import process_transfer
    from banking.fixed_deposit import create_safelock, access_safelock
    from banking.deposit_money import deposit
    from banking.login_panel import login
    from banking.withdrawals import withdraw
    from banking.collect_loan import preview
    from banking.update_bvn import update_bvn

    try:
        account_balance_display = None
        while True:
            if auth.account_status == 'active':
                display_name = signed_in_header(auth, account_balance_display)

                print(end='\n')
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print(f"|  1. {display_name} ACCOUNT BALANCE  |    2. TRANSFER MONEY    |   3. CARD-LESS WITHDRAWAL    |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|      4. DEPOSIT MONEY     |     5. COLLECT LOAN     |        6. UPDATE BVN         |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|  7. TRANSACTION HISTORY   |  8. GENERATE STATEMENT  |       9. BENEFICIARIES       |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|    10. UPGRADE ACCOUNT    |    11. OPEN ACCOUNT     |       12. CLOSE ACCOUNT      |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|     13. BLOCK ACCOUNT     |  14. VIEW CONTACT INFO  |  15. CHANGE TRANSACTION PIN  |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|  16. UPDATE ACCOUNT INFO  |  17. BANK INFORMATION   |      18. FIXED DEPOSIT       |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|                                     19. LOGOUT                                     |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

                user_input = input(">>> ").strip()

                if re.search('^1$', user_input):
                    if display_name == 'SHOW':
                        account_balance_display = True
                    else:
                        account_balance_display = False

                    continue
                elif re.search('^2$', user_input):
                    process_transfer(auth)
                    continue
                elif re.search('^3$', user_input):
                    withdraw(auth)
                    continue
                elif re.search('^4$', user_input):
                    deposit(auth)
                    continue
                elif re.search('^5$', user_input):
                    preview()
                    continue
                elif re.search('^6$', user_input):
                    update_bvn()
                    continue
                elif re.search('^7$', user_input):
                    continue
                elif re.search('^8$', user_input):
                    continue
                elif re.search('^9$', user_input):
                    continue
                elif re.search('^10$', user_input):
                    continue
                elif re.search('^11$', user_input):
                    continue
                elif re.search('^12$', user_input):
                    continue
                elif re.search('^13$', user_input):
                    continue
                elif re.search('^14$', user_input):
                    continue
                elif re.search('^15$', user_input):
                    continue
                elif re.search('^16$', user_input):
                    continue
                elif re.search('^17$', user_input):
                    continue
                elif re.search('^18$', user_input):
                    if auth.fixed_account == 'yes':
                        access_safelock(auth)
                        continue
                    elif auth.fixed_account == 'no':
                        create_safelock(auth)
                        continue
                elif re.search('^19$', user_input):
                    auth.user_logout()
                    del user_input
                    login()
                    break
                elif re.search('^.*(back|return).*$', user_input.strip().lower()):
                    auth.user_logout()
                    del user_input
                    go_back('script')
                    break
                else:
                    del user_input
                    continue
            else:
                header()
                print("\n:: Account is BLOCKED.\n:: Meet the admin to UNBLOCK your account.")
                time.sleep(5)
                break
    except Exception as e:
        log_error(e)
        go_back('script')
