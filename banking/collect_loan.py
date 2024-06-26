import datetime
import re
from time import sleep
from bank_processes.authentication import Authentication
from bank_processes.loan import Loan
from bank_processes.notification import Notification
from banking.fixed_deposit import calculate_interest, get_month
from banking.register_panel import countdown_timer
from banking.main_menu import go_back, header, calculate_end_date, log_error
from banking.deposit_money import deposit_default
from animation.colors import *

loan = Loan()
notify = Notification()


def repayment_period() -> str | int:
    while True:
        sleep(0.5)

        print(bold, brt_yellow, '\nRepayment period in months: (2 means Two months)', end, sep='')
        print(bold, magenta, '~~~~~~~~~~~~~~~~~~~~~~~~~~~', sep='')

        period = input('>>> ')
        print(end, end='')

        if re.search('^.*(back|return).*$', period, re.IGNORECASE):
            return 'preview'

        # Ensure the input is a valid number
        elif re.search("^[0-9]{1,3}$", period, re.IGNORECASE):

            return int(period)

        else:
            print(red, f"\n:: Wrong Input", end, sep='')
            sleep(1)
            continue


def annual_percentage_rate():
    while True:
        sleep(0.5)

        print(bold, brt_yellow, '\nAnnual percentage rate of interest: (%)', end, sep='')
        print(bold, magenta, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', sep='')

        rate = input('>>> ')
        print(end, end='')

        if re.search('^.*(back|return).*$', rate, re.IGNORECASE):
            return 'preview'

        # Ensure the input is a valid number
        elif re.search("^[0-9]{1,3}[.]?[0-9]{0,2}$", rate, re.IGNORECASE):
            return float(rate)

        else:
            print(red, f"\n:: Wrong Input", end, sep='')
            sleep(1)
            continue


def amount_of_the_loan():
    while True:
        sleep(0.5)

        print(bold, brt_yellow, '\nAmount of the Loan: (Naira)', end, sep='')
        print(bold, magenta, '~~~~~~~~~~~~~~~~~~~', sep='')

        amount = input('>>> ')
        print(end, end='')

        if re.search('^.*(back|return).*$', amount, re.IGNORECASE):
            return 'preview'

        # Ensure the input is a valid number
        elif re.search("^[0-9]{0,30}[.]?[0-9]{0,2}$", amount, re.IGNORECASE):
            return float(amount)

        else:
            print(red, f"\n:: Wrong Input", end, sep='')
            sleep(1)
            continue


def payment_info(*, _loan_amount, _annual_rate, _repayment_period, _payment_period, _total_payment, _interest):
    """
    Display the loan payment information and provide options to repeat or exit the process.

    Parameters
    ----------
    _loan_amount : float
        The amount of the loan in Naira.
    _annual_rate : float
        The annual percentage rate of interest.
    _repayment_period : int
        The repayment period in months.
    _payment_period : str
        The formatted monthly payment amount.
    _total_payment : str
        The formatted total payment amount.
    _interest : str
        The formatted total interest payments.

    Returns
    -------
    str
        User's decision to either 'back', 'continue', or 'break' the process
    """
    try:
        while True:
            header()

            print(bold, brt_yellow, '\nAmount of the Loan: (Naira)', end, sep='')
            print(bold, magenta, '~~~~~~~~~~~~~~~~~~~', end, sep='')
            print(green, f':: N{_loan_amount}\n', end, sep='')

            print(bold, brt_yellow, '\nAnnual percentage rate of interest: (%)', end, sep='')
            print(bold, magenta, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', end, sep='')
            print(green, f':: {_annual_rate}%\n', end, sep='')

            print(bold, brt_yellow, '\nRepayment period in months: (2 means Two months)', end, sep='')
            print(bold, magenta, '~~~~~~~~~~~~~~~~~~~~~~~~~~~', end, sep='')
            print(green, f':: {_repayment_period}\n', end, sep='')

            print(bold, brt_yellow, '\nPayment Information:', end, sep='')
            print(f'{bold}{magenta}~~~~~~~~~~~~~~~~~~~~\n')

            print(f'+{'~' * (38 + len(_payment_period))}+', sep='')
            print(f'|{end}  {bold}{brt_black_bg}{brt_yellow}Your monthly payment will be{end}  {bold}{magenta}::{end}  {green}{_payment_period}{end}  {bold}{magenta}|')
            print(f'+{'~' * (38 + len(_payment_period))}+\n')

            print(f'+{'~' * (36 + len(_total_payment))}+')
            print(f'|{end}  {bold}{brt_black_bg}{brt_yellow}Your total payment will be{end}  {bold}{magenta}::{end}  {green}{_total_payment}{end}  {bold}{magenta}|')
            print(f'+{'~' * (36 + len(_total_payment))}+\n')

            print(f'+{'~' * (46 + len(_interest))}+')
            print(f'|{end}  {bold}{brt_black_bg}{brt_yellow}Your total interest payments will be{end}  {bold}{magenta}::{end}  {green}{_interest}{end}  {bold}{magenta}|')
            print(f'+{'~' * (46 + len(_interest))}+\n', end)

            print(bold, brt_yellow, '\nDo you want to Repeat process?', sep='')
            print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')  # Present Yes/No options
            print(f'{bold}{magenta}~~~~~~     ~~~~~')

            _input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                return 'back'
            elif re.search('^1$', _input, re.IGNORECASE):
                return 'continue'
            elif re.search('^2$', _input, re.IGNORECASE):
                return 'break'
            else:
                print(red, f"\n:: Wrong Input", end, sep='')
                sleep(1.5)
                continue

    except Exception as e:
        log_error(e)
        go_back('script')


def loan_calculator():
    """
    Perform loan calculations by obtaining loan information from the user,
    calculating the interest, and displaying payment information.
    """
    try:
        while True:
            header()  # Display header for the loan calculator interface
            print(bold, brt_yellow, '\nEnter Loan Information:', end, sep='')
            print(bold, magenta, '~~~~~~~~~~~~~~~~~~~~~~~', end, sep='')

            # Obtain loan amount from the user
            loan_amount = amount_of_the_loan()
            if loan_amount == 'preview':
                break

            # Obtain annual percentage rate from the user
            annual_rate = annual_percentage_rate()
            if annual_rate == 'preview':
                break

            # Obtain repayment period from the user
            period = repayment_period()
            if period == 'preview':
                break

            # Calculate interest and rate of interest based on user input
            interest, rate_of_interest = calculate_interest(
                principal=loan_amount,
                rate_per_year=annual_rate,
                days=period * 30  # Convert period from months to days
            )

            # Display a countdown timer while computing payment information
            countdown_timer(_register='\rComputing Payment Information', _duty='', countdown=5)

            # Calculate payment period, total payment, and interest
            payment_period = f'{((interest + loan_amount) / period):,.2f}'
            total_payment = f'{(interest + loan_amount):,.2f}'
            _interest = f'{interest:,.2f}'

            # Display payment information and wait for user input
            _payment_info = payment_info(
                _loan_amount=loan_amount,
                _annual_rate=annual_rate,
                _repayment_period=period,
                _payment_period=payment_period,
                _total_payment=total_payment,
                _interest=_interest
            )

            # Handle user input from payment information display
            if re.search('^back$', _payment_info, re.IGNORECASE):
                del _payment_info
                break
            elif re.search('^break$', _payment_info, re.IGNORECASE):
                sleep(0.5)
                break
            elif re.search('^continue$', _payment_info, re.IGNORECASE):
                sleep(0.5)
                continue

    except Exception as e:
        log_error(e)  # Log any exceptions raised during execution
        go_back('script')  # Navigate back to the previous script or step


def loan_questions() -> tuple[str, str] | tuple[float, str | int]:
    """
    Interactively prompts the user for loan details.

    Returns
    -------
    tuple[str, str] | tuple[float, str | int]
        A tuple containing the validated loan amount and repayment period.

    Notes
    -----
    This function continuously prompts the user to enter the amount of money they need to borrow.
    It validates the input to ensure it is a numeric value greater than 10000.0 naira.
    If the user enters 'back' or 'return', the function breaks the loop and exits.
    Once a valid loan amount is entered, it prompts for the repayment period.
    The repayment period can't be entered in months or as a string ('preview' to go back).
    If both the loan amount and repayment period are valid, they are returned as a tuple.
    """
    while True:
        header()  # Display header for the loan questions interface

        print(bold, brt_yellow, '\nHow much money do you need to borrow? (greater than 10000)', end, sep='')
        print(bold, magenta, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', sep='')

        amount = input(">>> ")  # Prompt user to enter the loan amount
        print(end, end='')

        if re.search('^.*(back|return).*$', amount, re.IGNORECASE):
            return 'break', 'break'

        # Ensure the input is a valid number
        elif re.search("^[0-9]{0,30}[.]?[0-9]{0,2}$", amount, re.IGNORECASE) is None:
            print(red, '\n:: Digits Only', end, sep='')  # Notify user if input contains non-digits
            sleep(2)
            continue

        # Check if the amount is greater than 10000.0 naira
        elif float(amount) < 10000.0:
            print(red, '\n:: Amount must be more than 10000.0 naira.', end, sep='')  # Notify user if amount is too low
            sleep(2)
            continue

        else:
            amount = float(amount)  # Convert valid input to float

            _repayment_period = repayment_period()  # Prompt user for repayment period

            if _repayment_period == 'preview':
                return 'break', 'break'
            else:
                return amount, _repayment_period  # Return validated amount and repayment period


def loan_receipt(auth: Authentication, end_date, _type: str, _amount: str, interest: float, _repayment_period: int,
                 _monthly_payment: str, ):
    """
    Generate and print a loan receipt for a client, and save it to a file.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user details.
    end_date : str
        The end date of the loan in 'YYYY-MM-DD' format.
    _type : str
        The type of the loan.
    _amount : str
        The loan amount.
    interest : float
        The annual interest rate.
    _repayment_period : int
        The repayment period in months.
    _monthly_payment : str
        The monthly repayment amount.
    """

    # Get the current month and the next month names
    month = get_month(datetime.datetime.today().month)[0]
    next_month = get_month(datetime.datetime.today().month + 1)[0]

    # Display header
    header()

    # Generate the receipt content
    receipt = (f"""\n
Today's Date: {month} {datetime.datetime.today().day}, {datetime.datetime.today().year}

Dear {auth.account_holder},    

We are pleased to inform you that your loan application has been approved and the funds have been 
successfully disbursed to your account. Below are the details of your loan:

Loan Details:

Loan Type: {_type} Loan
Loan Amount: N{_amount}
Interest Rate: {interest}% per annum
Start Date: {month} {datetime.datetime.today().day}, {datetime.datetime.today().year}
End Date: {end_date}
Repayment Period: {_repayment_period} months
Monthly Payment: N{_monthly_payment}

Disbursement Details:

Disbursement Date: {month} {datetime.datetime.today().day}, {datetime.datetime.today().year}
Disbursed Amount: N{_amount}
Disbursement Account: {auth.account_number}

Repayment Schedule:

Your monthly repayment amount is N{_monthly_payment}. The first payment is due on {next_month} {datetime.datetime.today().day}, {datetime.datetime.today().year}.


If you have any questions or need further assistance, please do not hesitate to contact us at:

Phone: (123) 456-7890
Email: consolebetabank@gmail.com
Address: 123 Bank Street, Finance City, 12345
Thank you for choosing Console Beta Bank for your financial needs. We look forward to serving you.

Sincerely,

Jane Smith
Loan Officer
Console Beta Bank
""")

    # Print the receipt
    print(receipt)

    # Wait for user input to end the page
    print(green, end='')
    input('\nType Anything to end this page\n>>> ')
    print(end, end='')

    # Save the receipt to a file
    with open('notification/loan_receipt.txt', 'w') as file:
        file.write(receipt)

    notify.loan_notification(
        title='Console Beta Banking',
        message='Your Loan Receipt has been sent to your INBOX. Thanks for banking with us.',
        channel='loan_receipt'
    )

    go_back('signed_in', auth)


def loan_processing(*, auth: Authentication, amount: float, _repayment_period: int, interest: float, _type: tuple):
    """
    Process a loan application and update the loan database after obtaining necessary information from the client.

    Parameters
    ----------
    auth : Authentication
        The authentication object containing user details.
    amount : float
        The loan amount requested by the client.
    _repayment_period : int
        The repayment period in months.
    interest : float
        The annual interest rate.
    _type : tuple
        A tuple containing the loan type description and code.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If any error occurs during the loan processing.
    """
    try:
        # Calculate the total interest and rate of interest
        _interest, rate_of_interest = calculate_interest(
            principal=amount,
            rate_per_year=interest,
            days=_repayment_period * 30
        )

        # Calculate the monthly payment and total payment
        payment_period = f'{((_interest + amount) / _repayment_period):,.2f}'
        total_payment = f'{(_interest + amount):,.2f}'

        # Calculate the end date of the loan
        end_date = calculate_end_date(
            f'{datetime.datetime.today().year}-{datetime.datetime.today().month}-{datetime.datetime.today().day}',
            _repayment_period
        )

        # Get the month name
        month = get_month(int(end_date[5:7]))[0]

        while True:
            header()

            # Display loan terms
            print(bold, brt_yellow, f'\n{_type[0]} Loan Term', end, sep='')
            print(bold, magenta, f'{"~" * len(_type[0])}~~~~~~~~~~\n', end, sep='')
            print(f'{bold}{brt_yellow}Total Interest {magenta}:: {green}N{_interest:,.2f}\n', end)
            print(f'{bold}{brt_yellow}Interest Rate {magenta}:: {green}{interest}% per annum\n', end)
            print(f'{bold}{brt_yellow}Total Payment {magenta}:: {green}N{total_payment}\n', end)
            print(f'{bold}{brt_yellow}Monthly Payment {magenta}:: {green}N{payment_period}\n', end)
            print(f'{bold}{brt_yellow}End Date {magenta}:: {green}{month} {datetime.datetime.today().day}, {end_date[:4]}', end)

            # Ask the user to accept the terms
            print(f'{bold}{brt_yellow}\nDo you accept these Terms?')
            print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')  # Present Yes/No options
            print(f'{bold}{magenta}~~~~~~     ~~~~~')

            _input = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                break
            elif re.search('^1$', _input, re.IGNORECASE):
                # Process the loan if the terms are accepted
                loan.email = auth.email
                due_month = int(f'{datetime.datetime.today().month + 1}')
                due_year = int(f'{datetime.datetime.today().year}')

                # Adjust the due month and year if the month exceeds 12
                while due_month > 12:
                    due_month -= 12
                    due_year += 1

                # Add user information to the database if not already present
                if loan.check_user_existence():
                    loan.first_name = auth.first_name
                    loan.last_name = auth.last_name
                    loan.email = auth.email
                    loan.phone_number = auth.phone_number
                    loan.address = auth.address
                    loan.date_of_birth = auth.date_of_birth
                    loan.add_user()

                # Add the loan to the database
                loan.add_loan(
                    loan_type=_type[1],
                    loan_status=1,
                    amount=_interest + amount,
                    interest_rate=interest,
                    monthly_payment=(_interest + amount) / _repayment_period,
                    start_date=f'{datetime.datetime.today().year}-{datetime.datetime.today().month}-'
                               f'{datetime.datetime.today().day}',
                    due_date=f'{due_year}-{due_month}-{datetime.datetime.today().day}',
                    end_date=f'{end_date[:4]}-{end_date[5:7]}-{end_date[8:]}'
                )

                # Simulate a countdown timer
                countdown_timer(_register='Loan', _duty='Payment', countdown=5)

                # Process the deposit
                deposit_default(auth,
                                _amount=amount,
                                _description=f'LOAN/CBB/DEPOSIT TO {auth.account_holder}')

                # Generate a loan receipt
                loan_receipt(auth, f'{month} {datetime.datetime.today().day}, {end_date[:4]}',
                             _type[0], total_payment, interest, _repayment_period, payment_period)
                break
            elif re.search('^2$', _input, re.IGNORECASE):
                print(red, '\n:: Loan Terms Rejected', end, sep='')
                sleep(2.5)
                break
            else:
                print(red, f"\n:: Wrong Input", end, sep='')
                sleep(1.5)
                continue
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def types_of_loans(auth: Authentication):
    """
    Display and process different types of loans available for the user.

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class containing user details.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If any error occurs during the loan processing.
    """
    try:
        while True:
            header()
            print(bold, brt_yellow, '\nWhat Type of Loan do you want?', end, sep='')
            print(bold, magenta, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', sep='')

            print('\n+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|      {brt_black_bg}{brt_yellow}1. Personal Loan{end}     {bold}{magenta}|        {brt_black_bg}{brt_yellow}2. Mortgage Loan{end}        {bold}{magenta}|        {brt_black_bg}{brt_yellow}3. Auto Loan{end}        {bold}{magenta}|')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|      {brt_black_bg}{brt_yellow}4. Student Loan{end}      {bold}{magenta}|     {brt_black_bg}{brt_yellow}5. Small Business Loan{end}     {bold}{magenta}|       {brt_black_bg}{brt_yellow}6. Payday Loan{end}       {bold}{magenta}|')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|    {brt_black_bg}{brt_yellow}7. Home Equity Loan{end}    {bold}{magenta}|   {brt_black_bg}{brt_yellow}8. Debt Consolidation Loan{end}   {bold}{magenta}|   {brt_black_bg}{brt_yellow}9. Credit Builder Loan{end}   {bold}{magenta}|')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|   {brt_black_bg}{brt_yellow}10. Peer to Peer Loan{end}   {bold}{magenta}|         {brt_black_bg}{brt_yellow}11. Title Loan{end}         {bold}{magenta}|       {brt_black_bg}{brt_yellow}12. Bridge Loan{end}      {bold}{magenta}|')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input('>>> ')
            print(end, end='')

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                break
            else:
                amount, _repayment_period = loan_questions()  # Get the loan amount and repayment period from the user
                if amount == 'break' and _repayment_period == 'break':
                    continue

                if re.search('^1$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Personal Loan
                    if _repayment_period < 12:
                        interest = 18.0
                    else:
                        interest = 36.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Personal', 1)
                    )

                    continue
                elif re.search('^2$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Mortgage Loan
                    if _repayment_period < 24:
                        interest = 3.0
                    else:
                        interest = 5.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Mortgage', 2)
                    )

                    continue
                elif re.search('^3$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Auto Loan
                    if _repayment_period < 24:
                        interest = 5.0
                    else:
                        interest = 10.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Auto', 3)
                    )
                    continue
                elif re.search('4$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Student Loan
                    if _repayment_period < 24:
                        interest = 4.0
                    else:
                        interest = 7.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Student', 4)
                    )
                    continue
                elif re.search('^5$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Small Business Loan
                    if _repayment_period < 24:
                        interest = 10.0
                    else:
                        interest = 13.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Small Business', 5)
                    )
                    continue
                elif re.search('^6$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Payday Loan
                    if _repayment_period < 5:
                        interest = 200.0
                    elif _repayment_period < 3:
                        interest = 400.0
                    else:
                        interest = 20.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Payday', 6)
                    )
                    continue
                elif re.search('^7$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Home Equity Loan
                    if _repayment_period < 24:
                        interest = 5.0
                    else:
                        interest = 10.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Home Equity', 7)
                    )
                    continue
                elif re.search('^8$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Debt Consolidation Loan
                    if _repayment_period < 24:
                        interest = 15.0
                    else:
                        interest = 36.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Debt Consolidation', 8)
                    )
                    continue
                elif re.search('^9$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Credit Builder Loan
                    if _repayment_period < 24:
                        interest = 10.0
                    else:
                        interest = 16.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Credit Builder', 9)
                    )
                    continue
                elif re.search('^10$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Peer to Peer Loan
                    if _repayment_period < 24:
                        interest = 20.0
                    else:
                        interest = 30.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Peer to Peer', 10)
                    )
                    continue
                elif re.search('^11$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Title Loan
                    if _repayment_period < 24:
                        interest = 25.0
                    else:
                        interest = 40.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Title', 11)
                    )
                    continue
                elif re.search('^12$', user_input, re.IGNORECASE):
                    # Set the interest rate based on the repayment period for Bridge Loan
                    if _repayment_period < 24:
                        interest = 12.0
                    else:
                        interest = 20.0

                    loan_processing(
                        auth=auth, amount=amount, _repayment_period=_repayment_period, interest=interest,
                        _type=('Bridge', 12)
                    )
                    continue
                else:
                    print(red, f"\n:: Wrong Input", end, sep='')
                    sleep(1.5)
                    continue
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def preview(auth: Authentication):
    try:
        while True:
            header()

            print(bold, magenta, '\n+~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|   {brt_black_bg}{brt_yellow}1. COLLECT LOAN{end}   {bold}{magenta}|   {brt_black_bg}{brt_yellow}2. LOAN CALCULATOR{end}   {bold}{magenta}|')
            print('+~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input('>>> ')
            print(end, end='')

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                break
            elif re.search('^1$', user_input, re.IGNORECASE):
                types_of_loans(auth)
                continue
            elif re.search('^2$', user_input, re.IGNORECASE):
                loan_calculator()
                continue
            else:
                print(red, f"\n:: Wrong Input", end, sep='')
                sleep(1.5)
                continue
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)
