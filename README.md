# Entorno01 - Aplicación Web (FastAPI + PostgreSQL + Frontend Nativo)

Este proyecto divide de forma limpia el backend y el frontend.

## 🚀 Requisitos
1. **Python 3.8+**
2. **PostgreSQL** instalado y ejecutándose localmente.

## 🛠️ Configuración e Inicialización

### 1. Backend
El backend está construido con FastAPI y usa SQLAlchemy para conectar a PostgresSQL.

1. Abre una terminal en la carpeta `backend`:
   ```bash
   cd backend
   ```
2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configura tu Base de Datos**: 
   Abre el archivo `backend\.env` y modifica la variable `DATABASE_URL` con tus credenciales de PostgreSQL. Asegúrate de crear la base de datos (por ejemplo, `entorno01_db`) en pgAdmin o tu cliente SQL.
5. Inicia el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload
   ```
   *La API estará disponible en http://127.0.0.1:8000*
   *Puedes ver la documentación interactiva en http://127.0.0.1:8000/docs*

### 2. Frontend
El frontend es estático y no requiere instalación de dependencias, pero necesita el backend en ejecución para funcionar.

1. Navega a la carpeta `frontend`.
2. Puedes abrir directamente el archivo `index.html` en tu navegador haciendo doble clic, o usar una extensión como "Live Server" en VS Code.
3. Asegúrate de que el puerto configurado en `app.js` (por defecto `http://localhost:8000`) coincida con el puerto donde está corriendo FastAPI.

## 📁 Estructura del proyecto
- `/backend`: Lógica de servidor, modelos de datos, rutas de la API, y conexión a BD.
- `/frontend`: Interfaz de usuario (HTML, CSS oscuro premium, y llamadas Fetch en JS).
