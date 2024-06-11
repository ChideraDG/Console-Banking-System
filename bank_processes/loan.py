import datetime
import time

from bank_processes.database import DataBase


class Loan(DataBase):
    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, phone_number=None, address=None,
                 date_of_birth: str = None, due_date: str = None, end_date: str = None):
        self.__user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.date_of_birth = date_of_birth
        self.__due_date = due_date
        self.__end_date = end_date

    def add_users(self):
        query = f"""
        INSERT INTO {self.db_tables[6]}
        (first_name, last_name, email, phone_number, address, date_of_birth)
        VALUES('{self.first_name}', '{self.last_name}', '{self.email}', '{self.phone_number}', '{self.address}', 
        '{self.date_of_birth}')
        """

        self.query(query)

    def checking_user(self):
        query = f"""
        SELECT * 
        FROM {self.db_tables[6]}
        WHERE email = '{self.email}'
        """

        datas = self.fetch_data(query)

        if datas:
            return False
        else:
            return True

    def add_loan(self, *, loan_type: int, loan_status: int, amount: float, interest_rate: float, start_date: str,
                 due_date: str, end_date: str):
        query = f"""
                INSERT INTO {self.db_tables[7]}
                (user_id, loan_type_id, amount, interest_rate, start_date, due_date, end_date, status_id)
                VALUES({self.user_id}, {loan_type}, '{amount}', '{interest_rate}', '{start_date}', '{due_date}', 
                '{end_date}', {loan_status})
            """

        self.query(query)

    def check_loan(self):
        # for loop for each user_id loan status_id
        if datetime.datetime.today().date() > datetime.date(
                self.due_date[:4], int(self.due_date[5:7]), int(self.due_date[8:])) < datetime.date(
                self.end_date[:4], int(self.end_date[5:7]), int(self.end_date[8:])):
            pass

    @property
    def user_id(self):
        if self.email is not None:
            query = (f"""
            SELECT user_id 
            FROM {self.db_tables[6]} 
            WHERE email = '{self.email}'
            """)

            datas: tuple = self.fetch_data(query)

            for data in datas:
                for user_id in data:
                    self.user_id = user_id

        return self.__user_id

    @user_id.setter
    def user_id(self, _user_id):
        self.__user_id = _user_id

    @property
    def due_date(self):
        if self.user_id is not None:
            query = (f"""
            SELECT due_date 
            FROM {self.db_tables[6]} 
            WHERE user_id = '{self.user_id}'
            """)

            datas: tuple = self.fetch_data(query)

            for data in datas:
                for due_date in data:
                    self.due_date = due_date

        return self.__user_id

    @due_date.setter
    def due_date(self, _due_date):
        self.__due_date = _due_date

    @property
    def end_date(self):
        if self.user_id is not None:
            query = (f"""
            SELECT end_date 
            FROM {self.db_tables[6]} 
            WHERE user_id = '{self.user_id}'
            """)

            datas: tuple = self.fetch_data(query)

            for data in datas:
                for end_date in data:
                    self.end_date = end_date

        return self.__user_id

    @end_date.setter
    def end_date(self, _end_date):
        self.__end_date = _end_date
