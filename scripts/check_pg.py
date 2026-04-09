import psycopg2
import sys

try:
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="123456",
        dbname="postgres"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    # Check if DB exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'antigravity_test'")
    exists = cur.fetchone()
    
    if not exists:
        cur.execute("CREATE DATABASE antigravity_test ENCODING 'UTF8'")
        print("Database 'antigravity_test' CREATED successfully.")
    else:
        print("Database 'antigravity_test' already exists.")
    
    cur.close()
    conn.close()
    
    # Now test connection to the new DB
    conn2 = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="123456",
        dbname="antigravity_test"
    )
    print("Connection to 'antigravity_test' OK!")
    conn2.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
