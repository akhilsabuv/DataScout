import sqlalchemy
from sqlalchemy import create_engine, text
import logging
from faker import Faker
import random
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

fake = Faker()

# Database Credentials
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "StrongMySQLRoot!23",
    "database": "mysqlTest"
}

MSSQL_CONFIG = {
    "host": "localhost",
    "port": 1433,
    "user": "sa",
    "password": "StrongPassw0rd!",
    "database": "mssqlTest"
}

POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "user": "postgres",
    "password": "postgres", 
    "database": "postgresqltest"
}

def get_engine_url(db_type, config):
    if db_type == 'mysql':
        return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    elif db_type == 'mssql':
        return f"mssql+pymssql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    elif db_type == 'postgresql':
        return f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    return None

def seed_mysql(config):
    logging.info("--- Seeding MySQL (E-commerce Theme) ---")
    engine = create_engine(get_engine_url('mysql', config))
    with engine.connect() as conn:
        # Drop tables if exist to ensure clean state
        conn.execute(text("DROP TABLE IF EXISTS orders"))
        conn.execute(text("DROP TABLE IF EXISTS customers"))
        
        # Create Tables
        conn.execute(text("""
            CREATE TABLE customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                address TEXT,
                email VARCHAR(255)
            )
        """))
        conn.execute(text("""
            CREATE TABLE orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                order_date DATETIME,
                amount DECIMAL(10, 2),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """))
        
        # Generate Data
        logging.info("Generating 10,000 customers...")
        customers = []
        for _ in range(10000):
            customers.append({
                "name": fake.name(),
                "address": fake.address(),
                "email": fake.email()
            })
        
        # Batch insert customers
        conn.execute(
            text("INSERT INTO customers (name, address, email) VALUES (:name, :address, :email)"),
            customers
        )
        
        logging.info("Generating 10,000 orders...")
        orders = []
        for _ in range(10000):
            orders.append({
                "customer_id": random.randint(1, 10000),
                "order_date": fake.date_time_between(start_date='-1y', end_date='now'),
                "amount": round(random.uniform(10.0, 1000.0), 2)
            })
            
        conn.execute(
            text("INSERT INTO orders (customer_id, order_date, amount) VALUES (:customer_id, :order_date, :amount)"),
            orders
        )
        conn.commit()
        logging.info("MySQL seeding completed.")

def seed_mssql(config):
    logging.info("--- Seeding MSSQL (HR/Corporate Theme) ---")
    engine = create_engine(get_engine_url('mssql', config))
    with engine.connect() as conn:
        # Drop tables
        conn.execute(text("IF OBJECT_ID('payroll', 'U') IS NOT NULL DROP TABLE payroll"))
        conn.execute(text("IF OBJECT_ID('employees', 'U') IS NOT NULL DROP TABLE employees"))
        
        # Create Tables
        conn.execute(text("""
            CREATE TABLE employees (
                id INT IDENTITY(1,1) PRIMARY KEY,
                full_name VARCHAR(255),
                job_title VARCHAR(255),
                department VARCHAR(255),
                hire_date DATE
            )
        """))
        conn.execute(text("""
            CREATE TABLE payroll (
                id INT IDENTITY(1,1) PRIMARY KEY,
                employee_id INT,
                salary DECIMAL(10, 2),
                bonus DECIMAL(10, 2),
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        """))
        
        # Generate Data
        logging.info("Generating 10,000 employees...")
        employees = []
        for _ in range(10000):
            employees.append({
                "full_name": fake.name(),
                "job_title": fake.job(),
                "department": fake.job(), # Using job as department proxy for simplicity or fake.bs()
                "hire_date": fake.date_between(start_date='-5y', end_date='today')
            })
            
        conn.execute(
            text("INSERT INTO employees (full_name, job_title, department, hire_date) VALUES (:full_name, :job_title, :department, :hire_date)"),
            employees
        )
        
        logging.info("Generating 10,000 payroll records...")
        payroll = []
        for i in range(1, 10001):
            payroll.append({
                "employee_id": i,
                "salary": round(random.uniform(50000, 150000), 2),
                "bonus": round(random.uniform(0, 20000), 2)
            })
            
        conn.execute(
            text("INSERT INTO payroll (employee_id, salary, bonus) VALUES (:employee_id, :salary, :bonus)"),
            payroll
        )
        conn.commit()
        logging.info("MSSQL seeding completed.")

def seed_postgres(config):
    logging.info("--- Seeding PostgreSQL (App Analytics Theme) ---")
    engine = create_engine(get_engine_url('postgresql', config))
    with engine.connect() as conn:
        # Drop tables
        conn.execute(text("DROP TABLE IF EXISTS activity_logs"))
        conn.execute(text("DROP TABLE IF EXISTS user_sessions"))
        
        # Create Tables
        conn.execute(text("""
            CREATE TABLE user_sessions (
                id SERIAL PRIMARY KEY,
                session_token VARCHAR(255),
                ip_address VARCHAR(50),
                login_time TIMESTAMP
            )
        """))
        conn.execute(text("""
            CREATE TABLE activity_logs (
                id SERIAL PRIMARY KEY,
                session_id INT,
                action VARCHAR(255),
                details TEXT,
                FOREIGN KEY (session_id) REFERENCES user_sessions(id)
            )
        """))
        
        # Generate Data
        logging.info("Generating 10,000 user sessions...")
        sessions = []
        for _ in range(10000):
            sessions.append({
                "session_token": fake.uuid4(),
                "ip_address": fake.ipv4(),
                "login_time": fake.date_time_between(start_date='-1m', end_date='now')
            })
            
        conn.execute(
            text("INSERT INTO user_sessions (session_token, ip_address, login_time) VALUES (:session_token, :ip_address, :login_time)"),
            sessions
        )
        
        logging.info("Generating 10,000 activity logs...")
        logs = []
        for _ in range(10000):
            logs.append({
                "session_id": random.randint(1, 10000),
                "action": random.choice(['login', 'view_page', 'click_button', 'logout', 'purchase']),
                "details": fake.text(max_nb_chars=50)
            })
            
        conn.execute(
            text("INSERT INTO activity_logs (session_id, action, details) VALUES (:session_id, :action, :details)"),
            logs
        )
        conn.commit()
        logging.info("PostgreSQL seeding completed.")

def main():
    try:
        seed_mysql(MYSQL_CONFIG)
    except Exception as e:
        logging.error(f"MySQL Seeding Failed: {e}")

    try:
        seed_mssql(MSSQL_CONFIG)
    except Exception as e:
        logging.error(f"MSSQL Seeding Failed: {e}")

    try:
        seed_postgres(POSTGRES_CONFIG)
    except Exception as e:
        logging.error(f"PostgreSQL Seeding Failed: {e}")

if __name__ == "__main__":
    main()
