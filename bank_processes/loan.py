from bank_processes.database import DataBase


class Loan(DataBase):
    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, phone_number=None, address=None,
                 date_of_birth: str = None):
        self.__user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.date_of_birth = date_of_birth

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

    def add_loan(self, *, loan_type: int, loan_status: int, amount: float, interest_rate: float, start_date, end_date):
        query = f"""
                INSERT INTO {self.db_tables[7]}
                (user_id, loan_type_id, amount, interest_rate, start_date, end_date, status_id)
                VALUES({self.user_id}, {loan_type}, '{amount}', '{interest_rate}', '{start_date}', '{end_date}', 
                {loan_status})
            """

        self.query(query)

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
                    self.__user_id = user_id

        return self.__user_id

    @user_id.setter
    def user_id(self, _user_id):
        self.__user_id = _user_id
