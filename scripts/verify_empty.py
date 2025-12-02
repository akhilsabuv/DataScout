import psycopg2

# Credentials from AllTestCredentials.md for PostgreSQL
HOST = "localhost"
PORT = 5433
USER = "postgres"
PASSWORD = "postgres"
DB_NAME = "DataScout"

def verify_empty():
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
        count_conn = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM saved_schemas")
        count_schema = cur.fetchone()[0]
        
        print(f"Saved Connections: {count_conn}")
        print(f"Saved Schemas: {count_schema}")
        
        if count_conn == 0 and count_schema == 0:
            print("VERIFICATION SUCCESS: Tables are empty.")
        else:
            print("VERIFICATION FAILED: Tables are not empty.")
            
        cur.close()
        con.close()
        
    except Exception as e:
        print(f"Error verifying empty tables: {e}")

if __name__ == "__main__":
    verify_empty()
