# Integration of Astronomical Data (Ephemeris) in Horoscopes

## Overview

This functionality adds the calculation of precise astronomical planetary positions (ephemeris) and includes this information in prompts for OpenAI Assistants, enabling the generation of more accurate and astronomically correct horoscopes.

## What are Ephemerides?

Ephemerides are tables or data showing the positions of celestial bodies (planets, Moon, Sun, etc.) at specific moments in time. In astrology, this data is used as the basis for interpreting the influence of planets on earthly events and personalities.

## Implemented Functionality

1. **ephemeris.py Module**:
   - Calculation of exact planetary positions using the `ephem` library
   - Determination of zodiac signs for each planet
   - Calculation of moon phases
   - Determination of aspects between planets
   - Generation of reports in text and HTML formats

2. **Integration with Horoscope Generation**:
   - Automatic inclusion of ephemeris in requests to OpenAI Assistant
   - Proper handling of situations when the `ephem` library is unavailable
   - Detailed logs about ephemeris calculations

## How It Works

When the `daily_horoscope_replace.py` script creates a prompt for OpenAI Assistant, it:

1. Checks for the availability of the `ephemeris` module
2. Calculates current planetary positions for the horoscope date
3. Formats a readable ephemeris report
4. Adds this report to the main prompt for the assistant

Example of included data:
```
Astronomical data for 06/25/2023:
=====================================
Sun: Cancer 4.12° (Magnitude: -26.73)
Moon: Leo 22.45° (Magnitude: -12.14)
Mercury: Gemini 28.01° (Magnitude: 0.37)
Venus: Leo 7.33° (Magnitude: -4.41)
Mars: Leo 5.78° (Magnitude: 1.15)
Jupiter: Taurus 15.89° (Magnitude: -2.20)
Saturn: Pisces 7.25° (Magnitude: 0.70)
...

Moon Phase: Waxing Gibbous (94.2%)

Significant Aspects:
----------------------------------------
Sun Conjunction Mars (orb: 1.66°)
Venus Conjunction Mars (orb: 1.55°)
Jupiter Trine Saturn (orb: 8.64°)
```

## Benefits of Using Ephemerides

1. **Accuracy**: Horoscopes are based on real astronomical data
2. **Consistency**: All horoscopes use the same basic data about planetary positions
3. **Detail**: Assistants can interpret specific aspects and positions
4. **Authenticity**: Correspondence to real astronomical data improves the quality of horoscopes

## Testing

To verify ephemeris calculations, use:
```
python test_ephemeris.py
```

Or run the appropriate script:
- Windows: `test_ephemeris.bat`
- Linux/Mac: `test_ephemeris.sh`
- PowerShell: `test_ephemeris.ps1`

## Requirements

- Python 3.6 or newer
- `ephem` library (already included in requirements.txt)
- `pytz` library (for proper timezone handling)

## Notes

- If the `ephem` library is missing, the script will continue to work without ephemeris
- All calculations are performed for UTC time
- By default, the location of Kyiv, Ukraine is used
