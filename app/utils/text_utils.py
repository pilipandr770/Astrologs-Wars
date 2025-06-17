"""
Utility functions for text processing
"""
import re
from html import unescape

def strip_html_tags(text):
    """
    Removes HTML tags from text and returns clean text
    Also handles HTML entities like &nbsp;
    """
    if not text:
        return ""
        
    # First unescape any HTML entities
    text = unescape(text)
    
    # Then remove HTML tags
    clean_text = re.sub(r'<.*?>', '', text)
    
    # Clean up extra whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    return clean_text
