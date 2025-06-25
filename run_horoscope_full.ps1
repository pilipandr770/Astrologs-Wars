Write-Host "Running horoscope generator with DALL-E images, translations, and OpenAI assistant content generation..." -ForegroundColor Green

# Set environment variables
$env:USE_DALLE_IMAGES = "true"
$env:USE_TRANSLATIONS = "true"

# Check for required environment variables
if ([string]::IsNullOrEmpty($env:OPENAI_API_KEY)) {
    Write-Host "WARNING: OPENAI_API_KEY is not set. API features may not work correctly." -ForegroundColor Yellow
}

# Check for astrology assistant IDs
$assistantVars = @(
    "EUROPEAN_ASTROLOGY_ASSISTANT_ID",
    "CHINESE_ASTROLOGY_ASSISTANT_ID",
    "INDIAN_ASTROLOGY_ASSISTANT_ID",
    "LAL_KITAB_ASSISTANT_ID",
    "JYOTISH_ASSISTANT_ID",
    "NUMEROLOGY_ASSISTANT_ID",
    "TAROT_ASSISTANT_ID",
    "PLANETARY_ASTROLOGY_ASSISTANT_ID"
)

$assistantCount = 0
foreach ($var in $assistantVars) {
    if (![string]::IsNullOrEmpty((Get-Item env:$var -ErrorAction SilentlyContinue).Value)) {
        $assistantCount++
    }
}

Write-Host "Found $assistantCount configured astrology assistants" -ForegroundColor Cyan
if ($assistantCount -eq 0) {
    Write-Host "WARNING: No astrology assistant IDs are configured. Will use fallback template content." -ForegroundColor Yellow
}

# Run the horoscope generator
Write-Host "Starting horoscope generation process..." -ForegroundColor Green
python daily_horoscope_replace.py

Write-Host "Done." -ForegroundColor Green
Read-Host -Prompt "Press Enter to exit"
