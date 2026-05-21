---
name: php-mysql-expert
description: Especialista en desarrollo profesional de aplicaciones web con PHP 8.1+ y bases de datos MySQL/MariaDB. Sigue estándares PSR, utiliza PDO para seguridad y promueve arquitecturas limpias (OOP). Úsala cuando el usuario solicite crear backends en PHP, optimizar consultas SQL o securizar código PHP.
---
# Experto en Desarrollo PHP & MySQL Profesional

Esta Skill guía al agente en la construcción de sistemas robustos, seguros y mantenibles utilizando PHP moderno (8.1+) y bases de datos relacionales MySQL o MariaDB.

## Principios Fundamentales

1. **Tipado Estricto:** Siempre comienza los archivos con `declare(strict_types=1);`.
2. **Estándares PSR:** Cumplimiento riguroso de PSR-1 (Estilo), PSR-4 (Autoloading) y PSR-12 (Guía de estilo extendida).
3. **Seguridad por Diseño:**
    - **PDO:** Uso obligatorio de sentencias preparadas para todas las consultas.
    - **Sanitización:** Saneamiento de entradas y escape de salidas (XSS).
    - **Password Hashing:** Uso de `password_hash()` con BCRYPT o ARGON2.
4. **Arquitectura OOP:** Preferencia por Programación Orientada a Objetos, inyección de dependencias y separación de responsabilidades.

## Guía de Implementación Base

### Conexión Segura (PDO)
Utiliza siempre un Wrapper o una Factory para manejar la conexión. Asegúrate de configurar los atributos de error:

```php
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];
```

### Consultas SQL
- Evita el uso de `SELECT *`.
- Utiliza índices adecuadamente.
- Prefiere JOINs sobre múltiples consultas aisladas cuando sea posible.

## Checklist de Verificación de Código

- [ ] ¿Tiene `declare(strict_types=1)`?
- [ ] ¿Usa PDO con *prepared statements*?
- [ ] ¿Están las propiedades de clase tipadas (PHP 7.4+ / 8.1+)?
- [ ] ¿El namespace sigue la estructura PSR-4?
- [ ] ¿Se manejan las excepciones de base de datos correctamente?
