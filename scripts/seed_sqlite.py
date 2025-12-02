import sqlite3

def seed_sqlite():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    cursor.execute("INSERT INTO products (name, price) VALUES ('Laptop', 999.99)")
    cursor.execute("INSERT INTO products (name, price) VALUES ('Mouse', 19.99)")
    
    conn.commit()
    conn.close()
    print("SQLite seeded.")

if __name__ == "__main__":
    seed_sqlite()
