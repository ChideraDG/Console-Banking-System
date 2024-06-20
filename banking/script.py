import datetime
import calendar
import os
import re
import sys
import time
from dateutil.relativedelta import relativedelta
from bank_processes.authentication import Authentication
from animation.colors import *


def log_error(error: Exception):
    """
    Logs errors to a file.

    Parameters
    ----------
    error : Exception
        The exception object containing details of the error to be logged.

    Notes
    -----
    This function captures the exception details including the type of exception,
    the file name where the exception occurred, the line number, and a string
    representation of the error. It logs this information to a file named 'notification/error.txt'
    and also prints the error to the console with a delay of 3 seconds.
    """
    # Get the exception information
    exc_type, exc_obj, exc_tb = sys.exc_info()

    # Open the error log file in write mode
    with open('notification/error.txt', 'w') as file:
        # Write the exception details to the file
        file.write(
            f'{exc_type}, \n'  # Write the type of exception
            f'{os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]}\n'  # Get the filename where the exception occurred
            f'{exc_tb.tb_lineno}, \n'  # Write the line number where the exception occurred
            f'Error: {repr(error)}'  # Write the string representation of the error
        )

    # Print the error message to the console
    print(f'\nError: {repr(error)}')

    # Delay for 3 seconds to allow the user to read the error message
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

    # List of days of the week when index 0 is Monday and index 6 is Sunday
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
        print(f'{bold}{magenta}+~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+')
        print(f"|  {bold}{brt_black_bg}{brt_yellow}1. NEW USER{end}  {bold}{magenta}|  "
              f"{bold}{brt_black_bg}{brt_yellow}2. EXISTING USER{end}  {bold}{magenta}|")
        print(f"+~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+")
        print(f"|        {bold}{brt_black_bg}{brt_yellow}3. CUSTOMER SERVICE{end}         {bold}{magenta}|")
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
            print(bold, brt_yellow, italic, f"Good {time_of_the_day}, {auth.first_name}"
                  f"{' ' * (28 - len(auth.first_name + time_of_the_day))}"
                  f"{auth.account_balance} Naira"
                  f"{' ' * (24 - len(str(auth.account_balance)))}"
                  f"Session Token: {auth.session_token}", end, sep='')

            # Print separator line with dynamic length
            print(bold, magenta, f"~" * 7, "~" * len(time_of_the_day), "~" * len(auth.first_name),
                  " " * (28 - len(auth.first_name + time_of_the_day)), "~" * 6,
                  "~" * len(str(auth.account_balance)), " " * (24 - len(str(auth.account_balance))), "~~~~~~~~~~~~~~~",
                  "~" * len(auth.session_token), end, sep='')
        else:
            display_name = 'SHOW'
            print(end='\n')
            # Print personalized greeting without an account balance
            print(bold, brt_yellow, italic, f"Good {time_of_the_day}, {auth.first_name}"
                  f"{' ' * (58 - len(auth.first_name + time_of_the_day))}"
                  f"Session Token: {auth.session_token}", end, sep='')

            # Print separator line with dynamic length
            print(bold, magenta, f"~~~~~~~", "~" * len(time_of_the_day), "~" * len(auth.first_name),
                  ' ' * (58 - len(auth.first_name + time_of_the_day)),
                  "~~~~~~~~~~~~~~~", "~" * len(auth.session_token), end, sep='')

        return display_name
    except Exception as e:
        # Handle any exceptions by logging the error and navigating back
        log_error(e)
        go_back('script')


