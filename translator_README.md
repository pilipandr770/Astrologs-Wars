# Horoscope Translation Module

This module enables automatic translation of horoscope content into multiple languages using the OpenAI Assistant API.

## Overview

The `translator.py` module provides the `HoroscopeTranslator` class for translating horoscope content into various languages. It uses OpenAI's Assistant API to ensure high-quality, context-aware translations that maintain astrological terminology correctly.

## Features

- Translates content to English, German, and Russian
- Preserves formatting and HTML tags in the translated text
- Handles API communication with error handling and retries
- Waits for asynchronous translation to complete
- Can be toggled on/off via environment variables

## Requirements

- Python 3.7+
- OpenAI Python SDK (`openai`)
- OpenAI API key
- OpenAI Translation Assistant ID

## Installation

1. Ensure the OpenAI package is installed:
```
pip install openai
```

2. Set up the required environment variables:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_TRANSLATION_ASSISTANT_ID=your_assistant_id_here
```

## Usage

### Basic Usage

```python
from translator import HoroscopeTranslator

# Initialize translator
translator = HoroscopeTranslator()

# Check if service is available
if translator.is_available():
    # Translate content to English
    result = translator.translate_content("Ваш гороскоп на сьогодні...", "en")
    
    if result["success"]:
        translated_text = result["content"]
        print(translated_text)
    else:
        print(f"Translation error: {result.get('error')}")
```

### Integration with Horoscope Generation

The translator is designed to be integrated with the horoscope generation process:

```python
# In your horoscope generation script
from translator import HoroscopeTranslator

# Check if translations are enabled
use_translations = bool(os.getenv('USE_TRANSLATIONS', 'true').lower() == 'true')

if use_translations:
    translator = HoroscopeTranslator()
    
    if translator.is_available():
        # Translate to supported languages
        for lang_code in ['en', 'de', 'ru']:
            # Translate and update database fields
            result = translator.translate_content(content, lang_code)
            if result["success"]:
                # Update database field for this language
                horoscope_entry[f"content_{lang_code}"] = result["content"]
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_TRANSLATION_ASSISTANT_ID`: ID of your OpenAI Translation Assistant
- `USE_TRANSLATIONS`: Enable/disable translations (default: "true")

## Creating a Translation Assistant

1. Go to [OpenAI Platform](https://platform.openai.com/assistants)
2. Create a new assistant with GPT-4 or newer
3. Set instructions for astrological content translation
4. Save the assistant ID and add to your environment variables

## Error Handling

The translator handles several error conditions:

- Invalid input (empty content or unsupported language)
- Unavailable translation service (missing API key or assistant ID)
- API errors (connection issues, rate limits)
- Timeout or completion failure

Each error is logged and returned with a descriptive message.

## Future Improvements

Potential enhancements for this module:

1. Support for more languages
2. Batch translation for efficiency
3. Caching of frequently used translations
4. Custom terminology dictionary for consistent translations
5. Quality validation of translations

## See Also

- [HOROSCOPE_TRANSLATION_GUIDE.md](../docs/HOROSCOPE_TRANSLATION_GUIDE.md) - Comprehensive guide in Ukrainian
- [HOROSCOPE_TRANSLATION_GUIDE_EN.md](../docs/HOROSCOPE_TRANSLATION_GUIDE_EN.md) - English translation guide
