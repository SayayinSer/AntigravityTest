<#
.SYNOPSIS
  Impacta los cambios de la Versión 2 (Caja + Zona API) en la KB 77Lab.
#>
$KBPath = "D:\Models\77Lab\AngularV1"
$XPZPath = "d:\aaProyectos\Entorno04\Envio_XPZ\API_Zonas_V6.xml"
$PipelineScript = "d:\aaProyectos\Entorno04\.agents\skills\genexus-automation-msbuild\scripts\Invoke-GXPipeline.ps1"

Write-Host "Iniciando Impacto de Versión 2 (77Lab)..." -ForegroundColor Cyan

& $PipelineScript -KBPath $KBPath -XPZPath $XPZPath

if ($LASTEXITCODE -eq 0) {
    Write-Host "Versión 2 impactada correctamente." -ForegroundColor Green
} else {
    Write-Host "Error en el impacto de la Versión 2. Revise los logs." -ForegroundColor Red
}
