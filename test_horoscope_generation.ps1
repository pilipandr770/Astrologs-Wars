# PowerShell script to test horoscope content generation

Write-Host "Testing horoscope content generation..." -ForegroundColor Green

# Activate virtual environment if it exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated" -ForegroundColor Green
} elseif (Test-Path "venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "No virtual environment found" -ForegroundColor Yellow
}

# Run the test script
try {
    Write-Host "Running horoscope generation test..."
    python test_horoscope_generation.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Horoscope generation test completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Horoscope generation test failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    }
}
catch {
    Write-Host "Error running horoscope generation test: $_" -ForegroundColor Red
}

# If using virtual environment, deactivate it
if (Test-Path -Path Function:deactivate) {
    deactivate
    Write-Host "Virtual environment deactivated" -ForegroundColor Green
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
