<#
.SYNOPSIS
  Wrapper para ejecutar Análisis de Impacto en una KB.
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$KBPath,
    [string]$GXDir = "C:\Program Files (x86)\GeneXus\GeneXus18"
)

$msbuild = "C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe"
$scriptPath = Join-Path (Split-Path $PSScriptRoot) "resources\Impact.msbuild"

Write-Host "Iniciando Análisis de Impacto en $($KBPath)..." -ForegroundColor Cyan
& $msbuild $scriptPath "/p:KBPath=`"$KBPath`"" "/p:GX_PROGRAM_DIR=`"$GXDir`"" "/v:m" "/l:FileLogger,Microsoft.Build.Engine;logfile=Impact.log"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Análisis de impacto completado. Revise el reporte en la KB." -ForegroundColor Green
} else {
    Write-Error "Error durante el análisis de impacto. Consulte Impact.log."
}
