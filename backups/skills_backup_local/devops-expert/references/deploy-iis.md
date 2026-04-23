# Despliegue en IIS (On-Premise)

Guía para publicar aplicaciones en el Servidor de Información de Internet (IIS).

## 1. .NET Core (GX18 / C# / Web App)
Para publicar aplicaciones de .NET Core en IIS:
- **Prerrequisito:** Instalar el `.NET Core Hosting Bundle`.
- **Procedimiento:**
    - Generar el paquete con `dotnet publish -c Release`.
    - Crear un `Application Pool` configurado con `.NET CLR Version: No Managed Code`.
    - Apuntar el Sitio Web al directorio donde se guardó el publish.
- **Configuración:** Editar el archivo `web.config` generado para ajustar variables de entorno.

## 2. Java (GeneXus / JSP)
Implementación mediante `HttpPlatformHandler`:
- **Prerrequisito:** Instalación de `HttpPlatformHandler` mediante Web Platform Installer.
- **Configuración:**
    - El `web.config` debe contener la sección `<httpPlatform>` apuntando al ejecutable de **Tomcat** o el JAR ejecutable.
    - Definir los argumentos de la línea de comandos para el puerto dinámico (`%HTTP_PLATFORM_PORT%`).
- **Alternativa:** Uso de ISAPI Redirector para integración profunda con Tomcat.

---
*IIS ofrece un entorno estable y robusto para despliegues en Windows Server.*
