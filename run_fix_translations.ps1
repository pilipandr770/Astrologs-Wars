Write-Host "Starting translation fix script..." -ForegroundColor Cyan
python fix_translations.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "Translation fix completed successfully!" -ForegroundColor Green
} else {
    Write-Host "Translation fix failed with error code $LASTEXITCODE" -ForegroundColor Red
}
Read-Host -Prompt "Press Enter to continue..."
