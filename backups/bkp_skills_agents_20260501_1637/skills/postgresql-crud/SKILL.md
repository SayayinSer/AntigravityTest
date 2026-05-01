---
name: postgresql-crud
description: Manejo eficiente de operaciones CRUD sobre PostgreSQL usando FastAPI y SQLAlchemy. Incluye utilidades genéricas, manejo de sesiones y mejores prácticas de esquemas.
---

# Guía de Gestión CRUD con PostgreSQL y SQLAlchemy

Este skill define patrones estandarizados para interactuar con bases de datos PostgreSQL de forma eficiente, segura y escalable.

## 1. Clase Base de CRUD Genérica

Para evitar la repetición de código (Boilerplate), utiliza una clase base que maneje las operaciones comunes:

```python
from typing import Any, Generic, TypeVar, Type, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
```

## 2. Organización de Esquemas (Pydantic)

Sigue la separación de responsabilidades para los datos:
- `Base`: Campos comunes.
- `Create`: Campos requeridos para creación.
- `Update`: Campos opcionales para actualización.
- `Out`: Formato de respuesta (incluye ID, timestamps).

## 3. Mejores Prácticas

- **Uso de Inyección de Dependencias**: Utiliza siempre el generador `get_db` en los endpoints de FastAPI.
- **Manejo de Errores**: Captura excepciones de integridad (como duplicados) y devuelve códigos HTTP apropiados (e.g., 400 Bad Request).
- **Relaciones**: Carga relaciones de forma eficiente usando `joinedload` o `subqueryload` para evitar el problema N+1.
- **Migraciones**: Utiliza Alembic para gestionar cambios en el esquema de la base de datos de forma controlada.

## 4. Flujo de Trabajo

1. Definir el **Modelo** de SQLAlchemy.
2. Definir los **Esquemas** de Pydantic.
3. Instanciar el **CRUD** heredando de `CRUDBase`.
4. Utilizar el CRUD en los **Rutas** de FastAPI.

---
*Este skill asegura un backend robusto y fácil de mantener.*
