---
name: security-expert
description: Experto en la implementación de seguridad, control de acceso basado en roles (RBAC) y auditoría técnica siguiendo el estándar inspirado en GeneXus GAM. Úsala para securizar aplicaciones, definir jerarquías de usuarios y garantizar la trazabilidad de operaciones críticas.
---
# Experto en Seguridad y Auditoría (Estilo GAM)

Esta Skill define los procedimientos para blindar aplicaciones Python/FastAPI mediante un esquema de usuarios, roles y auditoría simple, garantizando que cada registro tenga un responsable y un momento de creación/modificación claro.

## Principios de Seguridad

1.  **Esquema de Identidad (GAM Like):**
    - **Usuarios:** Entidad principal con credenciales.
    - **Roles:** Agrupadores de permisos.
    - **UserRoles:** Relación muchos-a-muchos para asignar jerarquías.

2.  **Auditoría Simple:**
    - Cada tabla maestra debe incluir OBLIGATORIAMENTE:
        - `created_by`: ID del usuario creador.
        - `created_at`: Marca de tiempo de creación.
        - `updated_by`: ID del último usuario que modificó.
        - `updated_at`: Marca de tiempo de la última actualización.

3.  **Control de Acceso (RBAC):**
    - El acceso a los endpoints se debe validar mediante dependencias de FastAPI que verifiquen el rol del usuario actual.

## Lista de Verificación (Checklist) de Implementación

- [ ] Definir modelos `User` y `Role` en `models.py`.
- [ ] Implementar hashing de contraseñas (ej. passlib/bcrypt).
- [ ] Añadir campos de auditoría a las entidades de negocio (Marcas, Vehículos, Órdenes).
- [ ] Crear el Middleware o Dependencia `get_current_user`.
- [ ] Proteger rutas críticas (Administración, Cierre de Órdenes).

## Mejores Prácticas

- **Nunca** guardes contraseñas en texto plano.
- **Auditoría Automática:** Usa los eventos de SQLAlchemy (`before_insert`, `before_update`) para autocompletar los campos de auditoría sin intervenir en cada ruta del backend.
- **Principio de Mínimo Privilegio:** Los usuarios solo deben ver las acciones permitidas para su rol (ej. el técnico no puede borrar marcas).
