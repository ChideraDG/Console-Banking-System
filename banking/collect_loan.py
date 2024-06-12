import datetime
import os
import re
import sys
from time import sleep
from bank_processes.authentication import Authentication
from bank_processes.loan import Loan
from banking.fixed_deposit import calculate_interest, get_month
from banking.register_panel import countdown_timer
from banking.script import go_back, header, calculate_end_date, log_error
from banking.deposit_money import deposit_default

loan = Loan()


def repayment_period() -> str | int:
    while True:
        sleep(0.5)

        print('\nRepayment period in months: (2 means Two months)')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        period = input('>>> ')

        if re.search('^.*(back|return).*$', period, re.IGNORECASE):
            return 'preview'

        # Ensure the input is a valid number
        elif re.search("^[0-9]{1,3}$", period, re.IGNORECASE):

            return int(period)

        else:
            print(f"\n:: Wrong Input")
            sleep(1)
            continue


def annual_percentage_rate():
    while True:
        sleep(0.5)

        print('\nAnnual percentage rate of interest: (%)')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        rate = input('>>> ')

        if re.search('^.*(back|return).*$', rate, re.IGNORECASE):
            return 'preview'

        # Ensure the input is a valid number
        elif re.search("^[0-9]{1,3}[.]?[0-9]{0,2}$", rate, re.IGNORECASE):
            return float(rate)

        else:
            print(f"\n:: Wrong Input")
            sleep(1)
            continue


def amount_of_the_loan():
    while True:
        sleep(0.5)

        print('\nAmount of the Loan: (Naira)')
        print('~~~~~~~~~~~~~~~~~~~')

        amount = input('>>> ')

        if re.search('^.*(back|return).*$', amount, re.IGNORECASE):
            return 'preview'

        # Ensure the input is a valid number
        elif re.search("^[0-9]{0,30}[.]?[0-9]{0,2}$", amount, re.IGNORECASE):
            return float(amount)

        else:
            print(f"\n:: Wrong Input")
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

            print('\nAmount of the Loan: (Naira)')
            print('~~~~~~~~~~~~~~~~~~~')
            print(f':: N{_loan_amount}\n')

            print('\nAnnual percentage rate of interest: (%)')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(f':: {_annual_rate}%\n')

            print('\nRepayment period in months: (2 means Two months)')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(f':: {_repayment_period}\n')

            print('\nPayment Information:')
            print('~~~~~~~~~~~~~~~~~~~~\n')

            print(f'+{'~' * (38 + len(_payment_period))}+')
            print(f'|  Your monthly payment will be  ::  {_payment_period}  |')
            print(f'+{'~' * (38 + len(_payment_period))}+\n')

            print(f'+{'~' * (36 + len(_total_payment))}+')
            print(f'|  Your total payment will be  ::  {_total_payment}  |')
            print(f'+{'~' * (36 + len(_total_payment))}+\n')

            print(f'+{'~' * (46 + len(_interest))}+')
            print(f'|  Your total interest payments will be  ::  {_interest}  |')
            print(f'+{'~' * (46 + len(_interest))}+\n')

            print('\nDo you want to Repeat process?')
            print('1. Yes  |  2. No')
            print('~~~~~~     ~~~~~')
            _input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                del _input
                return 'back'
            elif re.search('^1$', _input, re.IGNORECASE):
                return 'continue'
            elif re.search('^2$', _input, re.IGNORECASE):
                return 'break'
            else:
                print(f"\n:: Wrong Input")
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
            header()
            print('\nEnter Loan Information:')
            print('~~~~~~~~~~~~~~~~~~~~~~~')

            loan_amount = amount_of_the_loan()
            if loan_amount == 'preview':
                break

            annual_rate = annual_percentage_rate()
            if annual_rate == 'preview':
                break

            period = repayment_period()
            if period == 'preview':
                break

            interest, rate_of_interest = calculate_interest(
                principal=loan_amount,
                rate_per_year=annual_rate,
                days=period * 30
            )

            countdown_timer(_register='\rComputing Payment Information', _duty='', countdown=5)

            payment_period = f'{((interest + loan_amount) / period):,.2f}'
            total_payment = f'{(interest + loan_amount):,.2f}'
            _interest = f'{interest:,.2f}'

            _payment_info = payment_info(
                _loan_amount=loan_amount,
                _annual_rate=annual_rate,
                _repayment_period=period,
                _payment_period=payment_period,
                _total_payment=total_payment,
                _interest=_interest
            )

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
        log_error(e)
        go_back('script')


