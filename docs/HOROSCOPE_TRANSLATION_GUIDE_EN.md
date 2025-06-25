# Multilingual Horoscopes: Automatic Translation System

**Last Updated:** June 25, 2025

## Introduction

This document describes the automatic translation system for horoscopes into various languages using OpenAI Translation Assistant. The system is integrated into the main horoscope generation script and allows for automatic translation of content into English, German, and Russian.

## Functionality Overview

The horoscope translation system includes the following key components:

1. **`HoroscopeTranslator` Class** (in the `translator.py` file)
   - Uses the OpenAI API for content translation
   - Supports translation into English, German, and Russian
   - Features a waiting mechanism and error handling

2. **Integration with the Main Horoscope Generation Script**
   - Automatically translates the title, content, and summary of horoscopes
   - Populates corresponding fields in the database (`title_XX`, `content_XX`, `summary_XX`)
   - Controlled via the `USE_TRANSLATIONS` environment variable

3. **Flexible Translation Management**
   - Activation/deactivation through the .env file or environment variables
   - Option to run with or without translations
   - Configurable in the Render configuration for production

## Technical Details

### Database Model

The `BlogBlock` model contains fields for storing multilingual content:
- `title_ua`, `title_en`, `title_de`, `title_ru` - titles in different languages
- `content_ua`, `content_en`, `content_de`, `content_ru` - content in different languages
- `summary_ua`, `summary_en`, `summary_de`, `summary_ru` - summaries in different languages

### Translation Process

1. Generation of core content in Ukrainian
2. Checking the availability of the translator and the presence of the `USE_TRANSLATIONS` setting
3. Sequential translation into each supported language:
   - Translation of title, content, and summary
   - Populating corresponding fields in the database
   - Logging translation results

### Setup and Management

#### Activating/Deactivating Translations

In the `.env` file:
```
USE_TRANSLATIONS=true  # Use automatic translation for horoscopes
```

In `render.yaml` (for production):
```yaml
envVars:
  - key: USE_TRANSLATIONS
    value: "true"
```

## Running and Usage

### Running with Translations

To run with translations only:
```
run_horoscope_with_translations.bat (Windows)
./run_horoscope_with_translations.sh (Linux/Mac)
```

### Running with Translations and DALL-E Images

For a full run with all features:
```
run_horoscope_full.bat (Windows)
./run_horoscope_full.sh (Linux/Mac)
```

## Troubleshooting

### Common Issues

1. **No Translation Occurring**
   - Check the `USE_TRANSLATIONS=true` setting
   - Ensure that `OPENAI_TRANSLATION_ASSISTANT_ID` is set
   - Verify the validity of the API key

2. **Translation Errors**
   - Check the logs for error messages
   - Make sure the OpenAI API is working correctly
   - Check the size of the content being translated (too large texts may cause errors)

3. **Website Display Issues**
   - Make sure the frontend is correctly selecting the content language
   - Verify that appropriate templates exist for different languages

## Usage Recommendations

1. **Cost Optimization**
   - Set `USE_TRANSLATIONS=false` during testing and development
   - Consider using translations only for specific horoscope types

2. **Translation Quality**
   - Regularly check the quality of translations
   - Adjust prompts if specific terminology requires improvement

## Future Enhancements

Potential improvements to the translation system:

1. **Additional Language Support**
   - Add support for more languages as needed (Spanish, French, Italian, etc.)
   - Implement language-specific customization options

2. **Quality Improvements**
   - Implement post-translation quality checks
   - Add domain-specific terminology to improve astrology translations

3. **Performance Optimization**
   - Implement batch translations for better efficiency
   - Add caching for frequently used translations

## API Reference

### HoroscopeTranslator Class

The main class for handling translations:

```python
translator = HoroscopeTranslator()
result = translator.translate_content(text, target_language)
```

#### Environment Variables Required:

- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_TRANSLATION_ASSISTANT_ID` - ID of your translation assistant

## Conclusion

The automatic translation system allows the astrology site to offer content in multiple languages with minimal manual effort. By leveraging the OpenAI Translation Assistant, high-quality translations are generated that maintain the nuance and specific terminology of astrological content.
