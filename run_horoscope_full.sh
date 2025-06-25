#!/bin/bash
echo "Running horoscope generator with DALL-E images and translations..."

# Set environment variables
export USE_DALLE_IMAGES=true
export USE_TRANSLATIONS=true

# Run the horoscope generator
python daily_horoscope_replace.py

echo "Done!"
read -p "Press Enter to exit..."
