import time
from datetime import datetime
from bank_processes.authentication import Authentication
from banking.script import log_error, go_back, header


def transaction_history(auth: Authentication):
    try:
        while True:
            header()

            print('\nChoose a Criteria:\n~~~~~~~~~~~~~~~~~~\n')
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

            table = auth.transaction_history(start_date=datetime(2024, 6, 1, 0, 0, 0),
                                             end_date=datetime(2024, 6, 15, 23, 0, 0), time_period=True)

            print(table)

    except Exception as e:
        log_error(e)
        go_back('script')


def generate_statement():
    try:
        while True:
            header()
    except Exception as e:
        log_error(e)
        go_back('script')