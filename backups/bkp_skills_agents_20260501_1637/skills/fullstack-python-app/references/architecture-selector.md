# Selector de Arquitectura: HTMX vs React

Guía para decidir el enfoque técnico de una aplicación web de Python.

## Criterio 1: Dinamismo de la Interfaz
- **HTMX:** Altamente recomendado para aplicaciones de gestión, CRUDs corporativos, dashboards informativos y sitios de contenido dinámico. Si el 90% de las acciones son "click -> cargar datos -> mostrar", HTMX es imbatible.
- **React:** Necesario para aplicaciones con estados complejos en el cliente (e.g., Editores de imagen, Juegos en el navegador, Drag & Drop avanzado, Colaboración en tiempo real).

## Criterio 2: Conocimiento Técnico
- **HTMX:** Bajísima curva de entrada. Un desarrollador de Python/FastAPI puede ser experto en HTMX en horas. No requiere Webpack, Babel ni NPM complejo.
- **React:** Requiere conocimiento sólido de JavaScript (ES6+), Hooks y el ecosistema de Node.js.

## Criterio 3: Rendimiento y SEO
- **HTMX:** Envía HTML parcial desde el servidor. El primer renderizado es instantáneo y es 100% amigable para buscadores (SEO) de forma nativa.
- **React:** El cliente debe descargar el bundle de JS antes de renderizar (LCP más lento). Requiere técnicas de SSR (Server Side Rendering) para un SEO óptimo.

## Criterio 4: Conclusión (Regla de Oro)
> *"Si no necesitas un estado complejo y persistente en el lado del cliente que deba sobrevivir a las navegaciones, elige HTMX. Si tu UI es una herramienta de software interactiva e independiente de la navegación, elige React."*

---
*Usa este selector como el primer paso de cualquier análisis de arquitectura.*
