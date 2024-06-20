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

    def add_user(self):
        """
        Adds a new user to the database.

        Notes
        -----
        This method constructs and executes an SQL query to insert user information into the database table.
        """
        query = f"""
        INSERT INTO {self.db_tables[6]}
        (first_name, last_name, email, phone_number, address, date_of_birth)
        VALUES('{self.first_name}', '{self.last_name}', '{self.email}', '{self.phone_number}', '{self.address}', 
        '{self.date_of_birth}')
        """
        self.query(query)  # Assuming self.query is a method to execute the query

    def check_user_existence(self):
        """
        Checks if a user already exists in the database based on their email.

        Returns
        -------
        bool
            True if the user does not exist (can be added), False if the user already exists.

        Notes
        -----
        This method constructs and executes an SQL query to select user data based on email.
        It returns True if no data is found (user does not exist), otherwise False.
        """
        query = f"""
        SELECT * 
        FROM {self.db_tables[6]}
        WHERE email = '{self.email}'
        """

        data = self.fetch_data(query)  # Assuming self.fetch_data retrieves data from the database

        return not bool(data)  # Return True if data is empty (user does not exist), False otherwise

    def add_loan(self, *, loan_type: int, loan_status: int, amount: float, interest_rate: float, start_date: str,
                 due_date: str, end_date: str, monthly_payment: float):
        """
        Add a new loan record to the loans table in the database.

        Parameters
        ----------
        loan_type : int
            The type of loan (e.g., personal, mortgage, etc.).
        loan_status : int
            The status of the loan (e.g., active, completed, etc.).
        amount : float
            The total amount of the loan.
        interest_rate : float
            The annual interest rate for the loan.
        start_date : str
            The start date of the loan.
        due_date : str
            The due date for the first payment.
        end_date : str
            The end date of the loan.
        monthly_payment : float
            The monthly payment amount.

        Returns
        -------
        None
        """
        query = f"""
                INSERT INTO {self.db_tables[7]}
                (user_id, loan_type_id, amount, interest_rate,monthly_payment, start_date, due_date, end_date, 
                status_id)
                VALUES({self.user_id}, {loan_type}, '{amount}', '{interest_rate}', '{monthly_payment}', '{start_date}', 
                '{due_date}', '{end_date}', {loan_status})
            """

        self.query(query)

    def make_loan_payments(self, *, loan_id: int, amount: float, payment_date: str):
        """
        Record a loan payment in the loan payments table in the database.

        Parameters
        ----------
        loan_id : int
            The ID of the loan for which the payment is being made.
        amount : float
            The amount of the payment.
        payment_date : str
            The date of the payment.

        Returns
        -------
        None
        """
        query = f"""
                 INSERT INTO {self.db_tables[8]}
                 (loan_id, amount, payment_date)
                 VALUES
                 ({loan_id}, '{amount}', '{payment_date}')
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
                    self.user_id = user_id

        return self.__user_id

    @user_id.setter
    def user_id(self, _user_id):
        self.__user_id = _user_id

    @user_id.deleter
    def user_id(self):
        del self.__user_id
