import datetime
import enum

from bank_processes.database import DataBase


class BVN:
    nationality: str = 'Nigeria'  # user's country of origin

    def __init__(self, bvn_number: str = None, first_name: str = None, middle_name: str = None, last_name: str = None,
                 gender: str = None, address: str = None, email: str = None, phone_number: str = None,
                 date_of_birth: str = None, created_date: datetime.datetime = None,
                 last_updated: datetime.datetime = None, bvn_status: str = None):
        self.database = DataBase
        self.bvn_number = bvn_number  # Users Bank Verification Number
        self.first_name = first_name  # user's first name
        self.middle_name = middle_name  # user's middle name
        self.last_name = last_name  # user's last name
        self.gender = gender  # user's gender
        self.address = address  # user's address
        self.email = email  # user's email
        self.phone_number = phone_number  # user's phone number
        self.date_of_birth = date_of_birth  # user's date of birth
        self.created_date = created_date  # date this bvn was created
        self.last_updated = last_updated  # date this bvn was last updated
        self.bvn_status = bvn_status  # user's status code (active, inactive, suspended)

    def register_bvn(self):
        """Method to register a new Bank Verification Number for a user, capturing their personal information and
        biometric data."""

        query = f"""
        insert into {self.database.db_tables[0]}
        (first_name, middle_name, last_name, address, phone_number, date_of_birth, nationality, email,
        bvn_number, created_date, last_updated, bvn_status)
        values('{self.first_name}', '{self.middle_name}', '{self.last_name}', '{self.address}', '{self.phone_number}',
        '{self.date_of_birth}', '{self.nationality}', '{self.email}', '{self.bvn_number}', '{self.created_date}',
        '{self.last_updated}', '{self.bvn_status}')
        """

        self.database.query(query)

    def verify_bvn(self):
        """Method to verify the authenticity of a BVN, validating it against the central database or authority to
        ensure it is valid and active."""
        pass

    def update_bvn(self):
        """Method to update the information associated with a BVN, such as personal details or biometric data,
        ensuring the data remains accurate and up to date."""
        pass

    def link_bvn_to_account(self):
        """Method to link a BVN to a user's bank account, enabling seamless identification and verification during
        account-related transactions."""
        pass

    def get_bvn_verification(self):
        """Method to retrieve information associated with a BVN, including personal details, linked accounts,
        and verification status."""
        pass

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
