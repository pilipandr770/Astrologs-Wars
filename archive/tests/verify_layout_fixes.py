#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script verifies that language switching, footer visibility, and chat widget issues have been fixed.
"""

import os
import re
import sys


def check_language_switcher():
    """Check if the language switcher form in base.html has been fixed."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for onchange attribute in the language switcher
    if 'onchange="this.form.submit()"' in content and 'lang_switch' in content:
        print("✓ Language switcher form has been fixed in base.html")
        return True
    else:
        print("ERROR: Language switcher form may not be properly fixed in base.html")
        return False


def check_index_template_reference():
    """Check if the template reference in main/routes.py has been fixed."""
    routes_path = os.path.join('app', 'main', 'routes.py')
    
    with open(routes_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if index.html.new has been replaced with index.html
    if "render_template('index.html'" in content and "render_template('index.html.new'" not in content:
        print("✓ Template reference has been fixed in main/routes.py")
        return True
    else:
        print("ERROR: Template reference may not be properly fixed in main/routes.py")
        return False


def check_z_index():
    """Check if z-index values have been increased for footer and chat widget."""
    style_css_path = os.path.join('app', 'static', 'css', 'style.css')
    
    with open(style_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check z-index for footer and chat widgets
    all_ok = True
    
    # Check base.html for footer z-index
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        base_content = f.read()
    
    if 'z-index:9000;' in base_content and 'id="site-footer"' in base_content:
        print("✓ Footer z-index has been increased in base.html")
    else:
        print("ERROR: Footer z-index may not be properly increased in base.html")
        all_ok = False
    
    # Check if chat widget has increased z-index
    if 'z-index:9100 !important' in base_content and 'chat-circle-btn' in base_content:
        print("✓ Chat button z-index has been increased in base.html")
    else:
        print("ERROR: Chat button z-index may not be properly increased in base.html")
        all_ok = False
    
    return all_ok


def check_footer_visibility():
    """Check if footer visibility has been improved."""
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    
    with open(footer_fix_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for visibility rules
    if 'visibility: visible !important' in content and 'z-index: 9000 !important' in content:
        print("✓ Footer visibility has been improved in footer_fix.css")
        return True
    else:
        print("ERROR: Footer visibility may not be properly improved in footer_fix.css")
        return False


if __name__ == "__main__":
    print("Verifying fixes for language switching, footer visibility, and chat widget...")
    
    lang_switcher_ok = check_language_switcher()
    template_ref_ok = check_index_template_reference()
    z_index_ok = check_z_index()
    footer_visibility_ok = check_footer_visibility()
    
    if lang_switcher_ok and template_ref_ok and z_index_ok and footer_visibility_ok:
        print("\nSUCCESS: All fixes have been verified!")
        print("The language switcher, footer, and chat widget should now be working correctly on all pages.")
        sys.exit(0)
    else:
        print("\nWARNING: Some fixes may not have been applied correctly.")
        print("Review the errors above and make necessary adjustments.")
        sys.exit(1)
