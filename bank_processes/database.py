import pymysql as sql


class DataBase:
    db_name = {'database': 'bankApp_db'}  # Name of the database storing bank-related data.

    # Credentials (e.g., username, password) required to authenticate and access the database.
    db_credentials = {
        'username': 'Chidera',
        'password': 'admin'
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

    def __init__(self, data_models: dict = None, db_tables: list = None):
        self.db_tables = db_tables  # List of tables within the database, representing different entities such as users, acc., etc.
        self.data_models = data_models  # Class definitions representing database tables, mapping attributes to database columns.

    @classmethod
    def connect(cls):
        """Method to establish a connection to the database server, including authentication and authorization if
        required."""

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
        cls.disconnect()

    @classmethod
    def fetch_data(cls, query):
        """Method to retrieve data from the database in response to a query, returning the results in a structured
        format such as lists, dictionaries, or objects."""
        pass

    @classmethod
    def commit(cls):
        """Method to commit changes made within a transaction to the database, persisting the changes permanently."""

        cls.db_connection.commit()

    @classmethod
    def rollback(cls):
        """Method to rollback changes made within a transaction, reverting the database to its state before the
        transaction started."""
        pass



