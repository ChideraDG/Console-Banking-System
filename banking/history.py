import re
import time
from datetime import datetime, date
from bank_processes.authentication import Authentication
from banking.script import log_error, go_back, header


def get_month_details(month_of_birth: int):
    """
    Returns the month name and the number of days in that month for a given year.

    Parameters
    ----------
    month_of_birth : int
        The month number (1 for January, 2 for February, etc.).
    max_year : int
        The year to consider for determining the number of days in February.

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


def by_date(*, current_year):
    try:
        def get_dates(title: str):
            header()

            print(f"\n{title.upper()} DATE:")
            print(f"~~~~~~{'~' * len(title)}")

            while True:
                print("\nInput the Year:")
                print("~~~~~~~~~~~~~~~")
                year = input(">>> ").strip()

                if re.search('^.*(back|return).*$', year, re.IGNORECASE):
                    return 'break'
                else:
                    if year.isdigit():
                        if 1900 < int(year) <= current_year:
                            break
                        elif not 1900 < int(year):
                            print("\n:: Invalid input\n:: Year is less than 1900")
                        elif not int(year) <= current_year:
                            print(f"\n:: Invalid input\n:: Year is greater than {current_year}")
                    else:
                        print(f"\n:: {title.title()} Year should be in digits.\nExample: 2001, 2004, etc.")
                    time.sleep(2)
                    continue

            while True:
                print("\nInput the Month:")
                print("~~~~~~~~~~~~~~~~")
                month = input(">>> ").strip()

                if re.search('^.*(back|return).*$', month, re.IGNORECASE):
                    return 'break'
                else:
                    if month.isdigit():
                        if year == str(current_year):
                            current_month = datetime.today().month
                        else:
                            current_month = 12

                        if 0 < int(month) <= current_month:
                            break
                        elif not 0 < int(month):
                            print("\n:: Invalid input\n:: Month is less than 1")
                        elif not int(month) <= current_month:
                            print(f"\n:: Invalid input\n:: Month is greater than {current_month}")
                    else:
                        print(f"\n:: {title.title()} Month should be in digits.\nExample: 1, 4, etc.")
                    time.sleep(2)
                    continue

            while True:
                print("\nInput the Day:")
                print("~~~~~~~~~~~~~~")
                day = input(">>> ").strip()

                if re.search('^.*(back|return).*$', day, re.IGNORECASE):
                    return 'break'
                else:
                    if day.isdigit():
                        if year == str(current_year):
                            current_day = datetime.today().day
                        else:
                            current_day = get_month_details(int(month))[1]

                        if 0 < int(day) <= current_day:
                            break
                        else:
                            print(f"\n:: Day of Birth should be within the number of days in "
                                  f"{get_month_details(int(month))[0]} in {year}.")
                    else:
                        print(f"\n:: {title.title()} Day should be in digits.\nExample: 1, 4, etc.")
                    time.sleep(2)
                    continue

            return f'{year}-{month}-{day}'

        start_date = get_dates('start')
        if start_date == 'break':
            return 'break'

        end_date = get_dates('end')
        if end_date == 'break':
            return 'break'

        if (date(
                year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]),
                day=int(start_date.split('-')[2]))
                > date(
                    year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]),
                    day=int(end_date.split('-')[2]))):
            print("\n:: Start Date cannot be greater than End Date")
            time.sleep(2)

            by_date(current_year=datetime.today().year)

        return start_date, end_date
    except Exception as e:
        log_error(e)
        go_back('script')


def process_transaction_history(*, auth: Authentication, criteria: str = 'all', start_date: str = None,
                                end_date: str = None, start_month: str = None, end_month: str = None):
    header()

    if criteria == 'date':
        print(auth.transaction_history(start_date=datetime(int(start_date.split('-')[0]), int(start_date.split('-')[1]),
                                                           int(start_date.split('-')[2]), 0, 0, 0),
                                       end_date=datetime(int(end_date.split('-')[0]), int(end_date.split('-')[1]),
                                                         int(end_date.split('-')[2]), 23, 59, 59), time_period=True))
    elif criteria == 'all':
        auth.transaction_history()


def transaction_history(auth: Authentication):
    # table = auth.transaction_history(start_date=datetime(2024, 6, 1, 0, 0, 0),
    #                                  end_date=datetime(2024, 6, 16, 23, 0, 0), time_period=True)
    try:
        while True:
            header()

            print('\nChoose a Criteria:\n~~~~~~~~~~~~~~~~~~\n')
            print("+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")
            print("|     1. BY DATE     |     2. BY MONTH     |")
            print("+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~+")
            print("|         3. ALL TRANSACTION HISTORY       |")
            print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
            user_input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                time.sleep(1)
                break
            elif re.search('^1$', user_input):
                dates = by_date(
                    current_year=datetime.today().year,
                )
                if dates == 'break':
                    continue
                else:
                    process_transaction_history(
                        auth=auth,
                        criteria='date',
                        start_date=dates[0],
                        end_date=dates[1]
                    )
                    break
            elif re.search('^2$', user_input):
                continue
            else:
                print("\n:: Invalid input, please try again.")
                time.sleep(2)
                continue

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
