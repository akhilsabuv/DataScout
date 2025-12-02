import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Credentials from AllTestCredentials.md for PostgreSQL
HOST = "localhost"
PORT = 5433
USER = "postgres"
PASSWORD = "postgres"
DB_NAME = "DataScout"

def drop_tables():
    try:
        con = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DB_NAME
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        print("Dropping tables...")
        cur.execute("DROP TABLE IF EXISTS saved_schemas CASCADE")
        cur.execute("DROP TABLE IF EXISTS saved_connections CASCADE")
        print("Tables dropped.")
            
        cur.close()
        con.close()
        
    except Exception as e:
        print(f"Error dropping tables: {e}")

if __name__ == "__main__":
    drop_tables()
