# Guía Frontend Minimalista: HTMX + Alpine.js

Esta guía detalla cómo crear interfaces potentes, dinámicas y profesionales utilizando estándares ligeros y eficientes.

## 1. El Trío Dinámico (HTMX, Alpine, Tailwind)
- **HTMX:** Maneja la comunicación con el servidor mediante atributos HTML para intercambiar fragmentos del DOM.
- **Alpine.js:** Maneja la interactividad puramente del lado del cliente (modales, dropdowns, estados temporales).
- **Tailwind CSS:** Proporciona los estilos visuales premium sin necesidad de escribir CSS personalizado.

## 2. Patrones Comunes de HTMX
```html
<!-- Actualización parcial de una tabla al buscar -->
<input type="text" name="q" placeholder="Buscar..." 
       hx-get="/search" hx-trigger="keyup changed delay:500ms" 
       hx-target="#search-results" hx-indicator=".loader">

<div id="search-results">
    <!-- Aquí se inyectará el HTML devuelto por el servidor -->
</div>
```

## 3. Interactividad con Alpine.js
```html
<!-- Modal sencillo y potente -->
<div x-data="{ open: false }">
    <button @click="open = true" class="btn-primary">Abrir Perfil</button>
    
    <div x-show="open" @click.away="open = false" class="modal-overlay">
        <div class="modal-content">
            <h2>Datos del Usuario</h2>
            <button @click="open = false">Cerrar</button>
        </div>
    </div>
</div>
```

## 4. Estética Premium Automática
- **Gradients:** Usa gradientes suaves en fondos y botones.
- **Micro-animaciones:** Aplica transiciones suaves con clases de Tailwind (`transition-all duration-300`).
- **Glassmorphism:** Usa `backdrop-blur-md` y opacidades para un look moderno.

---
*Usa esta guía para construir aplicaciones rápidas, sencillas y visualmente impactantes.*
