from typing import Tuple, Any

import pymysql as sql


class DataBase:
    db_name = {'database': 'bankApp_db'}  # Name of the database storing bank-related data.
    db_tables = [
        'Bank_Verification_Number', 'User', 'Transaction', 'Account', 'Fixed_Deposit', 'Central_Bank', 'LoanUsers',
        'Loans', 'LoansPayments',
    ]  # List of tables within the db, representing different entities.

    # Credentials (e.g., username, password) required to authenticate and access the database.
    db_credentials = {
        'username': 'root',
        'password': ''
    }

    # Configuration settings for database connections, such as host and port.
    db_config_settings = {
        'host': 'localhost'
    }

    # Connection object or parameters required to establish a connection to the database server.
    db_connection = sql.connect(
            host=db_config_settings['host'],
            user=db_credentials['username'],
            password=db_credentials['password'],
            database=db_name['database']
        )

    db_cursor = db_connection.cursor()  # Cursor object for executing SQL queries and interacting with the database.
    data_models = None  # Class definitions representing database tables, mapping attributes to database columns.

    @classmethod
    def disconnect(cls):
        """Method to gracefully close the connection to the database server, releasing any resources allocated by the
        connection."""

        cls.db_cursor.close()

    @classmethod
    def query(cls, query):
        """Method to execute SQL queries against the database, allowing for data retrieval, insertion, updating,
        and deletion operations."""

        cls.db_cursor.execute(query)
        cls.commit()

    @classmethod
    def fetch_data(cls, query) -> tuple[tuple[Any, ...], ...]:
        """Retrieve data from the database in response to a query.

        This method executes the provided SQL query using the database cursor,
        fetches all the results, and returns them in a structured format.

        Parameters
        ----------
        query : str
            The SQL query to be executed.

        Returns
        -------
        tuple[tuple[Any, ...], ...]
            The fetched data from the database, returned as a tuple of tuples.
        """
        # Execute the provided query
        cls.db_cursor.execute(query)
        # Fetch all results from the executed query
        data = cls.db_cursor.fetchall()

        # Return the fetched data
        return data

    @classmethod
    def commit(cls):
        """Persist changes made within a transaction to the database.

        This method commits all the changes made during the current transaction
        to the database, making the changes permanent.

        Usage
        -----
        - Typically called after a series of database operations that should
          be saved as a single transaction.
        - Ensures that all changes are written to the database.
        """
        cls.db_connection.commit()

    @classmethod
    def rollback(cls):
        """Revert the database to its state before the transaction.

        This method rolls back any changes made during the current transaction,
        reverting the database to its state before the transaction started.

        Usage
        -----
        - Typically called in error-handling scenarios to undo changes made
          during a failed transaction.
        - Helps maintain data integrity by reverting to a consistent state.

        """
        cls.db_connection.rollback()
