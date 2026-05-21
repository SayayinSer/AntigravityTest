---
name: genexus-automation-msbuild
description: Skill experta para la automatización de tareas en GeneXus utilizando MSBuild. Permite realizar operaciones como importación/exportación de XPZ, reconstrucción de KB, ejecución de consultas y mantenimiento, siguiendo las mejores prácticas de DevOps y automatización industrial.
---

# GeneXus Automation & MSBuild Expert

Esta skill proporciona las capacidades necesarias para automatizar flujos de trabajo dentro de una Knowledge Base (KB) de GeneXus utilizando el motor de MSBuild. Está diseñada para ser utilizada en entornos de integración continua (CI), automatización de tareas repetitivas y gestión profesional de cambios.

## 1. Tareas Principales de MSBuild en GeneXus

El uso profesional de MSBuild en GeneXus se basa en la ejecución de tareas (`Tasks`) definidas en `Genexus.Tasks.targets`. Las operaciones más comunes son:

### A. Gestión de la KB
- **OpenKnowledgeBase**: Abre una KB existente. Es el paso previo obligatorio para cualquier otra tarea.
- **CloseKnowledgeBase**: Cierra la KB liberando recursos.
- **CheckKnowledgeBase**: Realiza una auditoría interna de la estructura de la KB.

### B. Gestión de Objetos (XPZ)
- **Import**: Importa un archivo XPZ o XML.
  - *Mejor Práctica*: Usar `PreviewMode='true'` antes de una importación real para validar impactos.
- **Export**: Exporta objetos seleccionados o toda la KB a un XPZ.

### C. Construcción y Generación
- **BuildAll**: Compila todos los objetos modificados.
- **RebuildAll**: Fuerza la recompilación de toda la KB.
- **GenerateOnly**: Genera el código fuente sin compilar los binarios.

## 2. Mejores Prácticas de Automatización

1. **Aislamiento de Logs**: Siempre redirigir la salida de MSBuild a archivos de log específicos para diagnóstico posterior (`/l:FileLogger,Microsoft.Build.Engine;logfile=Build.log`).
2. **Variables de Entorno**: No codificar rutas en los archivos `.msbuild`. Utilizar propiedades que puedan ser pasadas por la línea de comandos (`/p:KBPath=$(KBPath)`).
3. **Validación Previa (Gates)**: Antes de importar cambios masivos, ejecutar un `BuildAll` para asegurar que la KB base es estable.
4. **Manejo de Errores**: Capturar el código de salida de MSBuild. Un código diferente de 0 indica que la tarea falló o tuvo errores críticos.
5. **Seguridad**: Nunca incluir credenciales (DB, GAM) en los scripts de MSBuild. Utilizar variables de entorno o archivos de configuración seguros.

## 3. Ejemplo de Script MSBuild para Importación

```xml
<Project DefaultTargets="ImportXPZ" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Import Project="$(GX_PROGRAM_DIR)\Genexus.Tasks.targets" />
  <PropertyGroup>
    <KBPath>C:\Models\MiProyecto</KBPath>
    <XPZPath>C:\Envio_XPZ\Cambios.xpz</XPZPath>
  </PropertyGroup>
  <Target Name="ImportXPZ">
    <OpenKnowledgeBase KnowledgeBaseDir="$(KBPath)" />
    <Import File="$(XPZPath)" />
    <CloseKnowledgeBase />
  </Target>
</Project>
```

## 4. Estructura de Automatización Recomendada

- **`/scripts`**: Contiene wrappers de PowerShell o Bash que invocan a MSBuild:
  - `Invoke-GXImport.ps1`: Importación de XPZ.
  - `Invoke-GXRebuild.ps1`: Rebuild All de la KB.
  - `Invoke-GXImpact.ps1`: Análisis de impacto de base de datos.
- **`/msbuild`**: Contiene archivos `.msbuild` puros que definen las tareas.
- **`/logs`**: Carpeta para almacenar los resultados de cada ejecución.

---
*Usa esta skill para profesionalizar el ciclo de vida de desarrollo en GeneXus, reduciendo errores manuales y acelerando la entrega de valor.*
