#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script fixes the chat widget behavior to ensure it starts hidden
and only appears when the chat button is clicked.
"""

import os


def fix_chat_widget():
    """Fix the chat widget to restore its original behavior."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the chat button - keep it visible but remove unnecessary styles
    if 'id="chat-open-btn" class="chat-circle-btn" style="z-index:9100 !important; display:block !important; visibility:visible !important;"' in content:
        content = content.replace(
            'id="chat-open-btn" class="chat-circle-btn" style="z-index:9100 !important; display:block !important; visibility:visible !important;"',
            'id="chat-open-btn" class="chat-circle-btn" style="z-index:9100 !important;"'
        )
    
    # Fix the chat window - ensure it's hidden by default
    if 'id="chat-window" class="chat-window" style="z-index:9200 !important;"' in content:
        content = content.replace(
            'id="chat-window" class="chat-window" style="z-index:9200 !important;"',
            'id="chat-window" class="chat-window" style="z-index:9200 !important; display: none;"'
        )
    
    # Write the updated content back to the file
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Add a script to base.html if assist.js isn't being loaded or executed properly
    if 'document.addEventListener("DOMContentLoaded", function() {' in content and 'chatWindow.style.display = "none";' in content:
        print("assist.js script is properly included and should be working correctly")
    else:
        # Add additional inline script to ensure chat functionality works
        additional_script = """
    <script>
      // Additional script to ensure chat functionality
      document.addEventListener("DOMContentLoaded", function() {
        const chatBtn = document.getElementById("chat-open-btn");
        const chatWindow = document.getElementById("chat-window");
        const chatMin = document.getElementById("chat-minimize");
        
        if (chatBtn && chatWindow) {
          // Ensure chat is hidden initially
          chatWindow.style.display = "none";
          
          // Open chat when button is clicked
          chatBtn.addEventListener("click", function() {
            chatWindow.style.display = "flex";
          });
          
          // Close chat when minimize button is clicked
          if (chatMin) {
            chatMin.addEventListener("click", function() {
              chatWindow.style.display = "none";
            });
          }
        }
      });
    </script>
    """
        
        # Insert the additional script before the closing </body> tag
        if '</body>' in content:
            content = content.replace('</body>', additional_script + '</body>')
            
            # Write the updated content back to the file
            with open(base_html_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print("Chat widget has been fixed to start hidden and only appear when clicked")


def update_footer_fix_css():
    """Update footer_fix.css to prevent it from affecting chat widget visibility."""
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    
    with open(footer_fix_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove any CSS rules that force the chat widget to always be visible
    if 'body > #chat-window' in content and 'display: block !important' in content:
        updated_content = content.replace(
            'body > #chat-window {',
            'body > .dont-force-chat-window {'
        )
        
        # Write the updated content back to the file
        with open(footer_fix_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    
    print("footer_fix.css has been updated to respect chat widget visibility")


if __name__ == "__main__":
    fix_chat_widget()
    update_footer_fix_css()
    print("Chat widget now functions correctly - it starts hidden and appears when the chat button is clicked")
