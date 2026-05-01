---
name: openapi-integration
description: Integración, uso y operación con APIs REST basadas en especificaciones OpenAPI/Swagger en formato YAML 3.0 de forma sencilla y natural.
---

# Skill de Integración OpenAPI 3.0 (YAML)

Este skill permite operar con cualquier API REST partiendo de su definición en formato YAML 3.0, facilitando la generación de clientes, la validación de peticiones y la exploración de endpoints.

## 1. Exploración Natural de la API

Para usar una API de forma "natural", el agente debe:
- **Identificar el Root**: Localizar el archivo YAML (e.g., `openapi.yaml`, `swagger.yaml`).
- **Mapear Endpoints**: Listar rutas, métodos y descripciones resumidas.
- **Entender el Contrato**: Identificar esquemas de entrada (Request Body) y salida (Response).

## 2. Generación Rápida de Clientes (Python)

Patrón para integrar un endpoint específico usando `httpx` y Pydantic:

```python
import httpx
from pydantic import BaseModel
from typing import List

# Basado en el esquema de la API en el YAML
class User(BaseModel):
    id: int
    name: str

async def get_users() -> List[User]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/users")
        response.raise_for_status()
        return [User(**item) for item in response.json()]
```

## 3. Operación Directa con YAML

Si se dispone de herramientas de CLI, se pueden automatizar tareas:
- **Validación**: `openapi-generator-cli validate -i spec.yaml`
- **Mocking**: `prism mock spec.yaml`
- **Generación Total**: `openapi-generator-cli generate -i spec.yaml -g python -o ./client`

## 4. Mejores Prácticas de Integración

- **Seguridad**: Manejar `securitySchemes` (Bearer, API Key) de forma segura mediante variables de entorno o archivos `.env`.
- **Manejo de Errores**: Implementar lógica para códigos 4xx y 5xx basados en las respuestas definidas en el YAML.
- **Resiliencia**: Añadir reintentos (retries) y timeouts adecuados para operaciones de red.
- **Actualización**: Sincronizar el código cliente siempre que la especificación YAML cambie.

---
*Este skill facilita la integración fluida con servicios externos y la consistencia entre la documentación y la implementación.*
