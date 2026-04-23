from app.database import SessionLocal
from app import models

def check_data():
    db = SessionLocal()
    vehicles = db.query(models.Vehicle).all()
    print(f"Total vehicles: {len(vehicles)}")
    for v in vehicles:
        print(f"Vehicle: {v.plate} (ID: {v.id})")
        print(f"  Orders: {len(v.orders)}")
        for o in v.orders:
            print(f"    Order ID: {o.id}, Status: {o.status}, Entry: {o.entry_date}")
    db.close()

if __name__ == "__main__":
    check_data()
