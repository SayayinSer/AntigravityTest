---
name: nextjs-expert
description: Experto sénior en Next.js con enfoque en App Router, Server Components y patrones de arquitectura escalable.
---

# Next.js Expert Skill (Senior Level)

Esta skill proporciona las directrices maestras para el desarrollo de aplicaciones de vanguardia con Next.js, priorizando el rendimiento, la mantenibilidad y la experiencia del usuario.

## 1. Arquitectura y Estructura (App Router)
- **Colocación (Colocation)**: Mantener componentes, estilos y tests cerca de la ruta que los utiliza.
- **Rutas Privadas**: Utilizar la convención `_folder` para organizar código interno que no debe ser accesible vía URL.
- **Layouts Anidados**: Maximizar el uso de layouts para persistencia de estado de UI y reducción de re-renderizados.
- **Parallel & Intercepting Routes**: Implementar dashboards complejos y modales contextuales sin perder el estado de la URL.

## 2. Estrategia de Datos y Server Components
- **Server Components por Defecto**: Utilizar Server Components para fetch de datos, acceso a BD y lógica pesada.
- **Client Boundaries**: Mover el estado interactivo (`useState`, `useEffect`) lo más abajo posible en el árbol de componentes.
- **Fetching Eficiente**: Utilizar `fetch` nativo con caché automático y `revalidateTag` / `revalidatePath` para actualizaciones granulares.
- **Streaming**: Implementar `loading.js` y `Suspense` para mejorar el Time to First Byte (TTFB).

## 3. Form Handling y Server Actions
- **Server Actions**: Centralizar la mutación de datos en acciones de servidor seguras.
- **Validación con Zod**: Validar siempre el `formData` en el servidor antes de procesar.
- **Estado Progresivo**: Usar `useFormStatus` y `useFormState` para feedbacks instantáneos y manejo de errores.
- **Optimistic Updates**: Implementar `useOptimistic` para una UI instantánea antes de confirmar en el servidor.

## 4. Rendimiento y Optimización
- **Optimización de Imágenes**: Uso estricto de `next/image` con tamaños y prioridades correctas.
- **Fonts & Scripts**: Cargar fuentes locales o de Google vía `next/font` para evitar CLS.
- **Partial Prerendering (PPR)**: (Experimental) Combinar partes estáticas y dinámicas en una misma ruta.
- **Bundle Analysis**: Monitorear el tamaño del cliente para evitar dependencias innecesarias en componentes cliente.

## 5. SEO y Seguridad
- **Metadata API**: Generar metadatos dinámicos para SEO social y técnico.
- **Middleware**: Gestionar autenticación, internacionalización y redirecciones a nivel de edge.
- **Security Headers**: Configurar CSP y otros headers críticos en `next.config.js`.

## Checklist Sénior
- [ ] ¿Se ha minimizado el uso de `"use client"`?
- [ ] ¿Los datos se obtienen lo más cerca posible de donde se consumen?
- [ ] ¿Se utiliza `Suspense` para las partes lentas de la página?
- [ ] ¿Las acciones de servidor validan tipos y permisos?
- [ ] ¿Se ha verificado el Core Web Vitals en producción?

---
*Usa esta skill para construir aplicaciones Next.js que definan el estándar de la industria.*
