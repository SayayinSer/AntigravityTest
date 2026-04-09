from app.database import engine, Base
from app import models

def init_db():
    print("Capturando esquema de base de datos...")
    # Eliminar tablas existentes para asegurar que las nuevas restricciones se apliquen
    print("Eliminando tablas existentes (Limpieza total)...")
    Base.metadata.drop_all(bind=engine)
    
    # Crear tablas con restricciones reales en PostgreSQL
    print("Creando nuevas tablas con integridad relacional (PostgreSQL)...")
    Base.metadata.create_all(bind=engine)
    print("¡Base de datos inicializada con éxito!")

if __name__ == "__main__":
    init_db()
