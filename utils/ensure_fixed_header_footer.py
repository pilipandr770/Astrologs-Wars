#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script ensures that both header and footer are fixed at the top
and bottom of all pages, respectively.
"""

import os
import re


def ensure_fixed_header_footer():
    """Ensure header is fixed at the top and footer at the bottom."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check and fix header tag to ensure it has position:fixed style
    if '<header>' in content:
        content = content.replace(
            '<header>',
            '<header style="position:fixed;top:0;left:0;right:0;width:100%;z-index:9000;background:var(--header-footer-bg);box-shadow:0 4px 12px rgba(0,0,0,0.05);">'
        )
    
    # Ensure body has proper padding to accommodate fixed header and footer
    if 'style="padding-top: 80px; padding-bottom: 80px;"' not in content:
        content = content.replace(
            '<body>',
            '<body style="padding-top: 80px; padding-bottom: 80px;">'
        )
    
    # Write the updated content back to the file
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Header and footer fixed position styles have been set in base.html")


def update_css_files():
    """Update CSS files to ensure consistent fixed header and footer."""
    style_css_path = os.path.join('app', 'static', 'css', 'style.css')
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    
    # Update style.css
    with open(style_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure header has position: fixed
    if 'header {' in content and 'position: fixed;' not in content:
        content = content.replace(
            'header {',
            'header { position: fixed;'
        )
    
    # Write the updated content back to the file
    with open(style_css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Update footer_fix.css
    with open(footer_fix_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_content = """/* Footer Fix CSS */
body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    padding-top: 80px; /* Add padding for fixed header */
    padding-bottom: 60px; /* Add padding for fixed footer */
}

main {
    flex: 1;
    padding-top: 20px;  /* Reduced since body has padding-top now */
    padding-bottom: 80px;
    margin-bottom: 0;
}

/* Fixed header styles */
header {
    position: fixed !important;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 9000 !important;
    background: var(--header-footer-bg, #f7f5ed) !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* Fixed footer styles */
#site-footer {
    position: fixed !important;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    z-index: 9000 !important;
    display: block !important;
    visibility: visible !important;
    background: var(--header-footer-bg, #f5f5f5) !important;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
}

/* Fix for blog display */
.blog-section {
    margin-bottom: 70px; /* Add margin to ensure content doesn't get hidden by footer */
}

/* Fix for specific pages that might hide the footer */
body > * {
    position: relative;
    z-index: auto !important;
}

body > main {
    z-index: 1 !important;
}

/* Additional space for mobile */
@media (max-width: 768px) {
    body {
        padding-top: 70px;
        padding-bottom: 80px;
    }
    main {
        padding-bottom: 100px;
    }
}
"""
    
    with open(footer_fix_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("CSS files have been updated to ensure consistent fixed header and footer")


def create_cross_browser_fix():
    """Create a CSS fix for cross-browser compatibility."""
    cross_browser_fix_path = os.path.join('app', 'static', 'css', 'fixed_position_fix.css')
    
    cross_browser_content = """/* Cross-browser fixes for position:fixed elements */

/* Ensure fixed positioning works in all browsers */
html, body {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
}

/* Header fixed position enforcement */
header {
    position: fixed !important;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 9000 !important;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
}

/* Footer fixed position enforcement */
#site-footer {
    position: fixed !important;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    z-index: 9000 !important;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
}

/* Fix for iOS Safari and Chrome issues with fixed positioning */
@supports (-webkit-overflow-scrolling: touch) {
    header, #site-footer {
        -webkit-transform: translateZ(0);
        transform: translateZ(0);
    }
}
"""
    
    with open(cross_browser_fix_path, 'w', encoding='utf-8') as f:
        f.write(cross_browser_content)
    
    # Add the new CSS file to base.html
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'fixed_position_fix.css' not in content:
        content = content.replace(
            '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/footer_fix.css\') }}">',
            '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/footer_fix.css\') }}">\n    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/fixed_position_fix.css\') }}">'
        )
        
        # Write the updated content back to the file
        with open(base_html_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("Cross-browser fixed position CSS fixes have been added")


if __name__ == "__main__":
    ensure_fixed_header_footer()
    update_css_files()
    create_cross_browser_fix()
    print("Header and footer are now properly fixed at the top and bottom of all pages")
