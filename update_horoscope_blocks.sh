#!/bin/bash
# Script for updating horoscope blocks styling (Linux/Mac)

echo "=== Updating Horoscope Blocks Styling ==="
python3 update_horoscope_blocks_visual.py

if [ $? -eq 0 ]; then
    echo
    echo "=== Success! ==="
    echo "Restart your application to see the changes."
    echo "You can use ./run_astro_site.sh to restart."
else
    echo
    echo "=== Error occurred ==="
    echo "Please check the output above for details."
fi
