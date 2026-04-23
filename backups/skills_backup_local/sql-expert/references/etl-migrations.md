# Patrones de ETL y Migración de Datos (SQL Only)

Guía para mover y transformar grandes volúmenes de datos utilizando SQL.

## 1. Migración de Tablas Grandes (Batching)
Evitar bloqueos masivos y llenado de logs:
- **Patrón:** Dividir la migración en lotes (chunks) basados en el ID o una fecha.
- **SQL (PostgreSQL):** `INSERT INTO target SELECT * FROM source WHERE id BETWEEN 1 AND 10000; COMMIT;`
- **Recomendación:** Usar `COMMIT` entre lotes para liberar el Transaction Log (WAL/Redo).

## 2. Limpieza de Datos (Data Cleansing)
Eliminar duplicados y corregir inconsistencias:
- **Duplicados:** Usar `ROW_NUMBER() OVER(PARTITION BY col1 ORDER BY id)` para identificar y borrar filas repetidas.
- **Normalización:** Mover datos de columnas de texto a tablas maestras (`Lookup Tables`).
- **Validación:** Comprobar integridad referencial mediante `LEFT JOIN ... WHERE target.id IS NULL`.

## 3. Carga Masiva (Bulk Load)
Estrategias para insertar millones de registros:
- **PostgreSQL:** `COPY table FROM 'file.csv' WITH (FORMAT csv);`
- **SQL Server:** `BULK INSERT table FROM 'file.csv' WITH (FIELDTERMINATOR = ',');`
- **MySQL:** `LOAD DATA INFILE 'file.csv' INTO TABLE table;`

## 4. Transformación de Esquemas (Zero Downtime)
Actualizar la estructura sin desconectar a los usuarios:
- **Añadir Columna:** Hacerlo con un valor por defecto que no bloquee la tabla (en PG 11+ es instantáneo).
- **Cambiar Tipo:** Crear una columna nueva, migrar datos en lotes, y luego renombrar.
- **Drop Columna:** Marcar como `UNUSED` primero si el motor lo soporta.

---
*La migración exitosa es aquella que el usuario no nota.*
