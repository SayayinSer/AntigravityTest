---
name: genexus-workwith-pattern
description: Especialista en la implementación del patrón estándar "Work With" inspirado en GeneXus. Esta skill asegura que cualquier entidad (tabla) del sistema tenga un ciclo de vida CRUD completo, validaciones de integridad, filtrado inteligente, paginación y reportes PDF, manteniendo una estética Slate & Sky.
---
# Patrón Estándar "Work With" (WW)

Esta skill encapsula la lógica de negocio y presentación necesaria para gestionar entidades de forma profesional y consistente, independiente del stack tecnológico.

## 🎯 Objetivos del Patrón
1. **Consistencia:** Todas las entidades se comportan y se ven igual.
2. **Integridad:** Validaciones robustas en backend y frontend.
3. **Eficiencia:** Búsqueda rápida, paginación para grandes volúmenes y reportes inmediatos.

## 🏗️ Estructura del Patrón

### 1. Capa de Datos (Data Model)
- **Identificadores:** Uso de nombres claros (ej. `ZonaCodigo` en lugar de `id`).
- **Nomenclatura:** Preferencia por nombres descriptivos en minúsculas para Postgres/MySQL o CamelCase para SQL Server.
- **Normalización:** Los datos de texto deben normalizarse (ej. `.upper()`) antes de persistir.

### 2. Capa de Servicios (Backend API)
Cualquier tecnología (FastAPI, C#, Java, GeneXus API) debe exponer:
- `GET /entity`: Lista paginada con soporte para filtros de búsqueda.
- `GET /entity/{id}`: Detalle de un registro único.
- `POST /entity`: Creación con validación de **Duplicidad**.
- `PUT /entity/{id}`: Actualización parcial o total.
- `DELETE /entity/{id}`: Borrado físico (o lógico si se requiere).

### 3. Capa de Interfaz (Frontend UI - Slate & Sky)
- **Dashboard:** Panel principal con el nombre de la tabla como título (limpio y prominente).
- **WorkWith List:** 
    - Tabla con hover effects y acciones iconográficas (`lucide-react`).
    - Filtro de búsqueda global en la parte superior.
    - Paginación inteligente (10 registros por defecto).
- **Acciones Rápidas:**
    - **Alta:** Formulario integrado o modal con validaciones inmediatas.
    - **Edición:** Edición inline (en la misma fila) para cambios rápidos.
    - **Reporte:** Botón de exportación a PDF que respete los filtros actuales y se abra en una nueva pestaña (Preview).

## 🛠️ Reglas de Implementación

### Validaciones Obligatorias
- **No Nulos:** Campos obligatorios no pueden estar vacíos.
- **Duplicidad:** Consultar la base de datos antes de insertar para evitar registros con el mismo nombre.
- **Formato:** Limpiar espacios y normalizar mayúsculas.

### Estándar de Reportes (PDF)
- El reporte debe llevar el nombre de la tabla como título principal.
- Incluir metadatos básicos: Fecha y hora de generación.
- Visualización: Siempre en pestaña nueva (`bloburl`).

### Paginación Inteligente
- Mostrar controles solo si `TotalRegistros > PageSize`.
- Resetear a la página 1 al cambiar el término de búsqueda.

## 🚀 Guía de Uso para el Agente
Cuando el usuario pida "aplicar el patrón WW" a una tabla:
1. **Analizar la Tabla:** Identificar PK y campos descriptivos.
2. **Generar Backend:** Crear endpoints estándar y lógica de duplicados.
3. **Generar Frontend:** Implementar la página con búsqueda, paginación e iconos.
4. **Verificar:** Probar el flujo completo (C-R-U-D) y la exportación PDF.
