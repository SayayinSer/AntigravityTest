# AI Agent Orchestration & Workspace Rules

Este documento define la capa de orquestación de inteligencia artificial para el proyecto **SayayinSer/AntigravityTest**. Establece las reglas de colaboración, los roles de los agentes y el uso de las habilidades especializadas disponibles.

## 1. Jerarquía de Agentes
- **Master Orchestrator (Antigravity)**: El agente principal responsable de la planificación de alto nivel, arquitectura y coordinación multi-stack. Utiliza la skill `software-architect-expert`.
- **Specialist Workers**: Agentes o sesiones activadas para tareas específicas (ej. Backend en Node.js, Frontend en Next.js, Modelado GeneXus).
- **Tool Automation (OpenCode CLI)**: Utilizado para tareas de terminal, integración MCP y despliegues rápidos.

## 2. Mapa de Skills y Roles
| Área Técnica | Skill Especialista | Rol de Agente |
| :--- | :--- | :--- |
| **Arquitectura** | `software-architect-expert` | Master Architect |
| **Frontend Moderno** | `nextjs-expert`, `frontend-design` | UI/UX Specialist |
| **Backend Node.js** | `nodejs-backend-expert` | Backend Engineer |
| **GeneXus / Nexa** | `nexa`, `genexus-expert` | GX Modeler |
| **Legacy / LAMP** | `php-mysql-expert`, `lamp-expert` | Legacy Backend Specialist |
| **Análisis** | `system-analyst-expert` | Quality & Logic Analyst |
| **Operaciones** | `devops-expert`, `infra-deploy-manager` | Deployment Manager |

## 3. Protocolos de Interacción
### Flujo A-P-E (Analyze-Plan-Execute)
Todo cambio significativo debe seguir este ciclo:
1.  **Análisis**: Escaneo de impacto global usando `system-analyst-expert`.
2.  **Planificación**: Generación de un `implementation_plan.md` supervisado por el `software-architect-expert`.
3.  **Ejecución**: Delegación a la skill especialista correspondiente.

### Sincronización de Skills
- El espacio de trabajo mantiene una copia local de todas las skills en `.agents/skills/`.
- Cualquier mejora en una skill local debe ser sincronizada con la base global en `%USERPROFILE%\.gemini\antigravity\skills\`.

## 4. Reglas del Espacio de Trabajo
- **Consistencia de UI**: Todas las interfaces deben respetar el diseño "Slate & Sky" (referenciado en `frontend-design`).
- **Seguridad**: No se permiten mutaciones de datos sin validación previa (ej. Zod para JS/TS, Prepared Statements para PHP).
- **Documentación**: Cada cambio debe dejar rastro en un `walkthrough.md`.

## 5. Recursos de Aprendizaje para Agentes
- **Skills Locales**: `./.agents/skills/`
- **Documentación de Referencia**: `./README.md`
- **Esquemas de Datos**: `./Location_CRUD.yaml`, `./Owner_CRUD.yaml`

---
*Este documento es un artefacto vivo. Los agentes deben consultarlo al inicio de cada sesión compleja.*
