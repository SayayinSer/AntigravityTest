$date = Get-Date -Format "yyyyMMdd_HHmm"
$backupDir = "d:\aaProyectos\Entorno01\backups\skills_backup_$date"

Write-Host "Iniciando backup en: $backupDir"

if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force
}

Write-Host "Copiando skills locales..."
Copy-Item -Path "d:\aaProyectos\Entorno01\.agents\skills" -Destination $backupDir -Recurse -Force

Write-Host "Copiando skills globales..."
$globalSkills = "$env:USERPROFILE\.gemini\antigravity\skills"
Copy-Item -Path $globalSkills -Destination $backupDir -Recurse -Force

Write-Host "Backup completado con éxito."
