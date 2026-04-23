-- Esquema de Seguridad y Auditoría (Modelo GAM Simple)

-- 1. Tabla de Usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE
);

-- 2. Tabla de Roles
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- 3. Relación Usuarios-Roles (Jerarquía)
CREATE TABLE user_roles (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- 4. Campos de Auditoría Requeridos en Tablas Maestras
-- Alter Table Ejemplo (Aplicar a todas las tablas críticas):
-- ALTER TABLE work_orders ADD COLUMN created_by INT REFERENCES users(id);
-- ALTER TABLE work_orders ADD COLUMN updated_by INT REFERENCES users(id);
-- ALTER TABLE work_orders ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;
-- ALTER TABLE work_orders ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
