import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123456",
    dbname="antigravity_test"
)
cur = conn.cursor()

tables = ['users', 'roles', 'brands', 'vehicle_types', 'technicians']
for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    count = cur.fetchone()[0]
    print(f"  {t}: {count} registros")

print("\nUsuarios:")
cur.execute("SELECT id, username, full_name, status FROM users")
for row in cur.fetchall():
    print(f"  ID={row[0]} | {row[1]} | {row[2]} | {row[3]}")

print("\nRoles:")
cur.execute("SELECT id, name FROM roles")
for row in cur.fetchall():
    print(f"  ID={row[0]} | {row[1]}")

cur.close()
conn.close()
print("\nVerificacion completada OK!")
