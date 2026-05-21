<#
.SYNOPSIS
  Wrapper para ejecutar Rebuild All en una KB.
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$KBPath,
    [string]$GXDir = "C:\Program Files (x86)\GeneXus\GeneXus18"
)

$msbuild = "C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe"
$scriptPath = Join-Path (Split-Path $PSScriptRoot) "resources\Rebuild.msbuild"

Write-Host "Iniciando REBUILD ALL en $($KBPath)..." -ForegroundColor Cyan
& $msbuild $scriptPath "/p:KBPath=`"$KBPath`"" "/p:GX_PROGRAM_DIR=`"$GXDir`"" "/v:m" "/l:FileLogger,Microsoft.Build.Engine;logfile=Rebuild.log"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Rebuild completado con éxito." -ForegroundColor Green
} else {
    Write-Error "Error durante el Rebuild. Consulte Rebuild.log."
}
