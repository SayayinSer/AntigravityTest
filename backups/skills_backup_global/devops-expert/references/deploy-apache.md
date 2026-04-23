# Despliegue en Apache (On-Premise)

Guía para publicar aplicaciones en el Servidor Apache HTTP.

## 1. Java (Tomcat / GeneXus Java)
Utilizando `mod_proxy`:
- **Prerrequisito:** Habilitar módulos `proxy` y `proxy_http` de Apache.
- **Configuración:**
```apache
<VirtualHost *:80>
    ServerName mi-app.local
    ProxyPreserveHost On
    ProxyPass / http://localhost:8080/mi-app/
    ProxyPassReverse / http://localhost:8080/mi-app/
</VirtualHost>
```
- **Optimización:** Usar mod_jk para una mejor gestión de colas entre Apache y Tomcat.

## 2. Python (FastAPI / Uvicorn)
Utilizando Gunicorn con `uvicorn` workers:
- **Prerrequisito:** Instalación de `python-venv` y módulos `mod_proxy`.
- **Configuración:**
```apache
<VirtualHost *:80>
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```
- **Gestión de Servicio:** Usar `systemd` en Linux o un administrador de servicios en Windows para mantener el proceso vivo.

---
*Apache es versátil y altamente configurable mediante VirtualHosts.*
