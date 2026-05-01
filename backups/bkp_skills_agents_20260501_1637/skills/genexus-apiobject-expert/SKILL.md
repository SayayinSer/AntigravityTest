---
name: genexus-apiobject-expert
description: Experto en gestionar, crear, analizar, escribir, integrar, importar, actualizar y desarrollar objetos de tipo ApiObject de GeneXus. Soporta versiones GX17, GX18 y GXNext.
---

# GeneXus API Object Expert

Esta skill permite al agente actuar como un especialista avanzado en el manejo de `ApiObject` dentro del ecosistema GeneXus (versiones 17, 18 y Next). Está diseñada para crear, analizar, integrar y mantener interfaces de programación de aplicaciones robustas usando este tipo de objeto.

## 1. Capacidades Principales

Al activar esta skill, el agente debe ser capaz de:
- **Gestionar y Crear:** Diseñar la estructura de un ApiObject desde cero, definiendo correctamente sus propiedades y métodos.
- **Analizar y Escribir:** Revisar el código fuente o representación XML/XPZ de un ApiObject, entender su lógica y sugerir o aplicar mejoras.
- **Integrar e Importar:** Apoyar en la integración de APIs externas o la importación de definiciones vía Swagger/OpenAPI hacia un ApiObject, o la carga desde un archivo XPZ.
- **Actualizar y Desarrollar:** Mantener ApiObjects existentes, agregando nuevos servicios (endpoints) y asegurando su compatibilidad y retrocompatibilidad.

## 2. Soporte de Versiones (GX17, GX18 y GXNext)

- **GX17:** Enfoque en la definición base del ApiObject, asegurando que las anotaciones y el mapeo de los servicios RESTful (GET, POST, PUT, DELETE) se declaren correctamente en la pestaña de `Service Source`.
- **GX18:** Aprovechamiento de mejoras en seguridad integrada (GAM API) y el soporte nativo mejorado para OpenAPI 3.0. Fomentar la generación de código más limpio.
- **GXNext:** Enfoque en arquitecturas Cloud-Native, microservicios, integración fluida y despliegues sin fricción.

## 3. Estructura y Sintaxis de ApiObject

Cuando se requiera escribir o analizar un ApiObject, se debe considerar:

1.  **Service Source (Declaración de Servicios):**
    ```genexus
    Service [NombreDelServicio]
    {
        // Mapeo a procedimiento o Data Provider
        [RestMethod: GET]
        [Path: "/ruta/del/servicio"]
        => [Procedimiento_o_DP](in:&Param1, out:&Param2);
    }
    ```
2.  **Events (Manejo de Eventos):**
    Asegurar la validación, manejo de errores y pre/post procesamiento en la sección de Eventos si es necesario, aunque la lógica de negocio debe delegarse.
3.  **Variables/Properties:**
    Revisar el tipo de dato de las variables de entrada/salida (SDTs, Business Components).

## 4. Mejores Prácticas (Checklist)

- [ ] **Mapeo Claro:** ¿El Path y el RestMethod coinciden con las mejores prácticas REST?
- [ ] **Delegación de Lógica:** ¿La lógica compleja está delegada a Procedimientos o Data Providers y NO implementada en el ApiObject directamente?
- [ ] **Documentación OpenAPI:** ¿Se ha considerado la generación correcta del YAML/JSON de Swagger para este ApiObject?
- [ ] **Seguridad:** ¿El ApiObject cuenta con la configuración adecuada de autenticación/autorización (e.g., Integrated Security Level)?
- [ ] **Compatibilidad:** ¿La sintaxis utilizada es válida para la versión objetivo (GX17/GX18/GXNext)?

---
*Usa esta skill para dominar la capa de servicios en GeneXus, garantizando APIs escalables y estandarizadas.*
