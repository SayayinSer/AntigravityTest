import psycopg2
import json

def check_db():
    conn = psycopg2.connect(host="127.0.0.1", database="antigravity_test", user="postgres", password="123456")
    cur = conn.cursor()
    
    tables = ['owners', 'vehicles', 'appointments']
    result = {}
    for table in tables:
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
        result[table] = [c[0] for c in cur.fetchall()]
    
    print(json.dumps(result, indent=2))
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_db()
