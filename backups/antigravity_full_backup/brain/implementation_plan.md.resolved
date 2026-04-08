# Plan de Implementación: Módulo de Seguridad y Control de Acceso (RBAC)

Este plan define la transición del aplicativo hacia un entorno multi-usuario seguro, implementando un sistema de Roles y Permisos inspirado en GAM, con un enfoque en la simplicidad operativa y estética moderna.

## User Review Required

> [!IMPORTANT]
> - **Cifrado de Credenciales:** Utilizaremos `bcrypt` para asegurar que las contraseñas nunca se almacenen en texto plano.
> - **Acceso por Defecto:** Se implementará una política de "Permitido por Defecto", excepto para el módulo de Seguridad, el cual estará estrictamente restringido al rol `OficialSeguridad`.
> - **Sesión:** Utilizaremos Cookies Seguras o JWT para mantener la sesión del usuario.
> - **Usuarios Iniciales:** Se precargarán las cuentas de `SU` (OficialSeguridad) y roles genéricos para Operador, Gerente e Invitado.

## Proposed Changes

### 1. Dependencias de Seguridad
- **[ACTION]:** Instalación de `passlib[bcrypt]` y `python-jose[cryptography]`.

### 2. Actualización del Modelo (app/models.py)
- **[MODIFY] [app/models.py](file:///c:/aaProyectos/Entorno01/app/models.py):**
    - Añadir las clases `User` y `Role`.
    - Implementar la relación muchos-a-muchos vía `user_roles`.

### 3. Lógica de Autenticación (app/auth.py) [NEW]
- **[NEW] [app/auth.py](file:///c:/aaProyectos/Entorno01/app/auth.py):**
    - Funciones para `hash_password`, `verify_password` y `create_access_token`.

### 4. Módulo de Administración de Seguridad (app/templates/security.html) [NEW]
- **[NEW] [app/templates/security.html](file:///c:/aaProyectos/Entorno01/app/templates/security.html):**
    - Interfaz moderna para gestionar usuarios y asignarles roles.
- **[NEW] [app/templates/login.html](file:///c:/aaProyectos/Entorno01/app/templates/login.html):**
    - Pantalla de acceso minimalista y profesional.

### 5. Rutas y Middleware (app/main.py)
- **[MODIFY] [app/main.py](file:///c:/aaProyectos/Entorno01/app/main.py):**
    - Endpoints de Login/Logout.
    - Dependencia `check_role('OficialSeguridad')` para proteger el panel de administración.
    - Actualización de `seed.py` para incluir los usuarios y roles solicitados.

## Open Questions
- ¿Deseas que la sesión expire tras un tiempo de inactividad (ej. 30 min) o prefieres sesiones persistentes?
- ¿El usuario `SU` debe poder crear otros usuarios con el rol `OficialSeguridad` o solo él debe tener ese nivel?

## Verification Plan

### Manual Verification
1. Intentar acceder al sistema (redirigir a Login si no hay sesión).
2. Entrar como `SU` con clave `123456`.
3. Navegar al módulo de Seguridad (debe permitir acceso).
4. Crear un usuario `Operador` y probar entrar con su cuenta (no debe permitir entrar a Seguridad).
