import pymysql as sql

connection = sql.connect(
    host='localhost',
    user='root',
    password='',
    database='bankApp_db'
)

my_cursor = connection.cursor()

queries = [
    """
    CREATE TABLE Users (
        user_id INT PRIMARY KEY AUTO_INCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        phone_number VARCHAR(15),
        address VARCHAR(255),
        date_of_birth DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE LoanTypes (
        loan_type_id INT PRIMARY KEY AUTO_INCREMENT,
        type_name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE LoanStatus (
        status_id INT PRIMARY KEY AUTO_INCREMENT,
        status_name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE Loans (
        loan_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT,
        loan_type_id INT,
        amount DECIMAL(15, 2) NOT NULL,
        interest_rate DECIMAL(5, 2) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        status_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (loan_type_id) REFERENCES LoanTypes(loan_type_id),
        FOREIGN KEY (status_id) REFERENCES LoanStatus(status_id)
    );
    """,
    """
    CREATE TABLE Payments (
        payment_id INT PRIMARY KEY AUTO_INCREMENT,
        loan_id INT,
        amount DECIMAL(15, 2) NOT NULL,
        payment_date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (loan_id) REFERENCES Loans(loan_id)
    );
    """
]

for query in queries:
    my_cursor.execute(query)

my_cursor.close()
