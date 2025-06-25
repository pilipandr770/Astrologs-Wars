#!/bin/bash
echo "Running horoscope generator with translations..."

# Set environment variables
export USE_TRANSLATIONS=true

# Run the horoscope generator
python daily_horoscope_replace.py

echo "Done!"
read -p "Press Enter to exit..."
