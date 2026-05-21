---
name: iis-expert
description: Experto sénior en la administración, configuración y optimización de Internet Information Services (IIS). Domina la gestión de Application Pools, Binding, certificados SSL, seguridad de sitios, despliegue de aplicaciones .NET y troubleshooting de errores HTTP.
---
# IIS Expert - Guía de Operaciones

Esta Skill proporciona el conocimiento necesario para gestionar servidores IIS de forma profesional, asegurando alta disponibilidad, seguridad y rendimiento.

## Capacidades Principales
- **Configuración de Sitios**: Gestión de Bindings (Host Headers, IP, Puertos).
- **Application Pools**: Optimización de reciclado, identidad del proceso y límites de memoria.
- **Seguridad**: Configuración de permisos NTFS, Autenticación (Windows, Anonymous), y endurecimiento de SSL/TLS.
- **Troubleshooting**: Análisis de logs (W3C), Failed Request Tracing (FREB) y errores 5xx.
- **Automatización**: Uso de AppCmd.exe y el módulo WebAdministration de PowerShell.

## Mejores Prácticas
1. **Aislamiento**: Usar un Application Pool dedicado por cada sitio web.
2. **Privilegios Mínimos**: La identidad del AppPool debe tener solo los permisos necesarios en el sistema de archivos.
3. **Monitoreo**: Configurar alertas para el uso de CPU y memoria de los procesos `w3wp.exe`.
4. **Despliegue**: Usar Web Deploy para publicaciones consistentes y seguras.
