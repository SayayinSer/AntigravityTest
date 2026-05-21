
$localSkills = "d:\aaProyectos\Entorno04\.agents\skills"
$globalSkills = "$env:USERPROFILE\.gemini\config\skills"
$mcpConfig = "$env:USERPROFILE\.gemini\config\mcp_config.json"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupRoot = "d:\aaProyectos\Entorno04\Backups\Skills_Backup_$timestamp"

Write-Host "Iniciando nivelacin de Skills (Local <-> Global)..." -ForegroundColor Cyan

# 1. Crear carpeta de Backup
if (-not (Test-Path $backupRoot)) {
    New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
}

# 2. Backup de Local antes de sincronizar
Write-Host "Realizando Backup de Skills Locales..." -ForegroundColor Gray
robocopy $localSkills (Join-Path $backupRoot "Local") /E /NFL /NDL /NJH /NJS /R:0 /W:0

# 3. Backup de Global antes de sincronizar
Write-Host "Realizando Backup de Skills Globales..." -ForegroundColor Gray
robocopy $globalSkills (Join-Path $backupRoot "Global") /E /NFL /NDL /NJH /NJS /R:0 /W:0

# 4. Backup de Conexiones MCP
Write-Host "Realizando Backup de Conexiones MCP..." -ForegroundColor Gray
if (Test-Path $mcpConfig) {
    Copy-Item $mcpConfig (Join-Path $backupRoot "mcp_config.json") -Force
}

# 4. Sincronizar: Local -> Global (Copiar nuevas y actualizadas)
Write-Host "Sincronizando Local -> Global..." -ForegroundColor Yellow
robocopy $localSkills $globalSkills /E /XO /NFL /NDL /NJH /NJS /R:0 /W:0

# 5. Sincronizar: Global -> Local (Copiar nuevas y actualizadas)
Write-Host "Sincronizando Global -> Local..." -ForegroundColor Yellow
robocopy $globalSkills $localSkills /E /XO /NFL /NDL /NJH /NJS /R:0 /W:0

Write-Host "Nivelacin completada exitosamente." -ForegroundColor Green
Write-Host "Backup disponible en: $backupRoot" -ForegroundColor Cyan
