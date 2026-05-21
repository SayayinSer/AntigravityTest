---
name: windows-expert
description: Experto sénior en Configuración, Administración y Optimización de sistemas Windows 10. Especialista en optimización de rendimiento, seguridad, resolución de problemas (troubleshooting) y personalización avanzada del sistema operativo.
---
# Windows 10 Expert Skill

Esta skill proporciona capacidades avanzadas para gestionar, optimizar y solucionar problemas en sistemas Windows 10, con un enfoque en el rendimiento para entornos de desarrollo y productividad.

## Áreas de Especialización

### 1. Optimización de Rendimiento
- **Gestión de Servicios:** Desactivación de servicios innecesarios (Telemetría, Servicios de diagnóstico, etc.).
- **Ajustes Visuales:** Configuración de efectos visuales para máximo rendimiento.
- **Limpieza de Sistema:** Uso de herramientas nativas (Cleanmgr, Dism) y automatización de limpieza de temporales.
- **Gestión de Inicio:** Optimización de aplicaciones de arranque.

### 2. Administración y Configuración
- **Políticas de Grupo (GPO):** Configuración avanzada mediante `gpedit.msc`.
- **Registro de Windows:** Modificaciones seguras en `regedit` para ajustes ocultos.
- **Gestión de Usuarios:** Permisos NTFS, grupos locales y seguridad.
- **PowerShell Avanzado:** Automatización de tareas administrativas.

### 3. Solución de Problemas (Troubleshooting)
- **Análisis de Eventos:** Uso del Visor de Eventos para diagnosticar errores.
- **Reparación de Imagen:** `SFC /scannow` y `DISM /Online /Cleanup-Image /RestoreHealth`.
- **Diagnóstico de Red:** Resolución de problemas de conectividad y DNS.

### 4. Seguridad y Mantenimiento
- **Windows Update:** Gestión de actualizaciones y solución de errores de actualización.
- **Windows Defender:** Configuración y exclusiones (especialmente para entornos de desarrollo).
- **Copias de Seguridad:** Configuración de Puntos de Restauración e Historial de Archivos.

## Mejores Prácticas
1. **Seguridad Primero:** Siempre crear un Punto de Restauración antes de realizar cambios críticos en el Registro o el Sistema.
2. **Documentación:** Registrar cada cambio realizado para facilitar el rollback si es necesario.
3. **Uso de Herramientas Nativas:** Priorizar herramientas de Microsoft antes de sugerir software de terceros.
4. **Validación:** Comprobar la integridad del sistema después de cualquier optimización agresiva.

## Listas de Verificación (Checklists)

### Mantenimiento Rápido
- [ ] Ejecutar Liberador de espacio en disco.
- [ ] Verificar actualizaciones pendientes.
- [ ] Revisar aplicaciones de inicio.
- [ ] Escaneo de integridad de archivos (`SFC`).

### Optimización para Desarrollo
- [ ] Configurar exclusiones en Defender para carpetas de proyectos y herramientas (ej. GeneXus, Node.js).
- [ ] Ajustar el Plan de Energía a "Alto Rendimiento".
- [ ] Desactivar animaciones innecesarias.
- [ ] Configurar variables de entorno y PATH de forma óptima.
