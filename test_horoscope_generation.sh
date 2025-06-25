#!/bin/bash

# Shell script to test horoscope content generation

echo "Testing horoscope content generation..."

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated"
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
else
    echo "No virtual environment found"
fi

# Run the test script
echo "Running horoscope generation test..."
python test_horoscope_generation.py

if [ $? -eq 0 ]; then
    echo "Horoscope generation test completed successfully!"
else
    echo "Horoscope generation test failed with exit code: $?"
fi

# If using virtual environment, deactivate it
if type deactivate >/dev/null 2>&1; then
    deactivate
    echo "Virtual environment deactivated"
fi

echo "Press Enter to exit..."
read
