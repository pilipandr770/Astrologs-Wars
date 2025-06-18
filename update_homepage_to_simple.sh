#!/bin/bash
# Script for updating the homepage to a simple project info page (Linux/Mac)

echo "=== Updating Homepage to Simple Project Info ==="
python3 update_homepage_to_simple.py

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
