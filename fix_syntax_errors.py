#!/usr/bin/env python3
"""
Script to fix syntax errors in blog/routes.py
- Replace Russian/Ukrainian keywords with English ones
"""
import os
from pathlib import Path

def fix_syntax_errors():
    """Fix syntax errors in the blog/routes.py file"""
    # Get the base path
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
    with open(f"{blog_routes_path}.syntax.bak", 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created syntax backup at {blog_routes_path}.syntax.bak")
    
    # Define replacements (Russian/Ukrainian keywords -> English)
    replacements = [
        ('элиф', 'elif'),
        ('Элиф', 'elif'),
        ('ЭЛИФ', 'elif'),
        ('и ', 'and '),
        ('И ', 'and '),
        ('или', 'or'),
        ('Или', 'or'),
        ('ИЛИ', 'or'),
        ('если', 'if'),
        ('Если', 'if'),
        ('ЕСЛИ', 'if'),
        ('еще', 'else'),
        ('Еще', 'else'),
        ('ЕЩЕ', 'else'),
        ('верно', 'True'),
        ('Верно', 'True'),
        ('ВЕРНО', 'True'),
        ('ложь', 'False'),
        ('Ложь', 'False'),
        ('ЛОЖЬ', 'False'),
        ('для', 'for'),
        ('Для', 'for'),
        ('ДЛЯ', 'for'),
        ('в', 'in'),
        ('В', 'in'),
        ('возвращение', 'return'),
        ('Возвращение', 'return'),
        ('ВОЗВРАЩЕНИЕ', 'return')
    ]
    
    # Apply replacements
    fixed_content = content
    for rus, eng in replacements:
        fixed_content = fixed_content.replace(rus, eng)
    
    # Write the fixed content
    with open(blog_routes_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"✓ Fixed syntax in {blog_routes_path}")
    
    # Check for other potential issues in the file
    if 'get_blog_block_title' in fixed_content:
        print("⚠️ Note: The file contains function 'get_blog_block_title', please check for proper English syntax")
    
    return True

if __name__ == "__main__":
    print("🔧 Starting syntax fix...")
    fix_syntax_errors()
    print("✅ Syntax fix completed!")
    print("\nPlease commit and push these changes to fix the deployment error on Render.")
