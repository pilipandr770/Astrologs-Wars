#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script fixes the footer visibility in the base.html template.
It changes the footer from position:fixed to position:relative
and adds proper margin-top to ensure it's visible on all pages.
It also adds padding-bottom to the main content area to prevent
the footer from overlapping with content.
"""

import os


def fix_footer():
    """Fix the footer in base.html to make it visible on all pages."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Change the footer from position:fixed to position:relative
    # and add proper spacing to ensure visibility
    updated_footer_style = 'position:relative;left:0;right:0;bottom:0;width:100%;background:#f5f5f5;padding:1em;text-align:center;z-index:900;box-shadow:0 -2px 8px #eee;'
    
    # Update the footer style in the HTML
    if 'position:fixed;left:0;right:0;bottom:0' in content:
        content = content.replace(
            'style="position:fixed;left:0;right:0;bottom:0;width:100%;background:#f5f5f5;padding:1em;text-align:center;z-index:900;box-shadow:0 -2px 8px #eee;"', 
            f'style="{updated_footer_style}"'
        )
    
    # Add padding-bottom to the main tag to prevent content from overlapping with footer
    if '<main>' in content:
        content = content.replace(
            '<main>', 
            '<main style="padding-bottom: 80px; min-height: calc(100vh - 180px);">'
        )
    
    # Write the updated content back to the file
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Footer has been fixed in base.html")


def update_css_footer():
    """Update the footer styles in the CSS file."""
    css_path = os.path.join('app', 'static', 'css', 'style.css')
    
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the fixed positioning with relative positioning
    if 'footer#site-footer { \n    position: fixed;' in content:
        content = content.replace(
            'footer#site-footer { \n    position: fixed;', 
            'footer#site-footer { \n    position: relative;'
        )
    
    # Write the updated content back to the file
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Footer styles updated in style.css")


def add_css_fix():
    """Create CSS fix that ensures proper spacing at the bottom of every page."""
    css_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    
    css_content = """/* Footer Fix CSS */
body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

main {
    flex: 1;
    padding-bottom: 80px;
    margin-bottom: 30px;
}

#site-footer {
    margin-top: auto;
    position: relative;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
}
"""
    
    with open(css_fix_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    # Add the CSS file to base.html if it doesn't already include it
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "footer_fix.css" not in content:
        # Insert the link tag after the other CSS links
        css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/footer_fix.css\') }}">'
        if '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/astro_admin.css\') }}">' in content:
            content = content.replace(
                '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/astro_admin.css\') }}">',
                f'<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/astro_admin.css\') }}">\n    {css_link}'
            )
    
        # Write the updated content back to the file
        with open(base_html_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("Footer fix CSS created and linked in base.html")


if __name__ == "__main__":
    fix_footer()
    update_css_footer()
    add_css_fix()
    print("Footer visibility has been fixed on all pages.")
