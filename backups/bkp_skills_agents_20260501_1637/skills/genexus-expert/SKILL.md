---
name: genexus-expert
description: Experto en el desarrollo con GeneXus (18 y Next), integrando la metodología oficial "Nexa" de GeneXus Labs y el sistema de diseño "Mercury". Capaz de modelar objetos (Transacciones, Procedimientos, APIs, Panels) en formatos estructurados (.md) y portables (.yaml).
---

# GeneXus Expert Guide (Nexa Methodology)

Esta skill permite al agente actuar como un consultor senior de GeneXus, aplicando los estándares más modernos de **GeneXus Labs**.

## 1. Metodología Nexa (Analyze-Plan-Execute)

Sigue este flujo de trabajo para cualquier cambio en la Base de Conocimientos (KB):

1.  **Analizar Intención:** Entender qué objeto se necesita crear o modificar.
2.  **Referenciar Conocimiento:** Consultar las especificaciones de objetos y tipos de datos en la carpeta `references/`.
3.  **Planear:** Definir la estructura del objeto utilizando el **Nexa DSL**.
4.  **Ejecutar:** Generar la definición final en formato `.md` (para análisis) o `.yaml` (para importación).

## 2. Nexa DSL: Definición de Objetos

Utiliza bloques de código estructurados para definir objetos GeneXus.

### Estructura General de un Objeto (YAML)
```yaml
object:
  name: ItemTransaction
  type: Transaction
  description: Items maintained by the system
  structure:
    - name: ItemId
      type: numeric(10)
      id: true
    - name: ItemName
      type: varchar(100)
    - name: ItemPrice
      type: numeric(12,2)
  rules:
    - rule: default(ItemDate, today())
    - rule: error("Price must be positive") if ItemPrice <= 0
```

## 3. Mercury Design System

Al diseñar interfaces (Panels/Web Panels), prioriza el uso de los componentes de **Mercury**.
- **Layouts:** Flex/Grid basados en Mercury.
- **Tokens:** Usa nombres de tokens semánticos de diseño.
- **Interacciones:** Prioriza eventos declarativos.

## 4. Soporte para GX18 y GeneXus Next

- **Lógica:** Enfócate en el uso de **Business Components** y **Objetos API**.
- **Despliegue:** Optimiza para infraestructuras Cloud-Native y Microservicios.
- **Model-Driven:** El conocimiento reside en el modelo, no en el código manual.

## Checklist de Calidad GeneXus

- [ ] **Normalización:** ¿El modelo de datos sigue las reglas de inferencia de GX?
- [ ] **Performance:** ¿Los Data Providers están optimizados con `Where` y `Order`?
- [ ] **Documentación:** ¿Cada objeto tiene una descripción clara y metadatos?
- [ ] **Formatos:** ¿Se han generado ambos formatos (.md y .yaml) si se requiere portabilidad?

---
*Usa esta skill para escalar el desarrollo en GeneXus con la precisión de una IA experta.*
