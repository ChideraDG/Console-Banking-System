import datetime
from bank_processes.database import DataBase


class BVN:
    __nationality: str = 'Nigeria'  # User's country of origin

    def __init__(self, bvn_number: str = None, first_name: str = None, middle_name: str = None, last_name: str = None,
                 gender: str = None, address: str = None, email: str = None, phone_number: str = None,
                 date_of_birth: str = None, created_date: datetime.datetime = None,
                 last_updated: datetime.datetime = None, bvn_status: str = None):
        self.database = DataBase
        self.__bvn_number = bvn_number  # User's Bank Verification Number
        self.__first_name = first_name  # User's First Name
        self.__middle_name = middle_name  # User's Middle Name
        self.__last_name = last_name  # User's Last Name
        self.__gender = gender  # User's Gender
        self.__address = address  # User's Address
        self.__email = email  # User's E-mail
        self.__phone_number = phone_number  # User's Phone Number
        self.__date_of_birth = date_of_birth  # User's Date of Birth
        self.__created_date = created_date  # Date this BVN was created
        self.__last_updated = last_updated  # Date this BVN was last updated
        self.__bvn_status = bvn_status  # User's Status Code (active, inactive, suspended)

    def register_bvn(self):
        """Method to register a new Bank Verification Number for a user, capturing their personal information and
        biometric data."""

        try:
            query = f"""
            INSERT INTO {self.database.db_tables[0]}
            (first_name, middle_name, last_name, gender, address, phone_number, date_of_birth, nationality, email,
            bvn_number, created_date, last_updated, bvn_status)
            VALUES
            ('{self.__first_name}', '{self.__middle_name}', '{self.__last_name}', '{self.__gender}', '{self.__address}', 
            '{self.__phone_number}', '{self.__date_of_birth}', '{self.__nationality}', '{self.__email}', 
            '{self.__bvn_number}', '{self.__created_date}', '{self.__last_updated}', '{self.__bvn_status}')
            """

            self.database.query(query)
        except Exception as e:
            # Rollback changes if an error occurs
            self.database.rollback()

    def verify_bvn(self):
        """Method to verify the authenticity of a BVN, validating it against the central database or authority to
        ensure it is valid and active."""
        pass

    def update_bvn(self, *, _column_name: str, _data: str, _id_number: int):
        """
        Method to update the information associated with a BVN, such as personal details or biometric data,
        ensuring the data remains accurate and up to date.

        Parameters
        ----------
        _column_name : str
            The name of the column to update.
        _data : str
            The new data to be inserted into the specified column.
        _id_number : int
            The ID number identifying the specific BVN record to be updated.
        """

        # Construct the SQL query as a formatted string
        query = f"""
        UPDATE {self.database.db_tables[0]} 
        SET {_column_name} = '{_data}', last_updated = '{datetime.datetime.today().now()}'
        WHERE id = {_id_number}
        """

        # Execute the query using the database's query method
        self.database.query(query)

    def link_bvn_to_account(self):
        """Method to link a BVN to a user's bank account, enabling seamless identification and verification during
        account-related transactions."""
        pass

    def get_bvn_verification(self, column_id: int):
        """Method to retrieve information associated with a BVN, including personal details, linked accounts,
        and verification status."""
        query = (f"""
                    SELECT bvn_number
                    FROM {self.database.db_tables[0]} 
                    WHERE id = {column_id}
                    """)

        datas: tuple = self.database.fetch_data(query)

        for data in datas:
            for bvn in data:
                self.bvn_number = bvn

    def deactivation(self):
        """Method to deactivate or suspend a BVN, typically in cases of fraud, identity theft, or other security
        concerns."""
        pass

    def reactivation(self):
        """Method to re-activate a previously deactivated BVN, once any issues or concerns have been resolved and the
        BVN is deemed valid again."""
        pass

    def delete_bvn(self):
        """Method to permanently delete a BVN record from the system, typically in cases where the BVN is no longer
        required or has been replaced."""
        pass

    def authenticate_bvn(self):
        """Method to authenticate the identity of a user based on their BVN, verifying their identity during
        account-related transactions or authentication processes."""
        pass

    @property
    def bvn_number(self):
        return self.__bvn_number

    @bvn_number.setter
    def bvn_number(self, _bvn_number):
        self.__bvn_number = _bvn_number

    @bvn_number.deleter
    def bvn_number(self):
        del self.__bvn_number

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, _first_name):
        self.__first_name = _first_name

    @first_name.deleter
    def first_name(self):
        del self.__first_name

    @property
    def middle_name(self):
        return self.__middle_name

    @middle_name.setter
    def middle_name(self, _middle_name):
        self.__middle_name = _middle_name

    @middle_name.deleter
    def middle_name(self):
        del self.__middle_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, _last_name):
        self.__last_name = _last_name

    @last_name.deleter
    def last_name(self):
        del self.__last_name

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, _gender):
        self.__gender = _gender

    @gender.deleter
    def gender(self):
        del self.__gender

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, _address):
        self.__address = _address

    @address.deleter
    def address(self):
        del self.__address

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, _email):
        self.__email = _email

    @email.deleter
    def email(self):
        del self.__email

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, _phone_number):
        self.__phone_number = _phone_number

    @phone_number.deleter
    def phone_number(self):
        del self.__phone_number

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, _date_of_birth):
        self.__date_of_birth = _date_of_birth

    @date_of_birth.deleter
    def date_of_birth(self):
        del self.__date_of_birth

    @property
    def created_date(self):
        return self.__created_date

    @created_date.setter
    def created_date(self, _created_date):
        self.__created_date = _created_date

    @created_date.deleter
    def created_date(self):
        del self.__created_date

    @property
    def last_updated(self):
        return self.__last_updated

    @last_updated.setter
    def last_updated(self, _last_updated):
        self.__last_updated = _last_updated

    @last_updated.deleter
    def last_updated(self):
        del self.__last_updated

    @property
    def bvn_status(self):
        return self.__bvn_status

    @bvn_status.setter
    def bvn_status(self, _bvn_status):
        self.__bvn_status = _bvn_status

    @bvn_status.deleter
    def bvn_status(self):
        del self.__bvn_status
