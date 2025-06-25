#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script verifies that the footer fixes have been correctly applied
to ensure the footer is visible on all pages.
"""

import os
import re
import sys

def check_base_html():
    """Check if the base.html file has been updated correctly."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the footer style has been changed from fixed to relative
    if 'position:fixed' in content and 'id="site-footer"' in content:
        print("ERROR: Footer still has position:fixed in base.html!")
        return False
    
    # Check if position:relative is set for the footer
    if 'position:relative' in content and 'id="site-footer"' in content:
        print("✓ Footer position has been changed to relative in base.html")
    else:
        print("ERROR: Footer does not have position:relative in base.html!")
        return False
    
    # Check if main padding was added
    if 'main style="padding-bottom: 80px; min-height: calc(100vh - 180px);"' in content:
        print("✓ Main element has proper padding in base.html")
    else:
        print("ERROR: Main element does not have proper padding in base.html!")
        return False
    
    # Check if the footer-fix.css is included
    if 'footer_fix.css' in content:
        print("✓ footer_fix.css is linked in base.html")
    else:
        print("ERROR: footer_fix.css is not linked in base.html!")
        return False
    
    return True

def check_css():
    """Check if the CSS files have been updated correctly."""
    style_css_path = os.path.join('app', 'static', 'css', 'style.css')
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    
    # Check if style.css has been updated
    with open(style_css_path, 'r', encoding='utf-8') as f:
        style_content = f.read()
    
    # Extract the footer#site-footer style block
    footer_pattern = r'footer#site-footer\s*\{[^}]*\}'
    footer_match = re.search(footer_pattern, style_content)
    
    if footer_match:
        footer_style = footer_match.group(0)
        if 'position: fixed' in footer_style or 'position:fixed' in footer_style:
            print("ERROR: footer still has position: fixed in style.css!")
            return False
        
        if 'position: relative' in footer_style or 'position:relative' in footer_style:
            print("✓ Footer position has been changed to relative in style.css")
        else:
            print("ERROR: Footer does not have position: relative in style.css!")
            return False
    else:
        print("WARNING: Could not find footer#site-footer style block in style.css")
        # Not a fatal error, continue
    
    # Check if footer_fix.css exists and has correct content
    if not os.path.exists(footer_fix_path):
        print("ERROR: footer_fix.css does not exist!")
        return False
    
    with open(footer_fix_path, 'r', encoding='utf-8') as f:
        footer_fix_content = f.read()
    
    required_css_rules = [
        'body {', 
        'display: flex',
        'flex-direction: column',
        'min-height: 100vh',
        'main {',
        'flex: 1',
        'padding-bottom:',
        '#site-footer {',
        'margin-top: auto',
        'position: relative'
    ]
    
    all_rules_found = True
    for rule in required_css_rules:
        if rule not in footer_fix_content:
            print(f"ERROR: Missing CSS rule '{rule}' in footer_fix.css")
            all_rules_found = False
    
    if all_rules_found:
        print("✓ footer_fix.css has all required CSS rules")
    
    return all_rules_found

def check_admin_css_link():
    """Check if the admin CSS link is properly formatted."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for any improperly formatted Jinja2 tags
    if re.search(r'{\s+url_for\(', content):  # Single brace { with url_for
        print("ERROR: There is a malformed Jinja2 template tag in base.html")
        return False
    else:
        print("✓ All Jinja2 template tags are properly formatted")
        return True

if __name__ == "__main__":
    print("Verifying footer fixes...")
    
    base_html_ok = check_base_html()
    css_ok = check_css()
    admin_css_ok = check_admin_css_link()
    
    if base_html_ok and css_ok and admin_css_ok:
        print("\nSUCCESS: All footer fixes have been correctly applied!")
        print("The footer should now be visible on all pages.")
        sys.exit(0)
    else:
        print("\nWARNING: Some footer fixes may not have been applied correctly.")
        print("Review the errors above and make necessary adjustments.")
        sys.exit(1)
