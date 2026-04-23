---
name: sql-expert
description: Experto en el diseño, administración y optimización de bases de datos relacionales. Proporciona soluciones híbridas para PostgreSQL, MySQL/MariaDB y SQL Server mediante SQL avanzado, scripts de automatización y patrones de mantenimiento.
---

# SQL Expert & DBA Guide (Hybrid Support)

Esta skill permite al agente diseñar, optimizar y administrar bases de datos relacionales de alta disponibilidad en múltiples motores.

## 1. Estándares SQL Híbridos

Aunque cada motor tiene sus particularidades, se deben seguir principios universales de diseño:

- **PostgreSQL:** Priorizar el uso de tipos de datos ricos (`JSONB`, `INET`, `ARRAY`) y `EXPLAIN ANALYZE`.
- **MySQL / MariaDB:** Optimizar el uso de motores de almacenamiento (`InnoDB`) e índices de prefijo.
- **SQL Server:** Dominar el uso de `T-SQL`, CTEs (Common Table Expressions) y vistas indexadas.

## 2. Gestión de Transacciones y Concurrencia

Controla el comportamiento del sistema bajo carga masiva:

- **Niveles de Aislamiento:** `Read Committed` (por defecto), `Repeatable Read`, `Serializable`.
- **Bloqueos (Locks):** Identificación y resolución de Deadlocks y bloqueos prolongados.
- **Patrón:** SIEMPRE usar transacciones explícitas (`BEGIN`, `COMMIT`, `ROLLBACK`) para operaciones destructivas.

## 3. Optimización de Rendimiento (Tuning)

Sigue la jerarquía de optimización:
1.  **Modelo de Datos:** Normalización adecuada (3NF) vs Desnormalización controlada.
2.  **Índices:** Uso de índices compuestos, parciales y funcionales.
3.  **Consulta (Query):** Reescritura de JOINS, eliminación de subconsultas innecesarias y uso de `WHERE` sargable.

## 4. Patrones de Administración y Mantenimiento

Automatiza la salud de la base de datos mediante scripts SQL y envoltorios:
- **Limpieza de Datos:** Purga de tablas de logs y auditoría sin bloquear el sistema.
- **Reindexación:** Mantenimiento de estadísticas actualizadas para el optimizador de consultas.
- **Health Checks:** Consultas rápidas para verificar el tamaño de tablas y el estado de la replicación.

## Checklist de Administración Profesional

- [ ] **Plan de Ejecución:** ¿Se ha analizado el `EXPLAIN` del query más lento?
- [ ] **Constraints:** ¿Están definidas todas las `Primary Keys` y `Foreign Keys` necesarias?
- [ ] **Seguridad (DCL):** ¿Se sigue el principio de mínimo privilegio (`GRANT`/`REVOKE`)?
- [ ] **Idempotencia:** ¿Los scripts de migración pueden ejecutarse múltiples veces sin fallar?

---
*Usa esta skill para dominar los datos con precisión quirúrgica y rendimiento empresarial.*
