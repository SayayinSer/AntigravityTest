---
name: KB Source Metadata
description: Valores de KMW e Source extraidos do XPZ mais recente da IDE â€” usados para montar o envelope de import_file.xml
updated: 2026-05-05T18:35:08.0000000Z
last_xpz_materialization_run_at: 2026-05-05T18:35:08.0000000Z
source_xpz: d:\aaProyectos\Entorno04\XpzExportadosPelaIDE\FullExport.xpz
source_refresh_status: partial-new
---

## KMW

| Campo        | Valor          |
|---|---|
| MajorVersion | 4  |
| MinorVersion | 0  |
| Build        | 187794         |

## Source

| Campo    | Valor       |
|---|---|
| kb (GUID) |     |
| username  |   |
| UNCPath   |    |

## Source/Version

| Campo | Valor        |
|---|---|
| guid  |  |
| name  |  |

## Uso

Ao gerar um `import_file.xml` ou `.xpz` para importacao na KB, usar estes valores
nos blocos `<KMW>` e `<Source>` do envelope `<ExportFile>`.