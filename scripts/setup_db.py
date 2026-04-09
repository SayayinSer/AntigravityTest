import psycopg2
from psycopg2 import sql

def setup_database():
    try:
        # Conectar a PostgreSQL (a la BD por defecto 'postgres' para crear la nueva)
        db = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="123456",
            dbname="postgres"
        )
        db.autocommit = True
        cursor = db.cursor()

        # Crear base de datos si no existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'antigravity_test'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE antigravity_test ENCODING 'UTF8'")
            print("Base de datos 'antigravity_test' creada.")
        else:
            print("Base de datos 'antigravity_test' ya existe.")

        cursor.close()
        db.close()

        # Conectar a la nueva base de datos
        db = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="123456",
            dbname="antigravity_test"
        )
        db.autocommit = True
        cursor = db.cursor()

        # Crear Tablas
        tables = [
            """
            CREATE TABLE IF NOT EXISTS brands (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vehicle_types (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vehicles (
                id SERIAL PRIMARY KEY,
                internal_code VARCHAR(50) NOT NULL UNIQUE,
                plate VARCHAR(20) NOT NULL UNIQUE,
                brand_id INT REFERENCES brands(id),
                type_id INT REFERENCES vehicle_types(id),
                model VARCHAR(100),
                year INT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS technicians (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS work_orders (
                id SERIAL PRIMARY KEY,
                vehicle_id INT REFERENCES vehicles(id),
                status VARCHAR(20) DEFAULT 'Pendiente' CHECK (status IN ('Pendiente', 'En Ejecución', 'Terminada', 'Anulada')),
                diagnosis TEXT,
                solution TEXT,
                recommendation TEXT,
                entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                exit_date TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS wo_tasks (
                id SERIAL PRIMARY KEY,
                work_order_id INT REFERENCES work_orders(id),
                description TEXT,
                duration_minutes INT,
                technician_id INT REFERENCES technicians(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS wo_parts (
                id SERIAL PRIMARY KEY,
                work_order_id INT REFERENCES work_orders(id),
                description VARCHAR(255),
                quantity NUMERIC(10,2),
                unit_price NUMERIC(12,2),
                uom VARCHAR(20)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS wo_third_parties (
                id SERIAL PRIMARY KEY,
                work_order_id INT REFERENCES work_orders(id),
                provider_name VARCHAR(255),
                description TEXT,
                price NUMERIC(12,2)
            )
            """
        ]

        for table_sql in tables:
            cursor.execute(table_sql)

        # Cargar Datos Semilla (Pre-carga) con INSERT ... ON CONFLICT DO NOTHING
        brands = ['Toyota', 'Ford', 'Chevrolet', 'Volkswagen', 'Mercedes-Benz', 'Scania', 'Honda', 'Yamaha']
        for brand in brands:
            cursor.execute("INSERT INTO brands (name) VALUES (%s) ON CONFLICT DO NOTHING", (brand,))

        types = ['Auto', 'Camión', 'Moto', 'Utilitario', 'Maquinaria']
        for vtype in types:
            cursor.execute("INSERT INTO vehicle_types (name) VALUES (%s) ON CONFLICT DO NOTHING", (vtype,))

        techs = ['Juan Pérez', 'Carlos Gómez', 'Luis Rodríguez']
        for tech in techs:
            cursor.execute("INSERT INTO technicians (name) VALUES (%s) ON CONFLICT DO NOTHING", (tech,))

        # Pre-carga de Vehículos (Móviles)
        vehicles = [
            ('M001', 'ABC-123', 1, 1, 'Corolla', 2022),
            ('M002', 'XYZ-789', 2, 2, 'F-150', 2021),
            ('M003', 'MOT-456', 7, 3, 'CB500', 2023),
            ('M004', 'UTI-111', 4, 4, 'Amarok', 2020)
        ]
        for v in vehicles:
            cursor.execute(
                "INSERT INTO vehicles (internal_code, plate, brand_id, type_id, model, year) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                v
            )

        print("Base de datos 'antigravity_test' configurada exitosamente con PostgreSQL.")

    except psycopg2.Error as err:
        print(f"Error: {err}")
    finally:
        if 'db' in locals() and not db.closed:
            cursor.close()
            db.close()

if __name__ == "__main__":
    setup_database()
