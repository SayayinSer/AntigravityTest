import mysql.connector

def setup_database():
    try:
        # Conectar a MariaDB (sin especificar DB para crearla primero)
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            collation='utf8mb4_general_ci'
        )
        cursor = db.cursor()

        # Crear base de datos
        cursor.execute("CREATE DATABASE IF NOT EXISTS antigravity_test CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        cursor.execute("USE antigravity_test")

        # Crear Tablas
        tables = [
            """
            CREATE TABLE IF NOT EXISTS brands (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vehicle_types (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                internal_code VARCHAR(50) NOT NULL UNIQUE,
                plate VARCHAR(20) NOT NULL UNIQUE,
                brand_id INT,
                type_id INT,
                model VARCHAR(100),
                year INT,
                FOREIGN KEY (brand_id) REFERENCES brands(id),
                FOREIGN KEY (type_id) REFERENCES vehicle_types(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS technicians (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS work_orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT,
                status ENUM('Pendiente', 'En Ejecución', 'Terminada', 'Anulada') DEFAULT 'Pendiente',
                diagnosis TEXT,
                solution TEXT,
                recommendation TEXT,
                entry_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                exit_date DATETIME,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS wo_tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                work_order_id INT,
                description TEXT,
                duration_minutes INT,
                technician_id INT,
                FOREIGN KEY (work_order_id) REFERENCES work_orders(id),
                FOREIGN KEY (technician_id) REFERENCES technicians(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS wo_parts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                work_order_id INT,
                description VARCHAR(255),
                quantity DECIMAL(10,2),
                unit_price DECIMAL(12,2),
                uom VARCHAR(20),
                FOREIGN KEY (work_order_id) REFERENCES work_orders(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS wo_third_parties (
                id INT AUTO_INCREMENT PRIMARY KEY,
                work_order_id INT,
                provider_name VARCHAR(255),
                description TEXT,
                price DECIMAL(12,2),
                FOREIGN KEY (work_order_id) REFERENCES work_orders(id)
            )
            """
        ]

        for table_sql in tables:
            cursor.execute(table_sql)

        # Cargar Datos Semilla (Pre-carga)
        brands = [('Toyota',), ('Ford',), ('Chevrolet',), ('Volkswagen',), ('Mercedes-Benz',), ('Scania',), ('Honda',), ('Yamaha',)]
        cursor.executemany("INSERT IGNORE INTO brands (name) VALUES (%s)", brands)

        types = [('Auto',), ('Camión',), ('Moto',), ('Utilitario',), ('Maquinaria',)]
        cursor.executemany("INSERT IGNORE INTO vehicle_types (name) VALUES (%s)", types)

        techs = [('Juan Pérez',), ('Carlos Gómez',), ('Luis Rodríguez',)]
        cursor.executemany("INSERT IGNORE INTO technicians (name) VALUES (%s)", techs)

        # Pre-carga de Vehículos (Moviles)
        vehicles = [
            ('M001', 'ABC-123', 1, 1, 'Corolla', 2022),
            ('M002', 'XYZ-789', 2, 2, 'F-150', 2021),
            ('M003', 'MOT-456', 7, 3, 'CB500', 2023),
            ('M004', 'UTI-111', 4, 4, 'Amarok', 2020)
        ]
        cursor.executemany("INSERT IGNORE INTO vehicles (internal_code, plate, brand_id, type_id, model, year) VALUES (%s, %s, %s, %s, %s, %s)", vehicles)

        db.commit()
        print("Base de datos 'antigravity_test' configurada exitosamente.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    setup_database()
