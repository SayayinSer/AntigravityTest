#requires -version 5.1
<#
.SYNOPSIS
Wrapper local sanitizado para validar o contrato de Get-77LabKbMetadata.ps1.

.DESCRIPTION
Executa o script compartilhado `Test-XpzKbMetadataWrapper.ps1` para conferir se
o wrapper local `Get-77LabKbMetadata.ps1` expoe os campos obrigatorios existentes em
`kb-source-metadata.md`: `last_xpz_materialization_run_at`, `kb_name` e
`source_guid`.

Este wrapper deve ser usado em auditorias de setup para impedir que um
`Get-77LabKbMetadata.ps1` funcional apenas em parse seja classificado como
EQUIVALENTE quando falha em expor campos existentes no metadata local.

.PARAMETER MetadataPath
Caminho opcional para kb-source-metadata.md. Quando omitido, usa o arquivo na
raiz da pasta paralela.

.PARAMETER MetadataWrapperPath
Caminho opcional para Get-77LabKbMetadata.ps1. Quando omitido, usa o wrapper local na
mesma pasta `scripts`.

.PARAMETER SharedSkillsRoot
Raiz local da base compartilhada `GeneXus-XPZ-Skills`.

.EXAMPLE
.\Test-77LabKbMetadataWrapper.ps1

.EXAMPLE
.\Test-77LabKbMetadataWrapper.ps1 -MetadataPath C:\KB\kb-source-metadata.md -MetadataWrapperPath C:\KB\scripts\Get-77LabKbMetadata.ps1
#>

param(
    [string]$MetadataPath,

    [string]$MetadataWrapperPath,

    [string]$SharedSkillsRoot = "d:\aaProyectos\Entorno04\.agents\skills"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$KbRoot = Split-Path -Parent $PSScriptRoot
$repoRoot = $KbRoot
$SharedSkillsRoot = "d:\aaProyectos\Entorno04\.agents\skills"

if (-not $MetadataPath) {
    $MetadataPath = Join-Path $repoRoot "kb-source-metadata.md"
}

if (-not $MetadataWrapperPath) {
    $MetadataWrapperPath = Join-Path $PSScriptRoot "Get-77LabKbMetadata.ps1"
}

$enginePath = Join-Path $SharedSkillsRoot "scripts-xpz\Test-XpzKbMetadataWrapper.ps1"
if (-not (Test-Path -LiteralPath $enginePath -PathType Leaf)) {
    throw "Shared metadata wrapper test not found: $enginePath"
}

& $enginePath -MetadataPath $MetadataPath -WrapperPath $MetadataWrapperPath
