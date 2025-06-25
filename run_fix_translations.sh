#!/bin/bash
echo "Starting translation fix script..."
python3 fix_translations.py
if [ $? -eq 0 ]; then
    echo "Translation fix completed successfully!"
else
    echo "Translation fix failed with error code $?"
fi
read -p "Press any key to continue... " -n 1 -s
