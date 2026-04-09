# Manual de Restauración Global: Antigravity Intelligence

Este respaldo contiene el "Cerebro" y las "Habilidades" configuradas durante este proyecto. Sigue estos pasos para replicar el entorno en otra máquina.

## Contenido del Respaldo
1.  **Skills:** Los 13 módulos de conocimiento experto (FastAPI, SQL, Frontend, etc.).
2.  **Brain:** El historial de esta conversación, planes de implementación y artefactos generados.

## Pasos para la Restauración

### 1. Preparar el nuevo Workspace
En la nueva máquina, crea una carpeta para el proyecto y abre Antigravity en ella.

### 2. Inyectar las Habilidades (Skills)
- Localiza la carpeta `.agents/skills` en el nuevo workspace. Si no existe, créala.
- Copia el contenido de la carpeta `skills` de este backup dentro de `.agents/skills`.
- Antigravity reconocerá automáticamente estas habilidades al reiniciar o indexar el proyecto.

### 3. Recuperar el Contexto (Brain)
- Antigravity guarda la información de la sesión en: `%APPDATA%\.gemini\antigravity\brain\[id-conversacion]`.
- Puedes copiar los archivos de la carpeta `brain` de este backup en la carpeta de la nueva sesión para que el asistente tenga acceso a los logs históricos (`overview.txt`) y a los planes de trabajo previos.

### 4. Sincronizar Código
- Clona el repositorio de GitHub: `https://github.com/SayayinSer/AntigravityTest`
- El backup también se encuentra dentro del repositorio en la carpeta `backups`.

---
**Respaldo generado el:** 09/04/2026 (Versión Beta)
**Proyecto:** Antigravity Workflow Engine
