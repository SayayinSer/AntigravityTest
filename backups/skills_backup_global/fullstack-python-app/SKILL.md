---
name: fullstack-python-app
description: Generador de aplicaciones web completas utilizando Python (FastAPI/Flask) en el backend y opciones frontend dinámicas (HTMX + Alpine.js o React + Vite). Permite discernir la mejor arquitectura según los requisitos de interactividad y escala.
---

# Fullstack Python App Factory Guide

Esta skill permite al agente construir aplicaciones web modernas, funcionales y estéticamente premium integrando el poder de Python con las mejores herramientas frontend gratuitas.

## 1. Lógica de Discernimiento (Arquitectura)

Antes de comenzar, se debe elegir el camino adecuado basándose en la complejidad:

| Característica | **HTMX + Alpine.js** | **React + Vite** |
| :--- | :--- | :--- |
| **Complejidad UI** | Baja a Media (Formularios, Tablas) | Alta (Dashboards, Drag & Drop) |
| **Aprendizaje** | Muy Simple (HTML nativo) | Medio (JavaScript/TypeScript) |
| **Desarrollo** | Ultra Rápido (Todo en Python/Templates) | Rápido (Proyecto separado) |
| **Interactividad** | Servidor-Céntrico | Cliente-Céntrico (SPA) |
| **SEO** | Nativo y Excelente | Requiere SSR (Next.js) |

## 2. Camino A: Minimalismo Potente (HTMX + Jinja2)

Ideal para aplicaciones de gestión, CRUDs y sitios que requieren alta velocidad de desarrollo.
- **Backend:** FastAPI con Jinja2Templates.
- **Frontend:** Atributos `hx-get`, `hx-post`, `hx-target` para actualizaciones parciales del DOM.
- **Interactividad local:** Uso de **Alpine.js** para modales, tabs y estados efímeros del cliente.

## 3. Camino B: Modernidad Reactiva (React + Vite)

Ideal para aplicaciones altamente interactivas, móviles y con estados complejos.
- **Backend:** FastAPI como API REST (JSON).
- **Frontend:** Proyecto desacoplado con Vite, React y TypeScript.
- **Comunicación:** Uso de `fetch` o `axios` mediante `useEffect` o `React Query`.

## 4. Estilo y Diseño (TailwindCSS)

Independientemente del camino elegido, se usará **TailwindCSS** para el diseño:
- **Productividad:** Clases de utilidad para un diseño rápido y premium.
- **Consistencia:** Uso de temas y tokens de diseño predefinidos.

## Checklist de Generación de App

- [ ] **Selección:** ¿Se ha decidido entre HTMX y React basándose en los RFs?
- [ ] **Estructura:** ¿Se han separado los directorios `api/` y `web/`?
- [ ] **Contract:** ¿Se han definido los esquemas de Pydantic para la comunicación?
- [ ] **Estética:** ¿Se ha aplicado el sistema de diseño (Tipografía, Gradients, Spacing)?

---
*Usa esta skill para materializar ideas en aplicaciones web reales con la agilidad de un experto.*
