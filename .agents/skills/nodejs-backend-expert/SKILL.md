---
name: nodejs-backend-expert
description: Especialista sénior en desarrollo backend con Node.js, enfocado en arquitecturas escalables, seguridad avanzada y alto rendimiento.
---

# Node.js Backend Expert Skill (Senior Level)

Esta skill proporciona las directrices para diseñar y construir soluciones backend de nivel empresarial utilizando Node.js, priorizando la robustez y la excelencia técnica.

## 1. Arquitectura Limpia (Clean Architecture)
- **Desacoplamiento**: Separar claramente las capas de Infraestructura, Dominio, Aplicación e Interfaz.
- **Inyección de Dependencias**: Utilizar patrones de DI para facilitar el testing y la modularidad.
- **Controladores Delgados**: Los controladores solo deben validar la entrada y delegar la lógica a los Casos de Uso/Servicios.
- **Domain-Driven Design (DDD)**: Aplicar conceptos de DDD para sistemas complejos (Aggregates, Value Objects, Repositories).

## 2. TypeScript y Estándares Modernos
- **ESM Nativo**: Usar `"type": "module"` y sintaxis de `import/export`.
- **Tipado Estricto**: Configuración de TypeScript con `strict: true` y sin uso de `any`.
- **Zod Validation**: Validar esquemas de datos en tiempo de ejecución para asegurar la integridad de las entradas (Body, Query, Params).

## 3. Seguridad Avanzada
- **Defensa en Capas**: Implementar `helmet` para cabeceras de seguridad, límites de tasa (rate limiting) y validación estricta de CORS.
- **Gestión de Secretos**: Nunca hardcodear credenciales; usar variables de entorno seguras y gestores de secretos.
- **Auditoría de Dependencias**: Ejecutar `npm audit` y usar herramientas como Snyk para prevenir vulnerabilidades en la cadena de suministro.

## 4. Rendimiento y Escalabilidad
- **I/O No Bloqueante**: Uso correcto de `async/await` y evitar operaciones síncronas que bloqueen el Event Loop.
- **Worker Threads**: Delegar tareas pesadas de CPU a hilos de trabajo independientes.
- **Estrategias de Caché**: Implementar Redis para datos distribuidos y caché en memoria para conjuntos de datos volátiles y pequeños.
- **Observability**: Logging estructurado con `Pino` y rastreo distribuido con OpenTelemetry.

## 5. Testing de Alta Calidad
- **Pirámide de Tests**: Priorizar tests unitarios y de integración.
- **Entornos Aislados**: Usar contenedores efímeros (Testcontainers) para pruebas con bases de datos reales.
- **AAA Pattern**: Estructurar los tests con Arrange, Act, Assert para máxima legibilidad.

## Checklist Sénior
- [ ] ¿La lógica de negocio está totalmente aislada de la infraestructura?
- [ ] ¿Se utiliza TypeScript de forma estricta sin `any`?
- [ ] ¿Todas las entradas externas están validadas con esquemas (ej. Zod)?
- [ ] ¿Se han implementado logs estructurados y métricas de salud?
- [ ] ¿El sistema escala horizontalmente sin estado compartido?

---
*Usa esta skill para liderar el desarrollo de backends Node.js con rigor técnico y visión arquitectónica.*
