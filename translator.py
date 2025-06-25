"""
Функции для перевода контента гороскопов с использованием OpenAI Translation Assistant
"""

import os
import time
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class HoroscopeTranslator:
    """
    Класс для перевода гороскопов с использованием OpenAI Translation Assistant
    """
    
    def __init__(self):
        """Initialize the translator with OpenAI API key and assistant ID"""
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.translation_assistant_id = os.environ.get('OPENAI_TRANSLATION_ASSISTANT_ID')
        self.client = OpenAI(api_key=self.api_key)
        
    def is_available(self):
        """Check if translation service is available"""
        return bool(self.api_key and self.translation_assistant_id)
        
    def translate_content(self, content, target_language, max_retries=3):
        """
        Translate content to the specified target language
        
        Args:
            content: Text content to translate
            target_language: Target language code (en, de, ru)
            max_retries: Maximum number of retries
            
        Returns:
            Dictionary with success status and translated content
        """
        # Skip if no content or target language
        if not content or not target_language or target_language.lower() == 'uk':
            return {"success": False, "error": "Invalid content or target language"}
            
        # Skip translation if service is not available
        if not self.is_available():
            logger.warning("Translation service not available - missing API key or assistant ID")
            return {"success": False, "error": "Translation service not available"}
            
        # Prepare the translation prompt
        language_names = {
            'en': 'English',
            'de': 'German',
            'ru': 'Russian',
            'uk': 'Ukrainian'
        }
        
        language_name = language_names.get(target_language.lower(), target_language)
        
        translation_prompt = (
            f"Translate the following horoscope content into {language_name}. "
            f"Maintain the same formatting and structure, but ensure the translation "
            f"sounds natural and fluent in {language_name}. Preserve any HTML formatting.\n\n"
            f"{content}"
        )
        
        try:
            logger.info(f"Translating content to {language_name}")
            
            # Create a thread
            thread = self.client.beta.threads.create()
            
            # Add message to thread
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=translation_prompt
            )
            
            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.translation_assistant_id
            )
            
            # Wait for completion
            return self._wait_for_completion(thread.id, run.id, max_retries)
            
        except Exception as e:
            logger.error(f"Error translating content to {language_name}: {str(e)}")
            return {"success": False, "error": str(e)}
            
    def _wait_for_completion(self, thread_id, run_id, max_retries=5):
        """Wait for OpenAI Assistant run to complete and fetch response"""
        retry_count = 0
        wait_time = 15  # Increased wait time to 15 seconds
        
        while retry_count < max_retries:
            try:
                # Check run status
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run_id
                )
                
                if run.status == "completed":
                    # Get all messages in the thread
                    messages = self.client.beta.threads.messages.list(
                        thread_id=thread_id
                    )
                    
                    # Extract the assistant's response
                    for msg in messages.data:
                        if msg.role == "assistant":
                            # Get the first text content
                            for content_item in msg.content:
                                if content_item.type == "text":
                                    return {"success": True, "content": content_item.text.value}
                                    
                    return {"success": False, "error": "No response content found"}
                
                elif run.status == "failed":
                    error_message = "Unknown error"
                    if hasattr(run, 'last_error') and run.last_error:
                        error_message = run.last_error
                        
                    return {"success": False, "error": f"Run failed: {error_message}"}
                    
                elif run.status in ["cancelled", "expired"]:
                    return {"success": False, "error": f"Run {run.status}"}
                    
                # Still in progress, wait and check again
                logger.info(f"Translation in progress, waiting {wait_time} seconds (retry {retry_count+1}/{max_retries})...")
                time.sleep(wait_time)  # Increased wait time
                
            except Exception as e:
                logger.error(f"Error checking run status: {str(e)}")
                retry_count += 1
                time.sleep(5)  # Short delay before retry
                
        return {"success": False, "error": "Max retries reached waiting for completion"}
