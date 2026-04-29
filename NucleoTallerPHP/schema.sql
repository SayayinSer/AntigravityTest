-- Schema de Base de Datos para NucleoTaller (LAMP / MySQL)
-- Generado a partir de la versión de Python (FastAPI/SQLAlchemy)

SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE IF NOT EXISTS `roles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL UNIQUE,
  `description` VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(100) NOT NULL UNIQUE,
  `hashed_password` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(150),
  `email` VARCHAR(150) UNIQUE,
  `status` ENUM('Activo', 'Suspendido') DEFAULT 'Activo',
  `failed_attempts` INT DEFAULT 0,
  `is_active` TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `user_roles` (
  `user_id` INT,
  `role_id` INT,
  PRIMARY KEY (`user_id`, `role_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `countries` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `provinces` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `country_id` INT,
  FOREIGN KEY (`country_id`) REFERENCES `countries`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `brands` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `vehicle_types` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `vehicles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `internal_code` INT UNIQUE,
  `plate` VARCHAR(20) NOT NULL UNIQUE,
  `brand_id` INT,
  `type_id` INT,
  `model` VARCHAR(100),
  `year` INT,
  `current_mileage` INT DEFAULT 0,
  `last_owner` VARCHAR(150),
  `last_service_date` DATETIME,
  `next_service_suggestion` DATETIME,
  `photo_url` VARCHAR(255) DEFAULT '/static/img/default_vehicle.png',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` INT,
  `updated_by` INT,
  FOREIGN KEY (`brand_id`) REFERENCES `brands`(`id`) ON DELETE RESTRICT,
  FOREIGN KEY (`type_id`) REFERENCES `vehicle_types`(`id`) ON DELETE RESTRICT,
  FOREIGN KEY (`created_by`) REFERENCES `users`(`id`) ON DELETE SET NULL,
  FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `technicians` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `work_orders` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `vehicle_id` INT,
  `status` ENUM('Pendiente', 'En Ejecución', 'Terminada', 'Anulada') DEFAULT 'Pendiente',
  `diagnosis` TEXT,
  `solution` TEXT,
  `recommendation` TEXT,
  `entry_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `exit_date` DATETIME,
  `recorded_mileage` INT,
  `created_by` INT,
  `updated_by` INT,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles`(`id`) ON DELETE RESTRICT,
  FOREIGN KEY (`created_by`) REFERENCES `users`(`id`) ON DELETE SET NULL,
  FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `wo_tasks` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `work_order_id` INT,
  `description` TEXT,
  `duration_minutes` INT,
  `technician_id` INT,
  FOREIGN KEY (`work_order_id`) REFERENCES `work_orders`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`technician_id`) REFERENCES `technicians`(`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `wo_parts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `work_order_id` INT,
  `description` VARCHAR(255),
  `quantity` DECIMAL(10,2),
  `unit_price` DECIMAL(12,2),
  `uom` VARCHAR(20),
  FOREIGN KEY (`work_order_id`) REFERENCES `work_orders`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `wo_third_parties` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `work_order_id` INT,
  `provider_name` VARCHAR(255),
  `description` TEXT,
  `price` DECIMAL(12,2),
  FOREIGN KEY (`work_order_id`) REFERENCES `work_orders`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `audit_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `action` VARCHAR(50),
  `entity_name` VARCHAR(50),
  `entity_id` INT,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `details` TEXT,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `owners` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `owner_number` INT UNIQUE,
  `email` VARCHAR(150) NOT NULL UNIQUE,
  `full_name` VARCHAR(150) NOT NULL,
  `phone` VARCHAR(50),
  `address` VARCHAR(255),
  `owner_type` ENUM('Persona Física', 'Persona Jurídica') DEFAULT 'Persona Física',
  `document_id` VARCHAR(50),
  `photo_url` VARCHAR(255) DEFAULT '/static/img/default_avatar.png',
  `country_id` INT,
  `province_id` INT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`country_id`) REFERENCES `countries`(`id`) ON DELETE SET NULL,
  FOREIGN KEY (`province_id`) REFERENCES `provinces`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `appointments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `owner_id` INT,
  `client_email` VARCHAR(150),
  `client_name` VARCHAR(150) NOT NULL,
  `client_phone` VARCHAR(50),
  `vehicle_id` INT,
  `plate` VARCHAR(20),
  `scheduled_date` DATETIME NOT NULL,
  `reason` TEXT,
  `status` ENUM('Pendiente', 'Confirmado', 'Atendido', 'Cancelado') DEFAULT 'Pendiente',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` INT,
  `updated_by` INT,
  FOREIGN KEY (`owner_id`) REFERENCES `owners`(`id`) ON DELETE RESTRICT,
  FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles`(`id`) ON DELETE SET NULL,
  FOREIGN KEY (`created_by`) REFERENCES `users`(`id`) ON DELETE SET NULL,
  FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS=1;

-- Insertar usuario admin por defecto (Clave: admin123, BCRYPT hash)
INSERT IGNORE INTO `roles` (`name`, `description`) VALUES ('Admin', 'Administrador Total');
INSERT IGNORE INTO `users` (`username`, `hashed_password`, `full_name`, `email`) VALUES ('admin', '$2y$10$R9h/cIPzHgi.URNNX3ni2exz5Z8eT8b8IeC5V4t8p4fL7Cq7C7z/C', 'Administrador', 'admin@local.com');
INSERT IGNORE INTO `user_roles` (`user_id`, `role_id`) VALUES (1, 1);
