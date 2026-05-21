param(
    [Parameter(Mandatory=$false)]
    [string]$XpzPath,
    [Parameter(Mandatory=$false)]
    [string]$OutputPath,
    [Parameter(Mandatory=$false)]
    [switch]$FullSnapshot,
    [Parameter(Mandatory=$false)]
    [string]$KbMetadataPath
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$enginePath = Join-Path $scriptDir "..\scripts-xpz\Sync-GeneXusXpzToXml.ps1"

Write-Host "--- Wrapper: Sync-GeneXusXpzToXml ---" -ForegroundColor Gray
& $enginePath @PSBoundParameters
