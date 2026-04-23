---
name: fullstack-node-react
description: Guía experta para el desarrollo de aplicaciones Fullstack profesionales utilizando Node.js, React, TypeScript y Prisma. Optimizada para arquitecturas Monorepo y soporte multi-dialecto SQL (PostgreSQL, MySQL, MariaDB, SQL Server).
---
# Fullstack Node-React Pro - Skill Guide

Esta Skill define los estándares de oro para construir aplicaciones modernas, seguras y escalables con un enfoque en la productividad y la robustez del tipo.

## 1. Arquitectura Monorepo Estándar
Se recomienda una estructura simplificada pero potente:
```text
/root
  ├── /client (React + Vite + TS)
  ├── /server (Node + Express + TS)
  ├── /common (Opcional: tipos compartidos)
  ├── package.json (Configuración de Workspaces)
  └── .env (Configuración centralizada)
```

## 2. Backend (Node.js + Express + TypeScript)
- **Patrón de Capas**: Router -> Controller -> Service -> Prisma.
- **Validación**: Usar `zod` para validar inputs de API y variables de entorno.
- **Seguridad**: Implementar JWT para autenticación y Middlewares para control de acceso.

## 3. Persistencia (Prisma ORM)
Prisma permite manejar múltiples motores SQL de forma profesional:
- **Configuración**: El archivo `schema.prisma` debe parametrizar el `provider` mediante variables de entorno.
- **Migraciones**: Realizar siempre `npx prisma migrate dev` para mantener el versionado de la base de datos.
- **Motores Soportados**:
  - `postgresql`: Para despliegues robustos (recomendado).
  - `mysql` / `mariadb`: Para compatibilidad legacy o alta disponibilidad simple.
  - `sqlserver`: Para entornos empresariales corporativos.

## 4. Frontend (React + Vite + TypeScript)
- **Componentes**: Basados en funciones, tipados estrictamente con Interfaces.
- **Estado Global**: Usar `Zustand` para un manejo ligero o `Redux Toolkit` para flujos complejos.
- **Fetch de Datos**: Priorizar `TanStack Query` (React Query) para manejo de caché y estados de carga.
- **Estilos**: `Tailwind CSS` por defecto para agilidad y diseño premium.

## 5. Checklist de Calidad Profesional
- [ ] Configuración estricta de `tsconfig.json` en ambos proyectos.
- [ ] Uso de `.env.example` para documentar secrets.
- [ ] Manejo centralizado de errores en el Backend (Error Middleware).
- [ ] Optimización de imágenes y assets en el Frontend.
- [ ] Documentación de API mediante Swagger/OpenAPI o `ts-rest`.

---
*Usa esta skill cuando el usuario solicite crear módulos, refactorizar lógica fullstack o integrar nuevas entidades de base de datos en aplicaciones Node/React.*
