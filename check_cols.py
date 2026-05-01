import psycopg2

def check_cols(table):
    conn = psycopg2.connect(host="127.0.0.1", database="antigravity_test", user="postgres", password="123456")
    cur = conn.cursor()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
    cols = [c[0] for c in cur.fetchall()]
    print(f"Table {table}: {', '.join(cols)}")
    cur.close()
    conn.close()

check_cols('wo_tasks')
check_cols('wo_parts')
check_cols('wo_third_parties')
