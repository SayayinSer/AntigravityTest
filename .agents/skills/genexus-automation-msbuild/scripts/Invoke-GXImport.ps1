<#
.SYNOPSIS
  Wrapper profesional para ejecutar tareas de MSBuild en GeneXus.
.DESCRIPTION
  Automatiza la llamada a MSBuild asegurando que las rutas de GeneXus y la KB sean correctas.
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$KBPath,
    
    [Parameter(Mandatory=$true)]
    [string]$XPZPath,
    
    [string]$GXDir = "C:\Program Files (x86)\GeneXus\GeneXus18",
    
    [switch]$Preview
)

$msbuild = "C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe"
$scriptPath = Join-Path (Split-Path $PSScriptRoot) "resources\Import.msbuild"

if (-not (Test-Path $GXDir)) {
    Write-Error "GeneXus directory not found: $GXDir"
    return
}

$previewVal = if ($Preview) { "true" } else { "false" }

$args = @(
    $scriptPath,
    "/p:KBPath=`"$KBPath`"",
    "/p:XPZPath=`"$XPZPath`"",
    "/p:GX_PROGRAM_DIR=`"$GXDir`"",
    "/p:PreviewMode=$previewVal",
    "/v:m",
    "/l:FileLogger,Microsoft.Build.Engine;logfile=GeneXus_Automation.log"
)

Write-Host "Iniciando automatización MSBuild para GeneXus..." -ForegroundColor Cyan
& $msbuild $args

if ($LASTEXITCODE -eq 0) {
    Write-Host "Operación completada exitosamente." -ForegroundColor Green
} else {
    Write-Error "La operación falló. Revise GeneXus_Automation.log para más detalles."
}
