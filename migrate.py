from app.database import engine
from sqlalchemy import text, inspect
from app.models import Base

def migrate():
    inspector = inspect(engine)
    columns = [c['name'] for c in inspector.get_columns('users')]
    
    with engine.connect() as conn:
        print("Checking users table...")
        if 'email' not in columns:
            print("Adding email...")
            conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR(150) UNIQUE"))
        if 'status' not in columns:
            print("Adding status...")
            conn.execute(text("ALTER TABLE users ADD COLUMN status ENUM('Activo', 'Suspendido') DEFAULT 'Activo'"))
        if 'failed_attempts' not in columns:
            print("Adding failed_attempts...")
            conn.execute(text("ALTER TABLE users ADD COLUMN failed_attempts INT DEFAULT 0"))
        
        print("Creating remaining tables (audit_logs)...")
        Base.metadata.create_all(bind=engine)
        
        conn.commit()
    print("Migration finished successfully.")

if __name__ == "__main__":
    migrate()
