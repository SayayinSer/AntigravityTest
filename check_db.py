import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="antigravity_test",
        user="postgres",
        password="123456"
    )
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    for table in tables:
        print(table[0])
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
