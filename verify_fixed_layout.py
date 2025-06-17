#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script verifies that fixed header and footer are properly set
while ensuring they're visible on all pages.
"""

import os
import re
import sys


def check_base_html():
    """Check if the base.html file has been updated correctly."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the footer style has fixed position
    if 'style="position:fixed;' in content and 'id="site-footer"' in content:
        print("✓ Footer has position:fixed in base.html")
    else:
        print("ERROR: Footer does not have position:fixed in base.html!")
        return False
    
    # Check if main has proper padding 
    if 'main style="padding-top: 70px; padding-bottom: 80px;' in content:
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


def check_css_files():
    """Check if the CSS files have been updated correctly."""
    style_css_path = os.path.join('app', 'static', 'css', 'style.css')
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    blog_css_path = os.path.join('app', 'static', 'css', 'blog_style.css')
    
    # Check style.css
    with open(style_css_path, 'r', encoding='utf-8') as f:
        style_content = f.read()
    
    # Check if header is fixed
    if 'header {' in style_content and 'position: fixed;' in style_content:
        print("✓ Header has position:fixed in style.css")
    else:
        print("ERROR: Header does not have position:fixed in style.css!")
        return False
    
    # Check if footer is fixed
    if 'footer#site-footer {' in style_content and 'position: fixed;' in style_content:
        print("✓ Footer has position:fixed in style.css")
    else:
        print("ERROR: Footer does not have position:fixed in style.css!")
        return False
    
    # Check footer_fix.css
    if os.path.exists(footer_fix_path):
        with open(footer_fix_path, 'r', encoding='utf-8') as f:
            footer_fix_content = f.read()
        
        if '#site-footer {' in footer_fix_content and 'position: fixed;' in footer_fix_content:
            print("✓ Footer has position:fixed in footer_fix.css")
        else:
            print("ERROR: Footer does not have position:fixed in footer_fix.css!")
            return False
            
        if '.blog-section {' in footer_fix_content and 'margin-bottom: 70px;' in footer_fix_content:
            print("✓ Blog section has proper margin in footer_fix.css")
        else:
            print("ERROR: Blog section does not have proper margin in footer_fix.css!")
            return False
    else:
        print("ERROR: footer_fix.css does not exist!")
        return False
    
    # Check blog_style.css
    with open(blog_css_path, 'r', encoding='utf-8') as f:
        blog_css_content = f.read()
    
    if '/* Fix for footer visibility */' in blog_css_content and 'margin-bottom: 70px;' in blog_css_content:
        print("✓ Blog styles have footer visibility fixes")
    else:
        print("ERROR: Blog styles do not have footer visibility fixes!")
        return False
    
    return True


if __name__ == "__main__":
    print("Verifying fixed header and footer setup...")
    
    base_html_ok = check_base_html()
    css_files_ok = check_css_files()
    
    if base_html_ok and css_files_ok:
        print("\nSUCCESS: Fixed header and footer are properly set up!")
        print("The footer should now be visible on all pages.")
        sys.exit(0)
    else:
        print("\nWARNING: Some issues were found with the fixed header and footer setup.")
        print("Review the errors above and make necessary adjustments.")
        sys.exit(1)
