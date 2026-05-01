---
name: devops-expert
description: Experto en el despliegue de aplicaciones desarrolladas con FastAPI, GeneXus y otras tecnologías en entornos de producción On-Premise. Especialista en la configuración de servidores IIS, Apache, Tomcat y bases de datos PostgreSQL.
---

# DevOps Expert Guide (On-Premise Deployment)

Esta skill permite al agente gestionar el ciclo de vida completo de un despliegue, asegurando que el software se publique de forma segura, escalable y automatizada en servidores propios.

## 1. Jerarquía Estándar de Entornos

Para cualquier despliegue, organiza la infraestructura siguiendo este flujo:

1.  **Desarrollo (DEV):** Entorno local o de equipo para integración continua y pruebas rápidas.
2.  **Staging / Testing (STG):** Réplica exacta de producción para validación final (User Acceptance Testing).
3.  **Producción (PRD):** Entorno crítico para usuarios finales con máxima disponibilidad y seguridad.

## 2. Estrategias de Despliegue por Servidor

Consulta las guías específicas en la carpeta `references/`:

- **IIS (.NET Core / C#):** Despliegue mediante `Publish` y configuración de `AppPools`.
- **IIS (Java):** Uso de `HttpPlatformHandler` para actuar como proxy hacia Tomcat o Jetty.
- **Apache (Python/FastAPI):** Configuración de `mod_proxy` para redirigir tráfico a `uvicorn`.
- **Apache (Java):** Integración con Tomcat mediante `mod_jk` o `mod_proxy_ajp`.

## 3. Gestión de Infraestructura On-Premise

Prioriza la estabilidad y la automatización local:
- **DNS Interno:** Configuración de nombres de host amigables para servicios.
- **Firewalls:** Apertura de puertos específicos (80, 443, 5432) siguiendo el principio de mínimo privilegio.
- **Backup:** Automatización de respaldos de PostgreSQL (`pg_dump`) y de archivos de configuración.

## 4. Automatización con Scripts

Cada despliegue debe estar acompañado de scripts que minimicen el error humano:
- **PowerShell:** Para automatizar cambios en IIS y servicios de Windows.
- **Bash:** Para gestionar servicios de Linux, permisos y actualizaciones de paquetes.

## Checklist de Publicación a Producción

- [ ] **Configuración:** ¿Se han migrado todas las variables de entorno de STG a PRD?
- [ ] **Base de Datos:** ¿Se han ejecutado las migraciones de esquema en PostgreSQL?
- [ ] **SSL/TLS:** ¿Están instalados y vigentes los certificados de seguridad?
- [ ] **Health Check:** ¿El endpoint `/health` responde correctamente tras reiniciar el servicio?
- [ ] **Logs:** ¿Está configurada la rotación de logs para evitar llenar el disco del servidor?

---
*Usa esta skill para garantizar que lo que funciona en local, brille en producción.*
