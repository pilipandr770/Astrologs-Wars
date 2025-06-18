# PowerShell script for updating horoscope blocks styling

Write-Host "=== Updating Horoscope Blocks Styling ===" -ForegroundColor Cyan

python update_horoscope_blocks_visual.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Success! ===" -ForegroundColor Green
    Write-Host "Restart your application to see the changes."
    Write-Host "You can use .\run_astro_site.ps1 to restart."
} else {
    Write-Host ""
    Write-Host "=== Error occurred ===" -ForegroundColor Red
    Write-Host "Please check the output above for details."
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
