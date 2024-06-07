import os
import re
import sys
from time import sleep
from bank_processes.authentication import Authentication
from banking.fixed_deposit import calculate_interest
from banking.register_panel import countdown_timer
from banking.script import go_back, header


def log_error(error: Exception):
    """Logs errors to a file."""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    with open('notification/error.txt', 'w') as file:
        file.write(f'{exc_type}, \n{os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]}, \n{exc_tb.tb_lineno}, '
                   f'\nError: {repr(error)}')
    print(f'\nError: {repr(error)}')
    sleep(3)


def repayment_period():
    while True:
        sleep(0.5)

        print('\nRepayment period in months: (2 means Two months)')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        period = input('>>> ')

        if re.search('^.*(back|return).*$', period, re.IGNORECASE):
            return 'preview'

        # Ensure the input is a valid number
        elif re.search("^[0-9]{1,2}$", period, re.IGNORECASE):
            if int(period) > 12:
                print(f"\n:: Wrong Month Input")
                sleep(1)
                continue
            else:
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
    try:
        while True:
            header()

            print('\nAmount of the Loan: (Naira)')
            print('~~~~~~~~~~~~~~~~~~~')
            print(f':: {_loan_amount}\n')

            print('\nAnnual percentage rate of interest: (%)')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(f':: {_annual_rate}\n')

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
                days=period*30
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


def preview():
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

# preview()