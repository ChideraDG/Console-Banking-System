import re
import time
from datetime import datetime
from banking.register_panel import countdown_timer
from banking.main_menu import (header,
                               go_back,
                               signed_in,
                               findDate,
                               log_error)
from bank_processes.authentication import (Authentication,
                                           verify_data,
                                           check_account_status,
                                           get_username_from_database,
                                           token_auth)
from bank_processes.notification import Notification
from animation.colors import *

auth = Authentication()
notify = Notification()


def username():
    """
    Validates the username of the user.

    Returns
    -------
    str
        The validated username.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the main script.

    Notes
    -----
    This function prompts the user to enter a username and validates it against the existing database. It checks if
    the username matches specific criteria (such as being equal to '1' or '2'), allows the user to go back to the
    previous menu by entering 'back' or 'return', and verifies if the username exists in the database. If the
    username exists and the account is suspended or blocked, it provides appropriate messages and navigates back to
    the main script. If the username is valid and the account is active, it returns the username. If the username is
    incorrect, it prompts the user to try again.
    """
    try:
        while True:
            print(f"{bold}{brt_yellow}\nENTER YOUR USERNAME:{end}")
            print(f"{bold}{magenta}~~~~~~~~~~~~~~~~~~~~")

            _username = input(">>> ").strip()
            print(end, end='')

            if re.search('^1$', _username):
                return _username
            elif re.search('^2$', _username):
                return _username
            elif re.search('^.*(back|return).*$', _username.lower()):
                del _username
                go_back('script')
                break

            if verify_data('username', 1, _username):
                if check_account_status(_username)[1] == 'suspended':
                    print(f"{brt_red}\n:: Account is SUSPENDED.\n:: Reset your Password.{end}")
                    del _username
                    time.sleep(3)
                    go_back('script')
                    break
                elif check_account_status(_username)[1] == 'blocked':
                    print(f"{red}\n:: Account is BLOCKED.\n:: Meet the admin to UNBLOCK your account.{end}")
                    del _username
                    time.sleep(3)
                    go_back('script')
                    break
                elif check_account_status(_username)[0]:
                    auth.username = _username
                    return _username
            else:
                print(f"{red}\n:: Wrong Username.{end}")
                time.sleep(3)
                continue
    except Exception as e:
        log_error(e)
        go_back('script')


def password():
    """
    Validates the password of the user.

    Returns
    -------
    str
        The validated password.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the main script.

    Notes
    -----
    This function prompts the user to enter a password and validates it. The user has up to 3 attempts to enter the
    correct password. If the user enters 'back' or 'return', the function navigates back to the main script. If the
    user enters '1' or '2', the function returns the password as valid. Otherwise, the function checks the password
    against the stored password. If the password is correct, it returns the password. If the password is incorrect,
    the function increments the login attempts and prompts the user to try again. After 3 unsuccessful attempts,
    the account is suspended, and the user is prompted to reset the password.
    """
    try:
        while auth.login_attempts < 3:
            print(f"{bold}{brt_yellow}\nENTER YOUR PASSWORD:{end}")
            print(f"{bold}{magenta}~~~~~~~~~~~~~~~~~~~~")

            _password = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _password, re.IGNORECASE):
                return 'back'
            else:
                if re.search('^1$', _password):
                    return _password
                elif re.search('^2$', _password):
                    return _password

                auth.password = _password
                if auth.password_validation():
                    return _password
                else:
                    auth.login_attempts = auth.login_attempts + 1
                    if auth.login_attempts == 3:
                        print(f"{red}\n:: Wrong Password.{end}")
                        print(f"{red}Account has being Suspended. Reset your password.{end}")
                        time.sleep(3)
                        del _password
                        break
                    else:
                        print(f"{red}\n:: Wrong Password.{end}")
                        print(red, 3 - auth.login_attempts,
                              ' attempts remaining.\nAccount will be suspended after exhausting attempts', end, sep='')
                        time.sleep(3)
                        del _password
                        continue

        auth.account_lockout()
        time.sleep(1)
        go_back('script')
    except Exception as e:
        log_error(e)
        go_back('script')


