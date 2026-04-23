---
name: fastapi-expert
description: Guía experta para el desarrollo de APIs profesionales con FastAPI. Incluye patrones de arquitectura modular, inyección de dependencias avanzada con Annotated, validación con Pydantic v2, seguridad JWT y testing asíncrono.
---

# FastAPI Expert Guide

Esta skill define los estándares para construir aplicaciones backend robustas, mantenibles y de alto rendimiento.

## 1. Estructura de Proyecto Sugerida (Modular)

Para proyectos que crecen, evita el archivo único `main.py`. Usa una estructura orientada a dominios o funcional:

```text
app/
├── api/              # Routers y definiciones de rutas
│   ├── v1/
│   │   ├── api.py    # Punto de entrada para v1
│   │   └── endpoints/ # Lógica de rutas específica
├── core/             # Configuración, seguridad, constantes
│   └── config.py
├── crud/             # Lógica de acceso a datos (opcional si usas services)
├── models/           # Modelos de base de datos (SQLAlchemy/SQLModel)
├── schemas/          # Modelos de Pydantic (Input/Output)
├── services/         # Lógica de negocio compleja
├── tests/            # Suite de pruebas
└── main.py           # Inicialización de FastAPI
```

## 2. Inyección de Dependencias (Estilo Moderno)

Utiliza `Annotated` para mejorar la legibilidad y facilitar el testing:

```python
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db

# Definición de tipos reutilizables
DBDep = Annotated[Session, Depends(get_db)]

@router.get("/{id}")
def read_item(id: int, db: DBDep):
    item = crud.item.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

## 3. Schemas y Validación (Pydantic v2)

- Usa `model_validate` y `model_dump` en lugar de los antiguos `from_orm` y `dict`.
- Separa claramente `ItemCreate`, `ItemUpdate` e `ItemPublic`.

```python
from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
```

## 4. Manejo Global de Errores y Middleware

Centraliza el manejo de excepciones para mantener respuestas consistentes:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong"},
    )
```

## 5. Pruebas Asíncronas (Testing)

Utiliza `pytest` con `httpx.AsyncClient` para probar endpoints `async`:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_read_main():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

## Checklist de Calidad Profesional

- [ ] **Documentación:** Usa `Summary` y `Description` en los decoradores de ruta.
- [ ] **Tipado Estricto:** Usa `mypy` para verificar tipos en todo el proyecto.
- [ ] **Security:** Implementa `OAuth2PasswordBearer` para rutas protegidas.
- [ ] **Background Tasks:** Usa `BackgroundTasks` nativo para envíos de correo o procesos ligeros.
- [ ] **Performance:** Configura `uvicorn` con múltiples workers en producción.
- [ ] **CORS:** Configura `CORSMiddleware` correctamente restringiendo orígenes.

---
*Usa esta skill para transformar requerimientos simples en infraestructuras de backend profesionales.*