def loan_questions() -> tuple[float, str | int]:
    while True:
        header()

        print('\nHow much money do you need to borrow? (greater than 10000)')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        amount = input(">>> ")

        if re.search('^.*(back|return).*$', amount, re.IGNORECASE):
            break

        # Ensure the input is a valid number
        elif re.search("^[0-9]{0,30}[.]?[0-9]{0,2}$", amount, re.IGNORECASE) is None:
            print('\n:: Digits Only')
            sleep(2)
            continue

        # Check if the amount is greater than 10.0 naira
        elif float(amount) < 10000.0:
            print('\n:: Amount must be more than 10000.0 naira.')
            sleep(2)
            continue

        else:
            amount = float(amount)

            _repayment_period = repayment_period()
            if _repayment_period == 'preview':
                break
            else:
                return amount, _repayment_period


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
    input('\nType Anything to end this page\n>>> ')

    # Save the receipt to a file
    with open('notification/loan_receipt.txt', 'w') as file:
        file.write(receipt)


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
    """
    try:
        _interest, rate_of_interest = calculate_interest(
            principal=amount,
            rate_per_year=interest,
            days=_repayment_period * 30
        )

        payment_period = f'{((_interest + amount) / _repayment_period):,.2f}'
        total_payment = f'{(_interest + amount):,.2f}'

        end_date = calculate_end_date(
            f'{datetime.datetime.today().year}-{datetime.datetime.today().month}-{datetime.datetime.today().day}',
            _repayment_period
        )

        month = get_month(int(end_date[5:7]))[0]

        while True:
            header()

            print(f'\n{_type[0]} Loan Term')
            print(f'{'~' * len(_type[0])}~~~~~~~~~~\n')
            print(f'Total Interest :: N{_interest:,.2f}\n')
            print(f'Interest Rate :: {interest}% per annum\n')
            print(f'Total Payment :: N{total_payment}\n')
            print(f'Monthly Payment :: N{payment_period}\n')
            print(f'End Date :: {month} {datetime.datetime.today().day}, {end_date[:4]}')

            print('\nDo you accept these Terms?')
            print('1. Yes  |  2. No')
            print('~~~~~~     ~~~~~')
            _input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', _input, re.IGNORECASE):
                break
            elif re.search('^1$', _input, re.IGNORECASE):
                loan.email = auth.email
                due_month = int(f'{datetime.datetime.today().month + 1}')
                due_year = int(f'{datetime.datetime.today().year}')

                while due_month > 12:
                    due_month -= 12
                    due_year += 1

                if loan.checking_user():
                    loan.first_name = auth.first_name
                    loan.last_name = auth.last_name
                    loan.email = auth.email
                    loan.phone_number = auth.phone_number
                    loan.address = auth.address
                    loan.date_of_birth = auth.date_of_birth
                    loan.add_users()
                loan.add_loan(
                    loan_type=_type[1],
                    loan_status=1,
                    amount=_interest + amount,
                    interest_rate=interest,
                    monthly_payment=float(payment_period),
                    start_date=f'{datetime.datetime.today().year}-{datetime.datetime.today().month}-'
                               f'{datetime.datetime.today().day}',
                    due_date=f'{due_year}-{due_month}-{datetime.datetime.today().day}',
                    end_date=f'{end_date[:4]}-{end_date[5:7]}-{end_date[8:]}'
                )
                countdown_timer(_register='Loan', _duty='Payment', countdown=5)
                deposit_default(auth,
                                _amount=_interest + amount,
                                _description=f'LOAN/CBB/DEPOSIT TO {auth.account_holder}')
                loan_receipt(auth, f'{month} {datetime.datetime.today().day}, {end_date[:4]}',
                             _type[0], total_payment, interest, _repayment_period, payment_period)
                break
            elif re.search('^2$', _input, re.IGNORECASE):
                print('\n:: Loan Terms Rejected')
                sleep(2.5)
                break
            else:
                print(f"\n:: Wrong Input")
                sleep(1.5)
                continue
    except Exception as e:
        log_error(e)
        go_back('script')


def types_of_loans(auth: Authentication):
    try:
        while True:
            header()
            print('\nWhat Type of Loan do you want?')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

            print('\n+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print('|      1. Personal Loan     |        2. Mortgage Loan        |        3. Auto Loan        |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print('|      4. Student Loan      |     5. Small Business Loan     |       6. Payday Loan       |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print('|    7. Home Equity Loan    |   8. Debt Consolidation Loan   |   9. Credit Builder Loan   |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print('|   10. Peer to Peer Loan   |         11. Title Loan         |       12. Bridge Loan      |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input('>>> ')

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                break
            else:
                amount, _repayment_period = loan_questions()
                if re.search('^1$', user_input, re.IGNORECASE):
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
                    print(f"\n:: Wrong Input")
                    sleep(1.5)
                    continue
    except Exception as e:
        log_error(e)
        go_back('script')


def preview(auth: Authentication):
    try:
        while True:
            header()

            print('\n+~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+')
            print('|   1. COLLECT LOAN   |   2. LOAN CALCULATOR   |')
            print('+~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input('>>> ')

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                break
            elif re.search('^1$', user_input, re.IGNORECASE):
                types_of_loans(auth)
                continue
            elif re.search('^2$', user_input, re.IGNORECASE):
                loan_calculator()
                continue
            else:
                print(f"\n:: Wrong Input")
                sleep(1.5)
                continue
    except Exception as e:
        log_error(e)
        go_back('script')
