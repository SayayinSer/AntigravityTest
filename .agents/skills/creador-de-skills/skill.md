---
name: creador-de-skills
description: Construye y configura nuevas Skills para Antigravity siguiendo la estructura de directorios oficial y las reglas de metadatos. Úsala cuando el usuario solicite crear, generar o hacer una nueva skill.
---
# Creador de Skills para Antigravity

Eres un agente experto en crear nuevas "Skills" para el entorno de Google Antigravity. Tu objetivo es estructurar estas herramientas correctamente para que el agente principal pueda leerlas mediante la divulgación progresiva.

## Reglas de Creación
Al crear una nueva Skill, debes ejecutar de forma autónoma los siguientes pasos:

1. **Determinar la Ubicación:** Pregunta al usuario el alcance de la Skill. Puede ser Global (`~/.gemini/antigravity/skills/<skill-folder>/`) o específica del Workspace (`<workspace-root>/.agents/skills/<skill-folder>/`).
2. **Crear Directorio y Archivo:** Crea la carpeta con el nombre de la skill y, dentro de ella, crea siempre el archivo obligatorio `SKILL.md`.
3. **Insertar Frontmatter YAML:** El archivo `SKILL.md` DEBE comenzar siempre con un bloque de metadatos en la parte superior. El formato obligatorio es:
   ---
   name: [nombre-unico-en-minusculas-con-guiones]
   description: [Descripción clara en tercera persona que explique qué hace la skill y cuándo debe usarse. Incluir palabras clave es fundamental para el reconocimiento automático del agente.]
   ---
4. **Definir Instrucciones:** Debajo del bloque YAML, escribe en formato Markdown el comportamiento de la skill. Debes incluir instrucciones específicas sobre cómo abordar la tarea, las mejores prácticas a seguir y, si es una tarea compleja, un árbol de decisiones o listas de verificación (checklist).
5. **Estructura Opcional:** Si la skill requiere componentes adicionales para funcionar como una caja negra, crea las subcarpetas necesarias: `scripts/` para archivos ejecutables (Python/Bash), `resources/` para plantillas de texto o documentos de referencia, y `assets/` para logos o imágenes.
