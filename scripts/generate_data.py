import sqlite3, os, random, hashlib
from datetime import datetime, timedelta
from faker import Faker

# Setup
if not os.path.exists("testData"): os.makedirs("testData")
db_path = "testData/ecommerce.db"
# Remove existing db to start fresh
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
fake = Faker()

# Schema
cursor.execute("CREATE TABLE IF NOT EXISTS user_credentials (user_id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT, email TEXT, role TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS customer_profiles (profile_id INTEGER PRIMARY KEY, user_id INTEGER, full_name TEXT, address TEXT, phone TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, stock INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, status TEXT, amount REAL)")

print("Generating data... this may take a moment.")

# 1. Users & Profiles (Generate 100 users)
users = []
profiles = []
for i in range(1, 101):
    username = fake.user_name()
    email = fake.email()
    role = "customer"
    users.append((i, username, hashlib.sha256(username.encode()).hexdigest(), email, role))
    
    profiles.append((i, i, fake.name(), fake.address().replace('\n', ', '), fake.phone_number()))

cursor.executemany("INSERT INTO user_credentials VALUES (?,?,?,?,?)", users)
cursor.executemany("INSERT INTO customer_profiles VALUES (?,?,?,?,?)", profiles)
print(f"Inserted {len(users)} users and profiles.")

# 2. Products (Generate 50 products)
categories = ['Electronics', 'Furniture', 'Clothing', 'Books', 'Home & Garden', 'Toys']
products = []
for i in range(1, 51):
    name = fake.catch_phrase()
    category = random.choice(categories)
    price = round(random.uniform(10.0, 2000.0), 2)
    stock = random.randint(0, 500)
    products.append((i, name, category, price, stock))

cursor.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)
print(f"Inserted {len(products)} products.")

# 3. Orders (Generate > 10,000 orders)
orders = []
num_orders = 12000
start_date = datetime(2023, 1, 1)
statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled', 'Processing']

for i in range(1, num_orders + 1):
    user_id = random.randint(1, 100)
    # Random date within last year
    order_date = start_date + timedelta(days=random.randint(0, 365))
    date_str = order_date.strftime("%Y-%m-%d")
    status = random.choices(statuses, weights=[1, 4, 10, 1, 2])[0]
    amount = round(random.uniform(20.0, 5000.0), 2)
    
    orders.append((i, user_id, date_str, status, amount))

cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders)
print(f"Inserted {len(orders)} orders.")

conn.commit()
conn.close()
print(f"Database created at {db_path} with >10k records.")
