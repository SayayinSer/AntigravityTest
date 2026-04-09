from app.database import engine
from sqlalchemy import text
import json
from datetime import datetime, date

def default_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return str(obj)

def backup():
    tables = ['users', 'roles', 'brands', 'vehicle_types', 'vehicles', 'work_orders', 'audit_logs', 'technicians', 'wo_tasks', 'wo_parts', 'wo_third_parties']
    data = {}
    with engine.connect() as conn:
        for table in tables:
            try:
                res = conn.execute(text(f"SELECT * FROM {table}"))
                data[table] = [dict(row._mapping) for row in res]
            except Exception as e:
                print(f"Error backup table {table}: {e}")
    
    with open('backups/db_beta_backup.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, default=default_serializer)
    print("Backup local de datos completado en backups/db_beta_backup.json")

if __name__ == "__main__":
    backup()
