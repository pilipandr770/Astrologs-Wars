#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script fixes issues with language switching, footer visibility, and chat widget.
"""

import os
import re


def fix_language_switcher():
    """Fix the language switcher form in base.html."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the language switcher form to include action and method explicitly
    updated_lang_switcher = """
        <!-- Права частина: Перемикач мов -->
        <div class="nav-right">
          <form id="lang-switcher-form" action="" method="get" style="display:inline;">
            <input type="hidden" name="lang_switch" value="1">
            <select name="lang" id="lang-switcher" onchange="this.form.submit()" style="padding:6px 12px;border-radius:8px;border:1px solid #ddd;font-size:1em;background:#fff;">
              <option value="uk" {% if g.get('lang', 'uk') == 'uk' %}selected{% endif %}>UA</option>
              <option value="en" {% if g.get('lang') == 'en' %}selected{% endif %}>EN</option>
              <option value="de" {% if g.get('lang') == 'de' %}selected{% endif %}>DE</option>
              <option value="ru" {% if g.get('lang') == 'ru' %}selected{% endif %}>RU</option>
            </select>
          </form>
        </div>"""
    
    # Use regex to replace the language switcher section
    pattern = r'<!-- Права частина: Перемикач мов -->\s*<div class="nav-right">.*?</div>'
    updated_content = re.sub(pattern, updated_lang_switcher, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("Language switcher form has been fixed in base.html")


def fix_index_template_reference():
    """Fix the template reference in main/routes.py."""
    routes_path = os.path.join('app', 'main', 'routes.py')
    
    with open(routes_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace index.html.new with index.html
    if "render_template('index.html.new'" in content:
        content = content.replace(
            "render_template('index.html.new'", 
            "render_template('index.html'"
        )
    
    # Write the updated content back to the file
    with open(routes_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Template reference has been fixed in main/routes.py")


def enhance_z_index():
    """Increase z-index for footer and chat widget to ensure they're visible on all pages."""
    style_css_path = os.path.join('app', 'static', 'css', 'style.css')
    
    with open(style_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure the footer has a high z-index
    if 'footer#site-footer {' in content:
        content = content.replace(
            'z-index: 1000;', 
            'z-index: 9000;'
        )
    
    # Update chat widget z-index
    if 'chat-circle-btn {' in content:
        content = content.replace(
            'z-index: 1100;', 
            'z-index: 9100;'
        )
    
    if 'chat-window {' in content:
        content = content.replace(
            'z-index: 1200;', 
            'z-index: 9200;'
        )
    
    # Write the updated content back to the file
    with open(style_css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Update base.html footer z-index
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'z-index:1000;' in content and 'id="site-footer"' in content:
        content = content.replace(
            'z-index:1000;',
            'z-index:9000;'
        )
    
    # Write the updated content back to the file
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Z-index values have been increased for footer and chat widget")


def ensure_footer_visibility():
    """Ensure footer visibility on all pages."""
    footer_fix_path = os.path.join('app', 'static', 'css', 'footer_fix.css')
    
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
    z-index: 9000 !important;
    display: block !important;
    visibility: visible !important;
    background: #f5f5f5 !important;
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

body > footer, 
body > #chat-open-btn, 
body > #chat-window {
    z-index: 9000 !important;
    display: block !important;
    visibility: visible !important;
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
    
    print("Footer visibility has been improved in footer_fix.css")


def fix_chat_widget_visibility():
    """Fix chat widget visibility."""
    base_html_path = os.path.join('app', 'templates', 'base.html')
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update chat widget styles to ensure visibility
    if 'chat-circle-btn' in content:
        content = content.replace(
            'class="chat-circle-btn"', 
            'class="chat-circle-btn" style="z-index:9100 !important; display:block !important; visibility:visible !important;"'
        )
    
    if 'chat-window' in content:
        content = content.replace(
            'class="chat-window"', 
            'class="chat-window" style="z-index:9200 !important;"'
        )
    
    # Write the updated content back to the file
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Chat widget visibility has been improved in base.html")


if __name__ == "__main__":
    fix_language_switcher()
    fix_index_template_reference()
    enhance_z_index()
    ensure_footer_visibility()
    fix_chat_widget_visibility()
    print("All fixes have been applied successfully!")
