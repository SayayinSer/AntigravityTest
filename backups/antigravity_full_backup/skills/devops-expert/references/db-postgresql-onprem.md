# PostgreSQL On-Premise (Production)

Guía para la configuración y mantenimiento de bases de datos PostgreSQL en servidores propios.

## 1. Configuración y Tuning
Edición de `postgresql.conf` para optimizar el rendimiento:
- `max_connections`: Ajustar basándose en la carga esperada.
- `shared_buffers`: Aproximadamente 25% de la memoria RAM del sistema.
- `temp_buffers`: Incrementar si se realizan muchas operaciones de tabla temporal.
- `work_mem`: Relevante para consultas complejas con sorting y hashing.

## 2. Seguridad y Acceso
Edición de `pg_hba.conf`:
- Restringir el acceso solo a las IPs de los servidores de aplicaciones.
- Usar métodos de autenticación seguros (`scram-sha-256`).
- No permitir el acceso a usuario `postgres` desde fuera del servidor.

## 3. Estrategias de Backup (Continuidad de Negocio)
Automatización mediante tareas programadas (Cron en Linux / Task Scheduler en Windows):
- **Backup Lógico:** `pg_dump -U [user] -F c [dbname] > [filename].dump`.
- **Rotación:** Mantener backups diarios de los últimos 7 días, semanales de los últimos 4 y mensuales de los últimos 12.
- **Validación:** Probar periódicamente la restauración de un backup en el entorno de STG.

---
*Una base de datos bien configurada es el corazón de cualquier aplicación empresarial.*
