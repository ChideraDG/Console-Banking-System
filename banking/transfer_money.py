import re
from bank_processes.account import Savings, Current
from bank_processes.authentication import Authentication
from banking.script import header


def beneficiaries(auth: Authentication):
    while True:
        beneficiary = auth.beneficiaries

        print(end='\n')

        for account_number, account_name in beneficiary.items():
            print(f'{account_number} - {account_name[0]} : {account_name[1]}')
            print('    ~~~', "~" * (len(account_name[0]) + len(account_name[1])), sep='')

        print("Pick a Beneficiary:")
        _input = input('>>> ')

        if re.search("^\\D$", _input):
            print('here')
            continue

        if int(_input) <= len(beneficiary):
            for key in beneficiary.keys():
                if int(_input) == key:
                    return beneficiary[key]
        else:
            continue


def process_transfer(auth: Authentication):
    savings = Savings()
    current = Current()

    header()

    while True:
        break

    if auth.account_type == 'savings':
        savings.transfer()
    elif auth.account_type == 'current':
        current.transfer()
    else:
        raise TypeError("Account Type doesn't exist")
