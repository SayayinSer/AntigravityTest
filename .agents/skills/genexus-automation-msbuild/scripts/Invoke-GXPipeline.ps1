<#
.SYNOPSIS
  Ejecuta el pipeline completo: Import -> Impact/Reorg -> Build.
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$KBPath,
    
    [Parameter(Mandatory=$true)]
    [string]$XPZPath,
    
    [string]$GXDir = "C:\Program Files (x86)\GeneXus\GeneXus18"
)

$msbuild = "C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe"
$scriptPath = Join-Path (Split-Path $PSScriptRoot) "resources\Pipeline.msbuild"

Write-Host "Ejecutando Pipeline de Impacto para la KB..." -ForegroundColor Cyan
Write-Host "KB: $KBPath"
Write-Host "XPZ: $XPZPath"

& $msbuild $scriptPath "/p:KBPath=`"$KBPath`"" "/p:XPZPath=`"$XPZPath`"" "/p:GX_PROGRAM_DIR=`"$GXDir`"" "/v:m" "/l:FileLogger,Microsoft.Build.Engine;logfile=Pipeline.log"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Pipeline finalizado con éxito." -ForegroundColor Green
} else {
    Write-Error "El pipeline falló. Revise Pipeline.log para detalles técnicos."
}
