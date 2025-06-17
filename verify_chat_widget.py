#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script verifies that the chat widget behavior has been properly fixed.
"""

import os
import re
import sys


def check_chat_widget():
    """Check if the chat widget has been properly fixed."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check that the chat button is visible
    if ('id="chat-open-btn"' in content and 
        'style="z-index:9100 !important;"' in content):
        print("✓ Chat button is properly visible")
    else:
        print("ERROR: Chat button might not be properly visible")
        return False
    
    # Check that the chat window is hidden by default
    if ('id="chat-window"' in content and 
        'style="z-index:9200 !important; display: none;"' in content):
        print("✓ Chat window is hidden by default")
    else:
        print("ERROR: Chat window might not be hidden by default")
        return False
    
    # Check that the JavaScript for toggling the chat is included
    if 'const chatBtn = document.getElementById("chat-open-btn");' in content:
        print("✓ Chat toggle JavaScript is included")
    else:
        print("ERROR: Chat toggle JavaScript might be missing")
        return False
    
    return True


def check_footer_fix_css():
    """Check if the footer_fix.css has been updated to not force chat window visibility."""
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    
    with open(footer_fix_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if CSS rules that force visibility have been removed or disabled
    if 'body > #chat-window' not in content or 'display: block !important' not in content:
        print("✓ footer_fix.css no longer forces chat window visibility")
        return True
    else:
        print("ERROR: footer_fix.css might still be forcing chat window visibility")
        return False


if __name__ == "__main__":
    print("Verifying chat widget fix...")
    
    chat_widget_ok = check_chat_widget()
    footer_css_ok = check_footer_fix_css()
    
    if chat_widget_ok and footer_css_ok:
        print("\nSUCCESS: Chat widget has been properly fixed!")
        print("The chat button should be visible, while the chat window should be hidden by default.")
        sys.exit(0)
    else:
        print("\nWARNING: There might be issues with the chat widget fix.")
        print("Review the errors above and make necessary adjustments.")
        sys.exit(1)
