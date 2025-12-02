import psycopg2

# Credentials from AllTestCredentials.md for PostgreSQL
HOST = "localhost"
PORT = 5433
USER = "postgres"
PASSWORD = "postgres"
DB_NAME = "DataScout"

def verify_data():
    try:
        con = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DB_NAME
        )
        cur = con.cursor()
        
        cur.execute("SELECT COUNT(*) FROM saved_connections")
        conn_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM saved_schemas")
        schema_count = cur.fetchone()[0]
        
        print(f"Saved Connections: {conn_count}")
        print(f"Saved Schemas: {schema_count}")
        
        if conn_count > 0 and schema_count > 0:
            print("VERIFICATION SUCCESS: Data persisted.")
        else:
            print("VERIFICATION FAILED: No data found.")
            
        cur.close()
        con.close()
        
    except Exception as e:
        print(f"Error verifying data: {e}")

if __name__ == "__main__":
    verify_data()
