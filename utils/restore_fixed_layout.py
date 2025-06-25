#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script restores the fixed positioning for both header and footer
while ensuring the footer is always visible on all pages, including the blog.
"""

import os


def restore_fixed_positions():
    """Restore fixed positions for header and footer in base.html."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Change the footer back to position:fixed but keep it visible with proper z-index
    updated_footer_style = 'position:fixed;left:0;right:0;bottom:0;width:100%;background:#f5f5f5;padding:1em;text-align:center;z-index:1000;box-shadow:0 -2px 8px #eee;'
    
    if 'style="position:relative;left:0;right:0;bottom:0;' in content:
        content = content.replace(
            'style="position:relative;left:0;right:0;bottom:0;width:100%;background:#f5f5f5;padding:1em;text-align:center;z-index:900;box-shadow:0 -2px 8px #eee;"', 
            f'style="{updated_footer_style}"'
        )
    
    # Add padding-bottom to the main tag to prevent content from overlapping with footer
    if '<main style=' in content:
        content = content.replace(
            '<main style="padding-bottom: 80px; min-height: calc(100vh - 180px);">', 
            '<main style="padding-top: 70px; padding-bottom: 80px; min-height: calc(100vh - 180px);">'
        )
    elif '<main>' in content:
        content = content.replace(
            '<main>', 
            '<main style="padding-top: 70px; padding-bottom: 80px; min-height: calc(100vh - 180px);">'
        )
    
    # Write the updated content back to the file
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Header and footer have been restored to fixed positions in base.html")


def update_css_for_fixed_positions():
    """Update the footer and header styles in CSS files."""
    style_css_path = os.path.join('app', 'static', 'css', 'style.css')
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    
    # Update style.css
    with open(style_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make sure header is fixed
    if 'header { position: relative;' in content:
        content = content.replace('header { position: relative;', 'header { position: fixed;')
    
    # Make sure footer is fixed
    if 'footer#site-footer { \n    position: relative;' in content:
        content = content.replace(
            'footer#site-footer { \n    position: relative;', 
            'footer#site-footer { \n    position: fixed;'
        )
    
    with open(style_css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Update footer_fix.css
    if os.path.exists(footer_fix_path):
        with open(footer_fix_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = """/* Footer Fix CSS */
body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    padding-bottom: 60px; /* Add padding to body to account for fixed footer */
}

main {
    flex: 1;
    padding-top: 70px;
    padding-bottom: 80px;
    margin-bottom: 0;
}

#site-footer {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    z-index: 1000;
}

/* Fix for blog display */
.blog-section {
    margin-bottom: 70px; /* Add margin to ensure content doesn't get hidden by footer */
}

/* Additional space for mobile */
@media (max-width: 768px) {
    body {
        padding-bottom: 80px;
    }
    main {
        padding-bottom: 100px;
    }
}
"""
        
        with open(footer_fix_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    
    print("CSS files updated to support fixed header and footer")


def update_blog_styles():
    """Add specific CSS rules for blog pages to ensure the footer is visible."""
    blog_css_path = os.path.join('app', 'static', 'css', 'blog_style.css')
    
    with open(blog_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '/* Fix for footer visibility */' not in content:
        content += """

/* Fix for footer visibility */
.blog-section {
    margin-bottom: 70px;
    padding-bottom: 20px;
}

.container {
    margin-bottom: 70px;
}

.blog-detail-content {
    margin-bottom: 80px;
}
"""
        
        with open(blog_css_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("Blog styles updated to ensure footer visibility")


if __name__ == "__main__":
    restore_fixed_positions()
    update_css_for_fixed_positions()
    update_blog_styles()
    print("Header and footer have been restored to their fixed positions while ensuring the footer is visible on all pages.")
