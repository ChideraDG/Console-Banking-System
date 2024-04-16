class DataBase:
    db_connection = None  # Connection object or parameters required to establish a connection to the database server.
    db_name = None  # Name of the database storing bank-related data.
    db_tables = None  # List of tables within the database, representing different entities such as users, acc., etc.
    db_credentials = None  # Credentials (e.g., username, password) required to authenticate and access the database.
    db_config_settings = None  # Configuration settings for database connections, such as host and port.
    data_models = None  # Class definitions representing database tables, mapping attributes to database columns.
    db_cursor = None  # Cursor object for executing SQL queries and interacting with the database.
    query_logs = None  # Log to record SQL queries executed against the database, for debugging and auditing purposes.

    @classmethod
    def connect(cls):
        """Method to establish a connection to the database server, including authentication and authorization if
        required."""
        pass

    @classmethod
    def disconnect(cls):
        """Method to gracefully close the connection to the database server, releasing any resources allocated by the
        connection."""
        pass

    @classmethod
    def query(cls):
        """Method to execute SQL queries against the database, allowing for data retrieval, insertion, updating,
        and deletion operations."""
        pass

    @classmethod
    def fetch_data(cls):
        """Method to retrieve data from the database in response to a query, returning the results in a structured
        format such as lists, dictionaries, or objects."""
        pass

    @classmethod
    def commit(cls):
        """Method to commit changes made within a transaction to the database, persisting the changes permanently."""
        pass

    @classmethod
    def rollback(cls):
        """Method to rollback changes made within a transaction, reverting the database to its state before the
        transaction started."""
        pass



