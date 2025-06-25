"""
Test script for verifying the translator functionality.
This script allows testing the HoroscopeTranslator class without running the entire horoscope generation process.
"""

import os
import sys
import logging
from dotenv import load_dotenv
from translator import HoroscopeTranslator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("translator_test.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("TranslatorTest")

# Load environment variables
load_dotenv()

def test_translator():
    """Test the HoroscopeTranslator functionality"""
    logger.info("Starting translator test")
    
    # Check required environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    assistant_id = os.environ.get('OPENAI_TRANSLATION_ASSISTANT_ID')
    
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        return False
        
    if not assistant_id:
        logger.error("OPENAI_TRANSLATION_ASSISTANT_ID not found in environment variables")
        return False
        
    # Initialize translator
    translator = HoroscopeTranslator()
    
    if not translator.is_available():
        logger.error("Translator service not available")
        return False
        
    # Test text in Ukrainian
    test_text = """
    Сьогодні зірки радять вам звернути увагу на свій внутрішній світ. 
    Медитація та глибоке дихання допоможуть відновити баланс. 
    В робочих питаннях очікуйте несподіваних пропозицій.
    """
    
    # Test translation for each supported language
    for lang_code in ['en', 'de', 'ru']:
        logger.info(f"Testing translation to {lang_code}")
        
        result = translator.translate_content(test_text, lang_code)
        
        if result.get('success'):
            translated_text = result.get('content')
            logger.info(f"Translation to {lang_code} successful: {translated_text[:50]}...")
            logger.info(f"Full translated text ({lang_code}):\n{translated_text}")
        else:
            logger.error(f"Translation to {lang_code} failed: {result.get('error')}")
            return False
    
    logger.info("All translation tests completed successfully")
    return True

if __name__ == "__main__":
    success = test_translator()
    if success:
        print("\nTranslator test successful! All languages translated correctly.")
    else:
        print("\nTranslator test failed. Check the logs for details.")
    
    sys.exit(0 if success else 1)
