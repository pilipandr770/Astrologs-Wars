#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script fixes any remaining issues with the footer CSS.
"""

import os
import re
import sys

def fix_remaining_css_issues():
    """Fix any remaining CSS issues with position: fixed."""
    style_css_path = os.path.join('app', 'static', 'css', 'style.css')
    
    with open(style_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for any other instances of position: fixed related to the footer
    # We'll use regex pattern to find and replace any remaining position: fixed for the footer
    pattern = r'(footer[^\{]*\{[^\}]*?)position:\s*fixed;'
    updated_content = re.sub(pattern, r'\1position: relative;', content)
    
    with open(style_css_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("All remaining position: fixed instances for footer have been replaced.")

if __name__ == "__main__":
    fix_remaining_css_issues()
    print("Footer CSS fixes completed successfully.")
