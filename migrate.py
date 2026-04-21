from app.database import engine, Base
from sqlalchemy import text, inspect
import app.models # Ensure all models are loaded

def migrate():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    with engine.connect() as conn:
        print("--- Iniciando Reparación de Esquema de Base de Datos ---")
        
        for table_name, table in Base.metadata.tables.items():
            if table_name not in existing_tables:
                print(f"Table {table_name} does not exist. Creating all tables...")
                Base.metadata.create_all(bind=engine)
                break # metadata.create_all handles all missing tables
            
            # Check for missing columns in existing table
            existing_columns = [c['name'] for c in inspector.get_columns(table_name)]
            for column in table.columns:
                if column.name not in existing_columns:
                    print(f"Adding missing column: {table_name}.{column.name}...")
                    # Get column type and definition for basic types
                    col_type = str(column.type)
                    # Adjust types for PostgreSQL if necessary
                    if "VARCHAR" in col_type: col_type = "VARCHAR(255)"
                    if "ENUM" in col_type: col_type = "VARCHAR(50)" # Use varchar for enums in simple migration
                    
                    try:
                        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column.name} {col_type}"))
                    except Exception as e:
                        print(f"Error adding {column.name}: {e}")
        
        conn.commit()
    print("--- Proceso de Migración/Reparación finalizado con éxito ---")

if __name__ == "__main__":
    migrate()
