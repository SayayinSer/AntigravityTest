$ErrorActionPreference = "Stop"

$phpUrl = "https://windows.php.net/downloads/releases/archives/php-8.2.10-nts-Win32-vs16-x64.zip"
$zipPath = "$PSScriptRoot\php.zip"
$extractPath = "$PSScriptRoot\php_bin"

Write-Host "Descargando PHP 8.2 Portable..."
Invoke-WebRequest -Uri $phpUrl -OutFile $zipPath

Write-Host "Extrayendo PHP..."
if (Test-Path $extractPath) {
    Remove-Item -Path $extractPath -Recurse -Force
}
Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force

Write-Host "Configurando php.ini..."
Copy-Item -Path "$extractPath\php.ini-development" -Destination "$extractPath\php.ini"

$iniPath = "$extractPath\php.ini"
(Get-Content $iniPath) -replace '^;extension_dir = "ext"', 'extension_dir = "ext"' | Set-Content $iniPath
(Get-Content $iniPath) -replace '^;extension=pdo_mysql', 'extension=pdo_mysql' | Set-Content $iniPath
(Get-Content $iniPath) -replace '^;extension=mbstring', 'extension=mbstring' | Set-Content $iniPath
(Get-Content $iniPath) -replace '^;extension=openssl', 'extension=openssl' | Set-Content $iniPath

Remove-Item -Path $zipPath -Force

Write-Host "PHP Instalado en $extractPath"
