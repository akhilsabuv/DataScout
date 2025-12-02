import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

# MySQL Credentials from AllTestCredentials.md
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "StrongMySQLRoot!23",
    "database": "mysqlTest"
}

def wait_for_backend():
    print("Waiting for backend to be ready...")
    for _ in range(10):
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("Backend is ready.")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    print("Backend failed to start.")
    return False

def connect_mysql():
    print("Connecting to MySQL...")
    try:
        response = requests.post(f"{BASE_URL}/connect/mysql", json=MYSQL_CONFIG)
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully connected. Connection ID: {data.get('connection_id')}")
            return True
        else:
            print(f"Failed to connect to MySQL. Status: {response.status_code}, Detail: {response.text}")
            return False
    except Exception as e:
        print(f"Exception during connection: {e}")
        return False

def delete_connection():
    print("Attempting to delete connection...")
    try:
        response = requests.delete(f"{BASE_URL}/connection")
        if response.status_code == 200:
            print("Delete request successful.")
            return True
        else:
            print(f"Delete request failed. Status: {response.status_code}, Detail: {response.text}")
            return False
    except Exception as e:
        print(f"Exception during delete: {e}")
        return False

if __name__ == "__main__":
    if not wait_for_backend():
        sys.exit(1)
    
    if not connect_mysql():
        sys.exit(1)
    
    # Wait a bit to ensure everything is settled
    time.sleep(2)
    
    if delete_connection():
        print("TEST PASSED: Connection deleted successfully.")
    else:
        print("TEST FAILED: Could not delete connection.")
        sys.exit(1)
