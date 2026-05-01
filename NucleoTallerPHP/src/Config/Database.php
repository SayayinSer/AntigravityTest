<?php
declare(strict_types=1);

namespace Config;

use PDO;
use PDOException;
use Exception;

class Database {
    private static ?PDO $connection = null;

    public static function getConnection(): PDO {
        if (self::$connection === null) {
            // Leer credenciales de entorno o hardcode local fallback (PostgreSQL para pruebas locales)
            $host = getenv('DB_HOST') ?: '127.0.0.1';
            $port = getenv('DB_PORT') ?: '5432';
            $dbname = getenv('DB_NAME') ?: 'antigravity_test';
            $username = getenv('DB_USER') ?: 'postgres';
            $password = getenv('DB_PASS') ?: '123456';
            
            // Usamos pgsql para pruebas locales que corren sobre la DB de Python
            $dsn = "pgsql:host={$host};port={$port};dbname={$dbname}";
            
            $options = [
                PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES   => false,
            ];

            try {
                self::$connection = new PDO($dsn, $username, $password, $options);
            } catch (PDOException $e) {
                throw new Exception("Error de conexión a la base de datos: " . $e->getMessage());
            }
        }

        return self::$connection;
    }
}
