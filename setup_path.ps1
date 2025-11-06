# Gmail to NotebookLM - PATH Setup Script
# This script adds the Python Scripts directory to your PATH

$scriptsPath = "C:\Users\paul\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"

Write-Host "Gmail to NotebookLM - PATH Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if directory exists
if (-not (Test-Path $scriptsPath)) {
    Write-Host "Error: Scripts directory not found at:" -ForegroundColor Red
    Write-Host $scriptsPath -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run 'pip install -e .' first" -ForegroundColor Yellow
    exit 1
}

# Get current user PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Check if already in PATH
if ($currentPath -like "*$scriptsPath*") {
    Write-Host "Scripts directory is already in your PATH!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "Adding Scripts directory to your PATH..." -ForegroundColor Yellow

    # Add to PATH
    $newPath = $currentPath + ";" + $scriptsPath
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")

    Write-Host "Successfully added to PATH!" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: You need to restart your terminal/PowerShell for changes to take effect." -ForegroundColor Yellow
    Write-Host ""
}

# Show available commands
Write-Host "Available Commands:" -ForegroundColor Cyan
Write-Host "-------------------" -ForegroundColor Cyan
Write-Host ""
Write-Host "CLI (Full):" -ForegroundColor Green
Write-Host "  gmail-to-notebooklm --label Work --output-dir ./exports" -ForegroundColor White
Write-Host ""
Write-Host "CLI (Short):" -ForegroundColor Green
Write-Host "  g2n --label Work --output-dir ./exports" -ForegroundColor White
Write-Host ""
Write-Host "GUI (Full):" -ForegroundColor Green
Write-Host "  gmail-to-notebooklm-gui" -ForegroundColor White
Write-Host ""
Write-Host "GUI (Short):" -ForegroundColor Green
Write-Host "  g2n-gui" -ForegroundColor White
Write-Host ""

# Test if commands work
Write-Host "Testing commands..." -ForegroundColor Yellow
Write-Host ""

try {
    & "$scriptsPath\g2n.exe" --version 2>$null
    Write-Host "✓ CLI commands are working!" -ForegroundColor Green
} catch {
    Write-Host "✗ CLI commands not yet available (restart terminal)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Restart your terminal/PowerShell" -ForegroundColor White
Write-Host "2. Run 'g2n-gui' to launch the desktop application" -ForegroundColor White
Write-Host "3. Or run 'g2n --help' for CLI usage" -ForegroundColor White
Write-Host ""
