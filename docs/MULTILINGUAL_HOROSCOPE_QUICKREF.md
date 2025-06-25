# Multilingual Horoscopes: Quick Reference Guide

This guide provides a quick reference for working with the multilingual horoscope system.

## Key Features

- **Automated Translation**: Horoscopes are automatically translated from Ukrainian to English, German, and Russian
- **Integration with Core Generation**: Translations happen during the horoscope generation process
- **Database Storage**: All translations are stored in dedicated language-specific fields
- **Configurable System**: Can be easily enabled/disabled via environment variables

## Commands

### Run Horoscope Generator with Translations Only

**Windows**:
```
run_horoscope_with_translations.bat
```

**Linux/Mac**:
```
./run_horoscope_with_translations.sh
```

### Run with Full Features (Translations + DALL-E)

**Windows**:
```
run_horoscope_full.bat
```

**Linux/Mac**:
```
./run_horoscope_full.sh
```

## Key Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `USE_TRANSLATIONS` | Enable/disable translation system | `true` |
| `OPENAI_API_KEY` | OpenAI API authentication | (required) |
| `OPENAI_TRANSLATION_ASSISTANT_ID` | ID for translation assistant | (required) |

## Database Fields

For each translated content type, the following fields exist:

| Content Type | Fields |
|--------------|--------|
| Title | `title_ua`, `title_en`, `title_de`, `title_ru` |
| Content | `content_ua`, `content_en`, `content_de`, `content_ru` |
| Summary | `summary_ua`, `summary_en`, `summary_de`, `summary_ru` |

## Troubleshooting

### Common Issues

1. **No translations appearing**
   - Check `USE_TRANSLATIONS=true` in `.env` or environment
   - Verify `OPENAI_TRANSLATION_ASSISTANT_ID` is set correctly
   - Ensure OpenAI API key is valid

2. **Incomplete translations**
   - Check logs for errors or timeouts
   - Verify content size isn't too large

3. **Translation quality issues**
   - Review OpenAI Assistant instructions
   - Consider refining prompts for specific terminology

## Integration with Frontend

When displaying content, use the appropriate language field based on user preferences:

```python
# Example pseudocode
def get_horoscope_content(blog_block, user_language):
    # Default to Ukrainian if translation not available
    content_field = f"content_{user_language}" if hasattr(blog_block, f"content_{user_language}") else "content_ua"
    return getattr(blog_block, content_field)
```

## Further Documentation

- [HOROSCOPE_TRANSLATION_GUIDE.md](docs/HOROSCOPE_TRANSLATION_GUIDE.md) - Comprehensive Ukrainian guide
- [HOROSCOPE_TRANSLATION_GUIDE_EN.md](docs/HOROSCOPE_TRANSLATION_GUIDE_EN.md) - Comprehensive English guide
- [translator_README.md](translator_README.md) - Technical documentation for the translator module
