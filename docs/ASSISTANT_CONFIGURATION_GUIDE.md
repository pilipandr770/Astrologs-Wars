# Astrology Assistant Configuration Guide

This document explains how to configure OpenAI assistants for the daily horoscope generator.

## Required Environment Variables

The daily horoscope generator uses OpenAI assistants to generate content for each astrology system. Each system position requires a specific assistant ID to be set as an environment variable.

### Primary Environment Variables

| Position | System | Primary Environment Variable |
|----------|--------|------------------------------|
| 1 | Західна астрологія (Western) | `EUROPEAN_ASTROLOGY_ASSISTANT_ID` |
| 2 | Китайська астрологія (Chinese) | `CHINESE_ASTROLOGY_ASSISTANT_ID` |
| 3 | Ведична астрологія (Vedic) | `INDIAN_ASTROLOGY_ASSISTANT_ID` |
| 4 | Нумерологія (Numerology) | `NUMEROLOGY_ASSISTANT_ID` |
| 5 | Таро (Tarot) | `TAROT_ASSISTANT_ID` |
| 6 | Кармічна астрологія (Karmic) | `KARMIC_ASTROLOGY_ASSISTANT_ID` |
| 7 | Езотерична астрологія (Esoteric) | `ESOTERIC_ASTROLOGY_ASSISTANT_ID` |
| 8 | Світла прогностика (Predictive) | `PREDICTIVE_ASTROLOGY_ASSISTANT_ID` |

### Alternative Environment Variables (Fallbacks)

If the primary environment variables are not set, the system will look for these fallback variables:

| Position | Fallback Environment Variables |
|----------|-------------------------------|
| 1 | `WESTERN_ASTROLOGY_ASSISTANT_ID` |
| 6 | `LAL_KITAB_ASSISTANT_ID` |
| 7 | `JYOTISH_ASSISTANT_ID` |
| 8 | `PLANETARY_ASTROLOGY_ASSISTANT_ID`, `LIGHT_ASTROLOGY_ASSISTANT_ID`, `ASTROLOGY_FORECASTING_ASSISTANT_ID`, `FORECASTING_ASSISTANT_ID` |

## Setting Up Environment Variables

### For Local Development

Create or update your `.env` file with these variables:

```
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# OpenAI Assistant IDs
EUROPEAN_ASTROLOGY_ASSISTANT_ID=asst_123...
CHINESE_ASTROLOGY_ASSISTANT_ID=asst_123...
INDIAN_ASTROLOGY_ASSISTANT_ID=asst_123...
NUMEROLOGY_ASSISTANT_ID=asst_123...
TAROT_ASSISTANT_ID=asst_123...
KARMIC_ASTROLOGY_ASSISTANT_ID=asst_123...
ESOTERIC_ASTROLOGY_ASSISTANT_ID=asst_123...
PREDICTIVE_ASTROLOGY_ASSISTANT_ID=asst_123...
```

### For Production (Render.yaml)

Add or update these environment variables in your `render.yaml` file:

```yaml
services:
  - type: web
    # ...other configurations...
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: EUROPEAN_ASTROLOGY_ASSISTANT_ID
        value: "asst_123..."
      - key: CHINESE_ASTROLOGY_ASSISTANT_ID
        value: "asst_123..."
      - key: INDIAN_ASTROLOGY_ASSISTANT_ID
        value: "asst_123..."
      - key: NUMEROLOGY_ASSISTANT_ID
        value: "asst_123..."
      - key: TAROT_ASSISTANT_ID
        value: "asst_123..."
      - key: KARMIC_ASTROLOGY_ASSISTANT_ID
        value: "asst_123..."
      - key: ESOTERIC_ASTROLOGY_ASSISTANT_ID
        value: "asst_123..."
      - key: PREDICTIVE_ASTROLOGY_ASSISTANT_ID
        value: "asst_123..."
```

## Troubleshooting

If a horoscope block is not being generated with custom content:

1. Check that the corresponding environment variable is set
2. Verify that the assistant ID is valid and the assistant exists in your OpenAI account
3. Run the `test_horoscope_generation.py` script to test specific assistant IDs
4. Check the logs for any errors related to assistant ID lookup or API calls

### Common Issues

- **First block (position 1) not generated**: Ensure `EUROPEAN_ASTROLOGY_ASSISTANT_ID` or `WESTERN_ASTROLOGY_ASSISTANT_ID` is set
- **Last block (position 8) not generated**: Ensure `PREDICTIVE_ASTROLOGY_ASSISTANT_ID`, `PLANETARY_ASTROLOGY_ASSISTANT_ID`, or `LIGHT_ASTROLOGY_ASSISTANT_ID` is set