def forgot_username():
    """
    Retrieves the username of the user based on the registered phone number or email.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the main script.

    Notes
    -----
    This function prompts the user to enter their registered phone number or email. It validates the input and checks
    if the phone number or email exists in the database. If valid, it retrieves the associated username and initiates
    a password and token authentication process. Upon successful token verification, the username is displayed to the
    user and saved in a notification file. If the token verification fails within 5 minutes, the function re-sends
    the token for re-authentication.
    """
    try:
        while True:
            print(f"{bold}{brt_yellow}\nENTER YOUR REGISTERED PHONE NUMBER/E-MAIL:{end}")
            print(f"{bold}{magenta}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            _input = input(">>> ").strip().lower()  # Get user input and convert it to lowercase.
            print(end, end='')

            if re.search('^.*(back|return).*$', _input.lower()):  # Check if the user wants to go back.
                del _input  # Delete the input to free memory.
                go_back('script')
                break
            else:
                if re.search(r"^\w+@(\w+\.)?\w+\.(edu|com|gov|ng|org)$", _input,
                             re.IGNORECASE):  # Validate email format.
                    _username: str = get_username_from_database(_input, email=True)  # Retrieve username by email.
                    column = 'email'
                elif re.search(r'^\+?[0-9]{3} ?[0-9-]{8,11}$', _input) and 11 <= len(
                        _input) <= 15:  # Validate phone number format.
                    _username: str = get_username_from_database(_input,
                                                                phone_number=True)  # Retrieve username by phone number.
                    column = 'phone_number'
                else:
                    print(f"{brt_red}\nWrong Input{end}")  # Notify user of incorrect input format.
                    time.sleep(3)
                    continue

                if verify_data(column, 1, _input):  # Verify if the input exists in the database.
                    auth.username = _username
                    time.sleep(1)
                    _password = password()  # Prompt for password.
                    time.sleep(1)

                    start_time = time.time()  # Start timing for token verification.
                    _token = token_auth()  # Send a token for verification.
                    while True:
                        print(f"{bold}{brt_yellow}\nENTER YOUR TOKEN NUMBER:{end}")
                        print(f"{bold}{magenta}~~~~~~~~~~~~~~~~~~~~~~~~")

                        _tokenNumber = input(">>> ").strip()  # Get the token number input from the user.
                        print(end, end='')

                        if re.search('^.*(back|return).*$', _tokenNumber,
                                     re.IGNORECASE):  # Check if the user wants to go back.
                            del _tokenNumber  # Delete the token number to free memory.
                            go_back('script')
                        else:
                            elapsed_time = time.time() - start_time  # Calculate elapsed time.
                            if elapsed_time < 300.0:  # Check if the token is entered within 5 minutes.
                                if _token == _tokenNumber:  # Verify if the token matches.
                                    notify.forgot_username_notification(
                                        title='Console Beta Banking',
                                        message=f"Your Username: {_username}. \nDon't Share it.",
                                        channel='Forgot_Username'
                                    )

                                    print(red, end='')
                                    print(
                                        "\n:: Username Successfully Recovered.\n:: Username sent to your notification")
                                    print(end, end='')

                                    break
                                else:
                                    print(
                                        f"{red}\n:: Wrong Token Number.\n:: Try Again{end}")  # Notify user of wrong token.
                                    time.sleep(3)
                                    continue
                            else:
                                print(f"{red}\n:: Time is already over 5 minutes.{end}")  # Notify user of timeout.
                                time.sleep(1)
                                print(f"{brt_yellow}\n:: Re-Sending Token Number{end}")
                                start_time = time.time()  # Reset start time for new token.
                                _token = token_auth()  # Resend token.
                                time.sleep(3)
                                continue
                    break
                else:
                    # Notify user if phone number/email doesn't exist.
                    print(f"{red}\n:: Phone Number doesn't exist.{end}")
                    time.sleep(3)
                    continue
    except Exception as e:
        log_error(e)  # Log the error if an exception occurs.
        go_back('script')  # Navigate back to the main script.


def forgot_password():
    """
    Resets the password of the user.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the main script.

    Notes
    -----
    This function prompts the user to enter their username. It verifies if the username exists in the database. If the
    username exists, the function initiates the password reset process, allowing the user to set a new password. If the
    username does not exist, it prompts the user to try again. The user can also choose to go back to the main script
    by entering 'back' or 'return'.
    """
    try:
        while True:
            print(f"{bold}{brt_yellow}\nENTER YOUR USERNAME:{end}")
            print(f"{bold}{magenta}~~~~~~~~~~~~~~~~~~~~")

            _input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                go_back('script')
            else:
                if verify_data('username', 1, _input):
                    auth.username = _input
                    time.sleep(2)
                    auth.reset_password()
                    auth.change_password()
                    notify.forgot_password_notification(
                        title='Console Beta Banking',
                        message=f"Your Password has been successfully changed.\nIf you didn't initiate this process."
                                f"\nBlock your Account or Visit your Nearest Branch to you. \nThank You",
                        channel='Forgot_Password'
                    )
                    break
                else:
                    print(f"{red}\n:: Username doesn't exist.{end}")
                    time.sleep(3)
                    continue
    except Exception as e:
        log_error(e)
        go_back('script')


def login():
    """
    Processes the user's login.

    Raises
    ------
    Exception
        If there is an error during the process, it logs the error and navigates back to the main script.

    Notes
    -----
    This function handles the user's login process. It prompts the user to enter their username and password, providing
    options to go back to the main script or retrieve forgotten username/password. Upon successful login, it displays a
    welcome message, logs the login event, and navigates the user to the signed-in section. The function also sends a
    login notification.
    """
    try:
        while True:
            # Display the header for the login section.
            header()

            # Provide options for going back or retrieving a forgotten username.
            print(f"{bold}{red}\nGo Back? Press 1{end}")
            print(f"{bold}{magenta}----------------{end}")
            print(f"{bold}{red}Forgot Username? Press 2{end}")
            print(f"{bold}{magenta}------------------------{end}")

            # Prompt the user to enter their username.
            _username: str = username()
            time.sleep(0.5)

            # Check if the user wants to go back to the main script.
            if re.search('^1$', _username):
                break
            # Check if the user wants to retrieve their forgotten username.
            elif re.search('^2$', _username):
                header()
                forgot_username()
                time.sleep(2)
                continue

            # Display the header again after retrieving the username.
            header()

            # Provide options for going back or retrieving a forgotten password.
            print(f"{bold}{red}\nGo Back? Press 1{end}")
            print(f"{bold}{magenta}----------------{end}")
            print(f"{bold}{red}Forgot Password? Press 2{end}")
            print(f"{bold}{magenta}------------------------{end}")
            print(f"{bold}{brt_yellow}{italic}\nWelcome Back, {auth.first_name}{end}")
            print(f"{bold}{magenta}~~~~~~~~~~~~~~" + '~' * len(auth.first_name) + f'{end}')

            # Prompt the user to enter their password.
            _password = password()

            # Check if the user wants to go back to the main script.
            if re.search('^1$', _password) or re.search('^back$', _password):
                continue
            # Check if the user wants to retrieve their forgotten password.
            elif re.search('^2$', _password):
                time.sleep(2)
                header()
                forgot_password()
                continue

            print(end='\n')

            # Display a countdown timer while logging in.
            countdown_timer(_register='\rLogging in', _duty='')

            # Get the current date and format it.
            date = datetime.today().date()
            day_in_words, day, month, year = findDate(str(date))

            # Set the username and password for authentication.
            auth.username = _username
            auth.password = _password

            # Perform the user login process.
            auth.user_login()

            # Send a login notification to the user.
            notify.sign_in_notification(
                title='Console Beta Banking',
                message=f"You logged into your Account on {day_in_words}, {day} {month} {year}.",
                channel='Log_In'
            )
            # Navigate to the signed-in section.
            signed_in(auth=auth)
            break
    except Exception as e:
        # Handle any exceptions by logging the error and navigating back to the main script.
        log_error(e)
        go_back('script')
