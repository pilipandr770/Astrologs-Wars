Write-Host "Running horoscope generator with DALL-E image generation..." -ForegroundColor Green

# Set environment variables
$env:USE_DALLE_IMAGES="true"

# Run the horoscope generator
python daily_horoscope_replace.py

Write-Host "Done!" -ForegroundColor Green
Read-Host -Prompt "Press Enter to exit"
