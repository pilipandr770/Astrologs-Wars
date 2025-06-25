#!/usr/bin/env python3
"""
Script to fix indentation and syntax errors in blog/routes.py
"""
import os
from pathlib import Path

def fix_indentation_errors():
    """Fix indentation and syntax errors in the blog/routes.py file"""
    base_path = os.getcwd()
    print(f"Working in directory: {base_path}")
    
    # Path to the blog routes file
    blog_routes_path = Path(base_path) / 'app' / 'blog' / 'routes.py'
    
    if not blog_routes_path.exists():
        print(f"❌ Blog routes file not found at {blog_routes_path}")
        return False
    
    # Read the current file content
    with open(blog_routes_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create a backup of the original file
    with open(f"{blog_routes_path}.indent.bak", 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created indentation backup at {blog_routes_path}.indent.bak")
    
    # Fixed version of the get_blog_block_title function
    fixed_content = """# app/blog/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session
from flask_login import current_user
from app.models import db, BlogBlock
from app.forms import BlogBlockForm
from app.utils.file_utils import save_uploaded_file
from app.admin.routes import admin_required
import os
from datetime import datetime

from app.blog import blog_bp

# Вспомогательные функции для получения локализованного контента блога
def get_blog_block_title(block):
    \"\"\"Получает заголовок блока блога в текущем языке\"\"\"
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        # Prefer title_ua if available, otherwise use the primary title
        return block.title_ua if block.title_ua else block.title
    elif lang == 'en' and block.title_en:
        return block.title_en
    elif lang == 'de' and block.title_de:
        return block.title_de
    elif lang == 'ru' and block.title_ru:
        return block.title_ru
    return block.title

def get_blog_block_content(block):
    \"\"\"Получает содержимое блока блога в текущем языке\"\"\"
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        # Prefer content_ua if available, otherwise use the primary content
        return block.content_ua if block.content_ua else block.content
    elif lang == 'en' and block.content_en:
        return block.content_en
    elif lang == 'de' and block.content_de:
        return block.content_de
    elif lang == 'ru' and block.content_ru:
        return block.content_ru
    return block.content

def get_blog_block_summary(block):
    \"\"\"Получает краткое описание блока блога в текущем языке\"\"\"
    from app.utils.text_utils import strip_html_tags
    
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        # Prefer summary_ua if available, otherwise use the primary summary
        summary = block.summary_ua if block.summary_ua else block.summary
    elif lang == 'en' and block.summary_en:
        summary = block.summary_en
    elif lang == 'de' and block.summary_de:
        summary = block.summary_de
    elif lang == 'ru' and block.summary_ru:
        summary = block.summary_ru
    else:
        summary = block.summary or ''
        
    # Strip HTML tags and return a short excerpt
    clean_summary = strip_html_tags(summary)
    return clean_summary[:200] + '...' if len(clean_summary) > 200 else clean_summary"""

    # Find end of the get_blog_block_summary function
    summary_end_index = content.find('@blog_bp.route')
    if summary_end_index == -1:
        print("Could not find end of get_blog_block_summary function")
        return False
    
    # Get the rest of the file content after the get_blog_block_summary function
    rest_content = content[summary_end_index:]
    
    # Combine fixed part with the rest of the file
    final_content = fixed_content + "\n\n" + rest_content
    
    # Fix other potential issues
    final_content = final_content.replace('inспомогательные', 'Вспомогательные')
    final_content = final_content.replace('функциand', 'функции')
    final_content = final_content.replace('получения локализоinанного', 'получения локализованного')
    final_content = final_content.replace('заголоinок', 'заголовок')
    final_content = final_content.replace(' in ', ' в ')
    
    # Write the fixed content
    with open(blog_routes_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✓ Fixed indentation and syntax in {blog_routes_path}")
    return True

if __name__ == "__main__":
    print("🔧 Starting indentation fix...")
    fix_indentation_errors()
    print("✅ Indentation fix completed!")
    print("\nPlease commit and push these changes to fix the deployment error on Render.")
