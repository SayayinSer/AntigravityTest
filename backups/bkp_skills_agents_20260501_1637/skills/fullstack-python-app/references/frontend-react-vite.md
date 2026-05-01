# Guía Frontend Moderno: React + Vite + TypeScript

Esta guía detalla el flujo de trabajo profesional para aplicaciones dinámicas, reactivas y escalables.

## 1. Stack Tecnológico Estándar
- **React:** Biblioteca para interfaces de usuario basadas en componentes.
- **Vite:** Herramienta de construcción (build tool) ultra rápida para desarrollo moderno.
- **TypeScript:** Seguridad de tipos de extremo a extremo para evitar errores en producción.
- **Tailwind CSS:** Sistema de diseño atómico para estilizado rápido y consistente.

## 2. Integración con Python (FastAPI)
- **Comunicación JSON:** Uso de `fetch` o `Axios` para consumir los endpoints de la API.
- **CORS:** Asegurar que el backend de FastAPI permita peticiones desde el origen del frontend (e.g., `localhost:5173`).
- **Data Fetching:** Se recomienda el uso de **React Query** o **SWR** para manejar el estado de las peticiones, caché y reintentos.

## 3. Estructura de Proyecto React
```text
src/
├── components/     # Componentes atómicos (Button, Input, Card)
├── hooks/          # Hooks personalizados (useAuth, useData)
├── pages/          # Pantallas principales (Home, Dashboard)
├── services/       # Clientes de API (api.ts)
├── store/          # Estado global (Zustand/Redux/Context)
└── types/          # Definiciones de interfaces TypeScript
```

## 4. Diseño Dinámico y Premium
- **Framer Motion:** Biblioteca recomendada para animaciones de entrada, salida y transiciones de estado.
- **Lucide React:** Set de iconos limpios y consistentes.
- **Design Tokens:** Define el `tailwind.config.js` con los colores, fuentes y espaciados de la marca.

---
*Usa esta guía para construir aplicaciones de software de clase mundial con la mejor experiencia de usuario.*
