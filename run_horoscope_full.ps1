Write-Host "Running horoscope generator with DALL-E images and translations..." -ForegroundColor Green

# Set environment variables
$env:USE_DALLE_IMAGES = "true"
$env:USE_TRANSLATIONS = "true"

# Run the horoscope generator
python daily_horoscope_replace.py

Write-Host "Done." -ForegroundColor Green
Read-Host -Prompt "Press Enter to exit"
