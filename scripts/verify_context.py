import psycopg2
import json

# Credentials from AllTestCredentials.md for PostgreSQL
HOST = "localhost"
PORT = 5433
USER = "postgres"
PASSWORD = "postgres"
DB_NAME = "DataScout"

def verify_context():
    try:
        con = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DB_NAME
        )
        cur = con.cursor()
        
        # Check Global Context
        cur.execute("SELECT global_context FROM saved_connections WHERE db_type='sqlite' ORDER BY id DESC LIMIT 1")
        global_ctx = cur.fetchone()
        print(f"Global Context: {global_ctx[0] if global_ctx else 'None'}")
        
        # Check Table Context
        cur.execute("SELECT table_context FROM saved_schemas WHERE table_name='products' ORDER BY id DESC LIMIT 1")
        table_ctx = cur.fetchone()
        print(f"Table Context: {table_ctx[0] if table_ctx else 'None'}")
        
        # Check Column Description (in JSON)
        cur.execute("SELECT columns_json FROM saved_schemas WHERE table_name='products' ORDER BY id DESC LIMIT 1")
        columns_json = cur.fetchone()
        if columns_json:
            cols = columns_json[0] # It's already a dict/list if using psycopg2 with json support, or string
            if isinstance(cols, str):
                cols = json.loads(cols)
            
            for col in cols:
                if col['name'] == 'id':
                    print(f"Column 'id' Description: {col.get('description', 'None')}")
        
        cur.close()
        con.close()
        
    except Exception as e:
        print(f"Error verifying context: {e}")

if __name__ == "__main__":
    verify_context()
