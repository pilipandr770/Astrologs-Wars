#!/bin/bash
echo "Running horoscope generator with DALL-E images, translations, and OpenAI assistant content generation..."

# Set environment variables
export USE_DALLE_IMAGES=true
export USE_TRANSLATIONS=true

# Check for required environment variables
if [ -z "$OPENAI_API_KEY" ]; then
  echo "WARNING: OPENAI_API_KEY is not set. API features may not work correctly."
fi

# Check for astrology assistant IDs
ASSISTANT_COUNT=0
for VAR_NAME in EUROPEAN_ASTROLOGY_ASSISTANT_ID CHINESE_ASTROLOGY_ASSISTANT_ID INDIAN_ASTROLOGY_ASSISTANT_ID LAL_KITAB_ASSISTANT_ID JYOTISH_ASSISTANT_ID NUMEROLOGY_ASSISTANT_ID TAROT_ASSISTANT_ID PLANETARY_ASTROLOGY_ASSISTANT_ID; do
  if [ -n "${!VAR_NAME}" ]; then
    ASSISTANT_COUNT=$((ASSISTANT_COUNT + 1))
  fi
done

echo "Found $ASSISTANT_COUNT configured astrology assistants"
if [ "$ASSISTANT_COUNT" -eq 0 ]; then
  echo "WARNING: No astrology assistant IDs are configured. Will use fallback template content."
fi

# Run the horoscope generator
echo "Starting horoscope generation process..."
python daily_horoscope_replace.py

echo "Done!"
read -p "Press Enter to exit..."
