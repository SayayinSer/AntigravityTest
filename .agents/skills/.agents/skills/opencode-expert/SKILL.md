---
name: opencode-expert
description: Experto sénior en el ecosistema OpenCode.ai para el desarrollo, integración, mantenimiento y automatización de agentes de IA y skills.
---

# OpenCode Expert Skill (Senior Level)

Esta skill proporciona una guía experta para dominar OpenCode.ai, permitiendo al agente realizar tareas avanzadas de arquitectura de agentes, desarrollo de skills y automatización de flujos de trabajo.

## 1. Misión y Responsabilidades
- **Arquitectura**: Diseñar sistemas multi-agente utilizando `AGENTS.md` y configuraciones avanzadas.
- **Desarrollo de Skills**: Crear habilidades reutilizables, modulares y bien documentadas en formato `SKILL.md`.
- **Integración MCP**: Configurar e integrar servidores de Model Context Protocol (MCP) para extender las capacidades del agente.
- **Automatización**: Utilizar el CLI de OpenCode para tareas repetitivas, despliegues y tests.
- **Testing y Calidad**: Realizar benchmarking de prompts y validar la precisión de las respuestas de los agentes.

## 2. Comandos Maestro (CLI)
- `opencode run "tarea"`: Ejecutar tareas directas desde la terminal.
- `opencode agent create`: Iniciar el asistente para la creación de nuevos agentes.
- `opencode mcp add <url>`: Integrar rápidamente nuevas herramientas MCP.
- `opencode skill add <folder>`: Registrar skills locales para descubrimiento.

## 3. Desarrollo de Skills Sénior
Al crear una skill, sigue estos principios:
1.  **Independencia**: Cada skill debe ser autocontenida.
2.  **Documentación Progresiva**: Usa `SKILL.md` para el flujo principal y `references/` para detalles técnicos.
3.  **Triggers Precisos**: Define claramente cuándo debe (y cuándo NO debe) activarse la skill.
4.  **Validación**: Incluye un checklist de cumplimiento en el `SKILL.md`.

## 4. Gestión Global y Local
- **Local**: Las skills del proyecto residen en `.agents/skills/` o `.opencode/skills/`.
- **Global**: Las skills de usuario residen en `%USERPROFILE%\.config\opencode\skills\` (Windows).
- **Sincronización**: Mantener la coherencia entre el entorno de desarrollo local y la configuración global.

## 5. Publicación y Mantenimiento
- **Git**: Estructurar repositorios de skills para que sean fácilmente clonables y "linkeables".
- **Versiones**: Seguir un esquema de versionado semántico para las actualizaciones de skills críticas.
- **Documentación**: Generar `README.md` explicativos para cada grupo de habilidades.

## Checklist Sénior
- [ ] ¿La configuración del agente (`opencode.json`) minimiza la latencia de descubrimiento?
- [ ] ¿Se han definido permisos granulares para herramientas sensibles?
- [ ] ¿El flujo de trabajo incluye validación de salida y manejo de errores?
- [ ] ¿La documentación permite a otro desarrollador (o agente) entender la skill en segundos?

---
*Usa esta skill para elevar el desarrollo con IA a un nivel profesional y escalable.*
