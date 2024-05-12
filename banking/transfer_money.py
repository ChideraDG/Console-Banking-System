import json
import re
import time
from bank_processes.authentication import Authentication
from banking.script import header, go_back


def beneficiaries(auth: Authentication):
    while True:
        beneficiary = json.loads(auth.beneficiaries)

        print(end='\n')
        if beneficiary:
            header()
            print('\n')

            for account_number, account_name in beneficiary.items():
                print(f'{account_number} - {account_name[0]} : {account_name[1]}')
                print('    ~~~', "~" * (len(account_name[0]) + len(account_name[1])), sep='')

            print("\nPick a Beneficiary:")
            _input = input('>>> ')

            if re.search("^\\D$", _input):
                print('here')
                continue

            if int(_input) <= len(beneficiary):
                for key in beneficiary.keys():
                    if _input == key:
                        return beneficiary[key]
            else:
                continue
        else:
            return ':: Empty'


def recipient_account_number(auth: Authentication):
    while True:
        header()
        print(end='\n')
        print("\nENTER YOUR RECIPIENT ACCOUNT NUMBER:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        _input = input(">>> ")

        auth.transaction_validation()


def process_transfer(auth: Authentication):

    if auth.transaction_limit > 0:
        while True:
            header()
            # To Bank or To Beneficiaries
            print(end='\n')
            print(" ~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~ ")
            print("|  1. to BANK  |  2. to BENEFICIARY  |")
            print(" ~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~ ")
            user_input = input(">>> ")

            if re.search('^1$', user_input):
                pass
            elif re.search('^2$', user_input):
                bene = beneficiaries(auth)
                if bene == ':: Empty':
                    print('\n' + bene)
                    time.sleep(3)
                    continue
                else:
                    print(bene)
                    time.sleep(5)
                    break
            else:
                continue
    else:
        print("\n:: Daily Transaction Limit Exceeded")
        time.sleep(3)
        go_back('signed_in', auth=auth)
    # if auth.account_type == 'savings':
    #     auth.transfer()
    # elif auth.account_type == 'current':
    #     auth.transfer()
    # else:
    #     raise TypeError("Account Type doesn't exist")
