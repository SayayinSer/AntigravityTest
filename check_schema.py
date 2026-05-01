import psycopg2

def check_all_tables():
    conn = psycopg2.connect(host="127.0.0.1", database="antigravity_test", user="postgres", password="123456")
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [t[0] for t in cur.fetchall()]
    
    for table in tables:
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
        cols = [c[0] for c in cur.fetchall()]
        print(f"Table {table}: {', '.join(cols)}")
    
    cur.close()
    conn.close()

check_all_tables()
