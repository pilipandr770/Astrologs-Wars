#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script verifies that the header and footer are properly fixed
at the top and bottom of all pages.
"""

import os
import re
import sys


def check_base_html():
    """Check if base.html has proper fixed header and footer."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for fixed header styles
    if ('position:fixed' in content and 'header' in content and 'top:0' in content):
        print("✓ Header has fixed positioning in base.html")
    else:
        print("ERROR: Header may not have fixed positioning in base.html")
        return False
    
    # Check for fixed footer styles
    if ('position:fixed' in content and 'id="site-footer"' in content and 'bottom:0' in content):
        print("✓ Footer has fixed positioning in base.html")
    else:
        print("ERROR: Footer may not have fixed positioning in base.html")
        return False
    
    # Check for body padding
    if 'padding-top: 80px; padding-bottom: 80px;' in content:
        print("✓ Body has proper padding to accommodate fixed elements")
    else:
        print("ERROR: Body may not have proper padding for fixed elements")
        return False
    
    return True


def check_css_files():
    """Check if CSS files have proper fixed header and footer styles."""
    style_css_path = os.path.join('app', 'static', 'css', 'style.css')
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    fixed_position_fix_path = os.path.join('app', 'static', 'css', 'fixed_position_fix.css')
    
    all_checks_passed = True
    
    # Check style.css
    with open(style_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'header' in content and 'position: fixed;' in content:
        print("✓ Header has fixed positioning in style.css")
    else:
        print("ERROR: Header may not have fixed positioning in style.css")
        all_checks_passed = False
    
    # Check footer_fix.css
    with open(footer_fix_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'position: fixed !important' in content and '#site-footer' in content:
        print("✓ Footer has fixed positioning in footer_fix.css")
    else:
        print("ERROR: Footer may not have fixed positioning in footer_fix.css")
        all_checks_passed = False
    
    # Check fixed_position_fix.css exists
    if os.path.exists(fixed_position_fix_path):
        print("✓ Cross-browser fixed position CSS file exists")
        
        with open(fixed_position_fix_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'position: fixed !important' in content and 'header' in content and '#site-footer' in content:
            print("✓ Cross-browser fixes include fixed positioning for header and footer")
        else:
            print("ERROR: Cross-browser fixes may not include proper fixed positioning")
            all_checks_passed = False
    else:
        print("ERROR: Cross-browser fixed position CSS file does not exist")
        all_checks_passed = False
    
    return all_checks_passed


def check_fixed_position_enforced():
    """Check if fixed positioning is properly enforced with !important."""
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    fixed_position_fix_path = os.path.join('app', 'static', 'css', 'fixed_position_fix.css')
    
    all_checks_passed = True
    
    # Check footer_fix.css
    with open(footer_fix_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'position: fixed !important' in content:
        print("✓ Fixed positioning is enforced with !important in footer_fix.css")
    else:
        print("ERROR: Fixed positioning may not be properly enforced in footer_fix.css")
        all_checks_passed = False
    
    # Check fixed_position_fix.css
    with open(fixed_position_fix_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'position: fixed !important' in content:
        print("✓ Fixed positioning is enforced with !important in fixed_position_fix.css")
    else:
        print("ERROR: Fixed positioning may not be properly enforced in fixed_position_fix.css")
        all_checks_passed = False
    
    return all_checks_passed


if __name__ == "__main__":
    print("Verifying fixed header and footer positioning...")
    
    base_html_ok = check_base_html()
    css_files_ok = check_css_files()
    fixed_position_enforced = check_fixed_position_enforced()
    
    if base_html_ok and css_files_ok and fixed_position_enforced:
        print("\nSUCCESS: Header and footer are properly fixed at the top and bottom of all pages!")
        sys.exit(0)
    else:
        print("\nWARNING: There might be issues with fixed header and footer positioning.")
        print("Review the errors above and make necessary adjustments.")
        sys.exit(1)
