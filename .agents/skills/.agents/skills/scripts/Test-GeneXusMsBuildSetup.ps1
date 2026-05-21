# --- Wrapper: Test-GeneXusMsBuildSetup.ps1 ---
# This is a wrapper for the engine script in scripts-xpz/
# Aligned with the methodology defined in README.md

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$enginePath = Join-Path $scriptDir "..\scripts-xpz\Test-GeneXusMsBuildSetup.ps1"

if (-not (Test-Path $enginePath)) {
    Write-Error "Engine script not found: $enginePath"
    exit 1
}

& $enginePath @PSBoundParameters