def signed_in(auth: Authentication):
    """Function to sign in Users with a Savings or Current account"""
    try:
        from banking.transfer_money import process_transfer
        from banking.fixed_deposit import create_safelock, access_safelock
        from banking.deposit_money import deposit
        from banking.login_panel import login
        from banking.withdrawals import withdraw
        from banking.collect_loan import preview
        from banking.update_bvn import update_bvn
        from banking.trans_history import transaction_history
        from banking.block_account import block_account
        from banking.generate_statement import generate_statement
        from banking.beneficiary import beneficiaries

        account_balance_display = None
        while True:
            if auth.account_status == 'active':
                display_name = signed_in_header(auth, account_balance_display)

                print(end='\n')
                print(bold, magenta, "+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~"
                                     "+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+", sep='')
                print(f"|{end}  {bold}{brt_black_bg}{brt_yellow}1. {display_name} ACCOUNT BALANCE{end}  {bold}{magenta}"
                      f"|    {bold}{brt_black_bg}{brt_yellow}2. TRANSFER MONEY{end}    {bold}{magenta}|    {bold}"
                      f"{brt_black_bg}{brt_yellow}3. CARD-LESS WITHDRAWAL{end}   {bold}{magenta}|")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print(f"|{end}      {bold}{brt_black_bg}{brt_yellow}4. DEPOSIT MONEY{end}     {bold}{magenta}|     "
                      f"{bold}{brt_black_bg}{brt_yellow}5. COLLECT LOAN{end}     {bold}{magenta}|        {bold}"
                      f"{brt_black_bg}{brt_yellow}6. UPDATE BVN{end}         {bold}{magenta}|")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print(f"|{end}  {bold}{brt_black_bg}{brt_yellow}7. TRANSACTION HISTORY{end}   {bold}{magenta}|  "
                      f"{bold}{brt_black_bg}{brt_yellow}8. GENERATE STATEMENT{end}  {bold}{magenta}|       {bold}"
                      f"{brt_black_bg}{brt_yellow}9. BENEFICIARIES{end}       {bold}{magenta}|")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print(f"|{end}    {bold}{brt_black_bg}{brt_yellow}10. UPGRADE ACCOUNT{end}    {bold}{magenta}|    "
                      f"{bold}{brt_black_bg}{brt_yellow}11. OPEN ACCOUNT{end}     {bold}{magenta}|       {bold}"
                      f"{brt_black_bg}{brt_yellow}12. CLOSE ACCOUNT{end}      {bold}{magenta}|")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print(f"|{end}     {bold}{brt_black_bg}{brt_yellow}13. BLOCK ACCOUNT{end}     {bold}{magenta}|  "
                      f"{bold}{brt_black_bg}{brt_yellow}14. VIEW CONTACT INFO{end}  {bold}{magenta}|  {bold}"
                      f"{brt_black_bg}{brt_yellow}15. CHANGE TRANSACTION PIN{end}  {bold}{magenta}|")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print(f"|{end}  {bold}{brt_black_bg}{brt_yellow}16. UPDATE ACCOUNT INFO{end}  {bold}{magenta}|  "
                      f"{bold}{brt_black_bg}{brt_yellow}17. BANK INFORMATION{end}   {bold}{magenta}|      {bold}"
                      f"{brt_black_bg}{brt_yellow}18. FIXED DEPOSIT{end}       {bold}{magenta}|")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print(f"|{end}                                     {bold}{brt_black_bg}{brt_yellow}19. LOGOUT{end}    "
                      f"                                 {bold}{magenta}|")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+", sep='')

                user_input = input(">>> ").strip()
                print(end, end='')

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
                    preview(auth)
                    continue
                elif re.search('^6$', user_input):
                    update_bvn(auth)
                    continue
                elif re.search('^7$', user_input):
                    transaction_history(auth)
                    continue
                elif re.search('^8$', user_input):
                    generate_statement(auth)
                    continue
                elif re.search('^9$', user_input):
                    beneficiaries(auth)
                    continue
                elif re.search('^10$', user_input):
                    continue
                elif re.search('^11$', user_input):
                    print("This option is UNAVAILABLE")
                    continue
                elif re.search('^12$', user_input):
                    continue
                elif re.search('^13$', user_input):
                    block_account(auth)
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
                elif re.search('^(19|.*(back|return).*)$', user_input):
                    auth.user_logout()
                    del user_input
                    signing_in()
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


def calculate_end_date(start_date_str, months) -> str:
    """
    Calculate the end date after adding a specified number of months to a start date.

    Parameters
    ----------
    start_date_str : str
        The start date in 'YYYY-MM-DD' format.
    months : int
        The number of months to add to the start date.

    Returns
    -------
    str
        The end date in 'YYYY-MM-DD' format.

    Examples
    --------
    >>> calculate_end_date('2024-01-15', 6)
    '2024-07-15'
    """

    # Convert the start date string to a datetime object
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')

    # Add the number of months to the start date
    end_date = start_date + relativedelta(months=months)

    # Return the end date in the same format as the input
    return end_date.strftime('%Y-%m-%d')
