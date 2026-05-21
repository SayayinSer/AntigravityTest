---
name: project-context-vault
description: Guarda y recupera el contexto completo de un proyecto (tareas, errores, estados y metadatos) para asegurar la continuidad entre sesiones de IA. Permite capturar "instantáneas" del progreso y restaurarlas en nuevas sesiones.
---
# Project Context Vault (Bóveda de Contexto)

Esta Skill permite gestionar el "Estado de Conciencia" del agente respecto al proyecto actual. Su objetivo es evitar que se pierda información crítica cuando se inicia una nueva conversación o se cambia de contexto.

## Estructura del Contexto
El contexto se almacena en `d:\aaProyectos\Entorno04\.context/` y se organiza de la siguiente manera:
- `last_snapshot.json`: El estado más reciente capturado.
- `snapshots/`: Historial de estados anteriores (opcional).
- `task_board.md`: Una copia persistente de las tareas pendientes y completadas.

## Cuándo usar esta Skill
- **Al finalizar una sesión:** Para "congelar" el estado actual antes de cerrar.
- **Al iniciar una nueva sesión:** Para "leer la memoria" de lo que se estaba haciendo.
- **Cuando ocurre un error crítico:** Para documentar el estado exacto del error y las pruebas realizadas.
- **Al completar un hito (milestone):** Para dejar un registro histórico del éxito.

## Instrucciones de Operación

### 1. Guardar Contexto (`Save`)
Cuando el usuario pida "Guardar Contexto", el agente debe:
1. Recopilar información de:
   - `task.md` (si existe en la sesión actual).
   - `implementation_plan.md` y `walkthrough.md`.
   - Estado de los servicios MCP (ej. si la KB de GeneXus está abierta).
   - Lista de archivos modificados en la sesión.
2. Ejecutar el script `scripts/context_saver.py` para persistir esta información en `.context/last_snapshot.json`.
3. Actualizar `.context/task_board.md` con las tareas pendientes.

### 2. Recuperar Contexto (`Load`)
Cuando el usuario pida "Recuperar Contexto" o al inicio de una sesión:
1. Leer `.context/last_snapshot.json`.
2. Re-hidratar el archivo `task.md` de la sesión actual con la información recuperada.
3. Informar al usuario sobre:
   - ¿Qué se estaba haciendo?
   - ¿Qué tareas quedaron pendientes?
   - ¿Qué errores se estaban resolviendo?

### 3. Registro de Errores y Estados
- Utiliza la acción `add-error` para documentar fallos específicos sin necesidad de guardar todo el contexto.
- Comando: `python scripts/context_manager.py add-error --project "path" --session "path" --message "Descripción del error"`

## Checklist de Continuidad
Antes de finalizar una sesión, asegúrate de:
- [ ] Ejecutar `save` para capturar el estado actual.
- [ ] Verificar que `task_board.md` refleja la realidad del proyecto.
- [ ] Documentar cualquier "deuda técnica" o tarea pendiente en la sección de tareas.

## Restauración de Memoria
Al iniciar una nueva sesión, el primer paso del agente debe ser:
1. `load` el contexto anterior.
2. Leer el `last_snapshot.json` y el `task_board.md`.
3. Presentar un resumen al usuario: "Hola, recuperé el contexto. Nos quedamos en [Hito] con [N] tareas pendientes. ¿Continuamos con [Tarea X]?"

---
*Diseñado para la continuidad cognitiva en Entorno04.*
