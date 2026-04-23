# Patrones de Administración y Optimización (DBA)

Guía para mantener la salud y el rendimiento de sistemas relacionales.

## 1. Diseño de Índices (Indexing Strategy)
- **B-Tree:** El índice por defecto para comparaciones de igualdad y rangos.
- **Compuestos:** Índices que cubren múltiples columnas. El orden IMPORTA (de más selectivo a menos selectivo).
- **Parciales (PostgreSQL):** Índices que solo cubren una parte de la tabla (`WHERE is_active = true`).
- **GIN (PostgreSQL):** Ideal para búsqueda de texto completo o campos `JSONB`.

## 2. Análisis de Consultas (Explain Plans)
- **Seq Scan vs Index Scan:** Cómo detectar escaneos secuenciales costosos.
- **Nested Loops vs Hash Joins:** Entender cómo el motor combina tablas basándose en el tamaño de los conjuntos de datos.
- **Cost Estimation:** Identificar el "costo" relativo de cada nodo del plan.

## 3. Mantenimiento Preventivo
- **Vacuum / Analyze (PostgreSQL):** Liberar espacio muerto y actualizar estadísticas.
- **Reorganize / Rebuild (SQL Server):** Eliminar la fragmentación lógica de los índices.
- **Analyze Table (MySQL):** Actualizar la cardinalidad de los índices para el optimizador.

## 4. Gestión de Bloqueos (Locking Analysis)
- **Shared vs Exclusive Locks:** Cómo operan en lecturas y escrituras.
- **Deadlock Detection:** Estrategias para evitar bloqueos mutuos mediante el orden consistente de acceso a tablas.
- **Idle in Transaction:** Cómo los procesos que no cierran transacciones pueden degradar el sistema.

---
*Un administrador proactivo previene crisis de rendimiento antes de que lleguen a producción.*
