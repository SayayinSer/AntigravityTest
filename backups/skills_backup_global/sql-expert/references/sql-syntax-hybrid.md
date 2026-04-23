# Comparativa de Sintaxis SQL Híbrida (Syntactic Sugar)

Esta guía detalla las diferencias más comunes al escribir SQL para distintos motores.

## 1. Paginación de Resultados
- **PostgreSQL / MySQL:** `LIMIT 10 OFFSET 20`
- **SQL Server:** `OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY`

## 2. Concatenación de Cadenas
- **PostgreSQL / SQL Server:** `col1 || ' ' || col2` o `CONCAT(col1, ' ', col2)`
- **MySQL:** `CONCAT(col1, ' ', col2)` (El operador `||` suele interpretarse como OR lógico a menos que se configure `PIPES_AS_CONCAT`).

## 3. Manejo de Fechas (Timestamp actual)
- **PostgreSQL:** `CURRENT_TIMESTAMP`, `now()`
- **MySQL:** `now()`, `CURRENT_TIMESTAMP()`
- **SQL Server:** `GETDATE()`, `SYSDATETIME()`

## 4. Upsert (Insert or Update)
- **PostgreSQL:** `INSERT ... ON CONFLICT (id) DO UPDATE SET ...`
- **MySQL:** `INSERT ... ON DUPLICATE KEY UPDATE ...`
- **SQL Server:** `MERGE INTO target USING source ON ... WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT ...`

## 5. Tipos de Datos (Equivalencias)
- **PostgreSQL:** `TEXT`, `VARCHAR`, `JSONB`, `BOOLEAN`
- **MySQL:** `TEXT`, `VARCHAR`, `JSON`, `TINYINT(1)` (boolean)
- **SQL Server:** `VARCHAR(MAX)`, `NVARCHAR`, `JSON` (via NVARCHAR/Constraints), `BIT` (boolean)

---
*Usa estas equivalencias para asegurar que los scripts se adapten al entorno de ejecución.*
