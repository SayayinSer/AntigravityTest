# Referencia de Objetos GeneXus (GX18 & Next)

Esta guía detalla la especificación técnica para los objetos principales de la Base de Conocimientos (KB) de GeneXus.

## 1. Transacciones (Transaction)
Definen el modelo de datos y las operaciones CRUD básicas.
- **Estructura:** Atributos con nombres semánticos.
- **Relaciones:** Inferidas por nombres de atributos idénticos.
- **Reglas:** Lógica declarativa (Default, Error, Msg).
- **Eventos:** After Trn, Start.

## 2. Procedimientos (Procedure)
Encapsulan la lógica de procesamiento y actualizaciones masivas.
- **Parámetros:** `Parm(in: &Var1, out: &Var2)`.
- **Layout:** Si es reporte (PDF/Excel), de lo contrario vacío.
- **Transaccionalidad:** Commit on Exit / rollback.

## 3. Data Providers (DP)
Definen estructuras de datos (SDTs) o colecciones de forma jerárquica.
- **Output:** Siempre devuelve un SDT o Business Component.
- **Cláusulas:** `Where`, `Order`, `Defined By`.

## 4. Objetos API
Exponen servicios REST o gRPC de forma profesional.
- **Sintaxis:**
```yaml
api:
  name: ItemService
  base_path: /api/items
  operations:
    - name: GetItems
      method: GET
      path: /all
      handler: ItemDP
    - name: CreateItem
      method: POST
      handler: ItemInsertProc
```

## 5. Panels (Mobile & Web)
Componentes de interfaz dinámica para GX18/Next.
- **Layout:** Controles de Mercury Design System.
- **Eventos:** `ClientStart`, `Refresh`, `ServerStart`.

---
*Consulta estas especificaciones antes de proponer cambios estructurales.*
