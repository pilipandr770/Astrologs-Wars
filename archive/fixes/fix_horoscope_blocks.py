#!/usr/bin/env python3
"""
Script to fix horoscope blocks issues:
1. Remove HTML tags from block titles
2. Add proper multilingual support for topics
3. Center buttons at the bottom of blocks
"""
import os
import re
from pathlib import Path

def update_horoscope_blocks_css():
    """Update CSS for horoscope blocks to center and align buttons"""
    # Get the base path
    base_path = os.getcwd()
    print(f"Working in directory: {base_path}")
    
    # Path to the horoscope-blocks.css file
    css_path = Path(base_path) / 'app' / 'static' / 'css' / 'horoscope-blocks.css'
    
    # Check if the file exists
    if not css_path.exists():
        print(f"❌ CSS file not found at {css_path}")
        return False
    
    # Read the current CSS content
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Create a backup of the original file
    with open(f"{css_path}.bak", 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"✓ Created backup of original CSS at {css_path}.bak")
    
    # Update the CSS for buttons
    if '.horoscope-block .btn' in css_content:
        # Update existing button styles
        new_css_content = re.sub(
            r'\.horoscope-block \.btn \{[^}]*\}',
            """.horoscope-block .btn {
  padding: 8px 16px;
  font-size: 0.9rem;
  margin-top: auto; /* Push button to the bottom */
  display: block;   /* Make button full width */
  width: 80%;       /* Width of button */
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}""",
            css_content
        )
        
        # Add button container style if not exists
        if '.button-container' not in new_css_content:
            new_css_content += """
/* Button container for proper alignment */
.button-container {
  margin-top: auto;
  text-align: center;
  width: 100%;
  padding-top: 15px;
}
"""
    else:
        # Add button styles if they don't exist
        new_css_content = css_content + """
/* Button styling */
.horoscope-block .btn {
  padding: 8px 16px;
  font-size: 0.9rem;
  margin-top: auto; /* Push button to the bottom */
  display: block;   /* Make button full width */
  width: 80%;       /* Width of button */
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}

.horoscope-block .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Button container for proper alignment */
.button-container {
  margin-top: auto;
  text-align: center;
  width: 100%;
  padding-top: 15px;
}
"""
    
    # Write the updated CSS content
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(new_css_content)
    
    print(f"✓ Updated button styles in {css_path}")
    return True

def update_blog_template():
    """Update blog templates to strip HTML tags and add multilingual support"""
    # Get the base path
    base_path = os.getcwd()
    
    # Update blog index template
    blog_index_path = Path(base_path) / 'app' / 'templates' / 'blog' / 'index.html'
    if blog_index_path.exists():
        # Read the template content
        with open(blog_index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a backup of the original file
        with open(f"{blog_index_path}.bak", 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created backup of original blog index template at {blog_index_path}.bak")
        
        # Add |striptags filter to the title
        content = re.sub(
            r'<h3 class="card-title h5">{{ get_blog_block_title\(block\) }}</h3>',
            '<h3 class="card-title h5">{{ get_blog_block_title(block)|striptags }}</h3>',
            content
        )
        
        # Update the button container to center it
        content = re.sub(
            r'<div class="card-footer bg-white border-0 mt-auto">\s*<a href="{{ url_for',
            '<div class="card-footer bg-white border-0 text-center mt-auto">\n                        <a href="{{ url_for',
            content
        )
        
        # Write the updated template content
        with open(blog_index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Updated blog index template at {blog_index_path}")
    else:
        print(f"❌ Blog index template not found at {blog_index_path}")
    
    # Update blog detail template
    blog_detail_path = Path(base_path) / 'app' / 'templates' / 'blog' / 'block_detail.html'
    if blog_detail_path.exists():
        # Read the template content
        with open(blog_detail_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a backup of the original file
        with open(f"{blog_detail_path}.bak", 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created backup of original blog detail template at {blog_detail_path}.bak")
        
        # Add |striptags filter to the title in breadcrumbs and h1
        content = re.sub(
            r'<li class="breadcrumb-item active" aria-current="page">{{ get_blog_block_title\(block\) }}</li>',
            '<li class="breadcrumb-item active" aria-current="page">{{ get_blog_block_title(block)|striptags }}</li>',
            content
        )
        
        content = re.sub(
            r'<h1 class="mb-4">{{ get_blog_block_title\(block\) }}</h1>',
            '<h1 class="mb-4">{{ get_blog_block_title(block)|striptags }}</h1>',
            content
        )
        
        # Write the updated template content
        with open(blog_detail_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Updated blog detail template at {blog_detail_path}")
    else:
        print(f"❌ Blog detail template not found at {blog_detail_path}")
    
    return True

def update_blog_routes():
    """Update the blog routes to improve multilingual support for titles"""
    # Get the base path
    base_path = os.getcwd()
    
    # Path to the blog routes file
    blog_routes_path = Path(base_path) / 'app' / 'blog' / 'routes.py'
    if not blog_routes_path.exists():
        print(f"❌ Blog routes file not found at {blog_routes_path}")
        return False
    
    # Read the current routes content
    with open(blog_routes_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create a backup of the original file
    with open(f"{blog_routes_path}.bak", 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created backup of original blog routes at {blog_routes_path}.bak")
      # Update the get_blog_block_title function to better handle multilingual content
    title_func_pattern = r'def get_blog_block_title\(block\):.*?return block\.title'
    
    new_title_func = '''def get_blog_block_title(block):
    """Получает заголовок блока блога в текущем языке"""
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
    return block.title'''
    
    # Replace the function
    updated_content = re.sub(title_func_pattern, new_title_func, content, flags=re.DOTALL)
    
    # Write the updated content
    with open(blog_routes_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✓ Updated blog routes with improved multilingual support at {blog_routes_path}")
    return True

if __name__ == "__main__":
    print("🔧 Starting fixes for horoscope blocks...")
    
    # 1. Update CSS for buttons
    update_horoscope_blocks_css()
    
    # 2. Update blog templates to strip HTML tags
    update_blog_template()
    
    # 3. Update blog routes for better multilingual support
    update_blog_routes()
    
    print("✅ Fixes completed successfully!")
    print("\nThese changes will:")
    print("1. Remove HTML tags from block titles")
    print("2. Add proper multilingual support for topics")
    print("3. Center buttons at the bottom of blocks")
