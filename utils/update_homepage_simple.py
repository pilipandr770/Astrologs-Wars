#!/usr/bin/env python3
"""
Script to update homepage to show horoscope blocks (local version).
- Removes recent blog posts section
- Adds astrology blocks with links to detail pages
"""
import os
import re

def update_files():
    """Update necessary files to modify homepage"""
    # Get the base path for the project
    base_path = os.getcwd()
    
    print(f"Working in directory: {base_path}")
    
    # Create directory for CSS file if it doesn't exist
    css_path = os.path.join(base_path, 'app', 'static', 'css')
    os.makedirs(css_path, exist_ok=True)
    
    # Create horoscope-blocks.css file
    css_content = """/* Стили для блоков гороскопов на главной странице */
.horoscope-block {
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
  height: 100%;
  cursor: pointer;
  background-color: #fff;
}

.horoscope-block:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.horoscope-block h3 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #333;
}

.horoscope-block p {
  font-size: 0.9rem;
  color: #666;
  flex-grow: 1;
  margin-bottom: 15px;
}

.horoscope-block img {
  border-radius: 8px;
  margin-bottom: 12px;
  height: 150px;
  object-fit: cover;
  width: 100%;
}

.horoscope-block .btn {
  align-self: center;
}"""
    
    css_file_path = os.path.join(css_path, 'horoscope-blocks.css')
    with open(css_file_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"✅ Created horoscope-blocks.css file: {css_file_path}")
    
    # Update the base.html template to include CSS
    base_template_path = os.path.join(base_path, 'app', 'templates', 'base.html')
    with open(base_template_path, 'r', encoding='utf-8') as f:
        base_content = f.read()
    
    if "horoscope-blocks.css" not in base_content:
        css_link_section = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/button_alignment.css\') }}">'
        new_css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/button_alignment.css\') }}">\n    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/horoscope-blocks.css\') }}">'
        
        base_content = base_content.replace(css_link_section, new_css_link)
        
        with open(base_template_path, 'w', encoding='utf-8') as f:
            f.write(base_content)
        
        print(f"✅ Updated base.html to include CSS")
    else:
        print("ℹ️ horoscope-blocks.css already included in base.html")
    
    # Update the main/routes.py file 
    routes_file = os.path.join(base_path, 'app', 'main', 'routes.py')
    try:
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if routes.py already has our changes
        if 'recent_blog_blocks' in content and 'astrology_blocks' not in content:
            # Update the definition of blog blocks
            content = content.replace(
                "recent_blog_blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).limit(7).all()",
                "astrology_blocks = BlogBlock.query.filter_by(is_active=True).filter(BlogBlock.position <= 8).order_by(BlogBlock.position).all()"
            )
            
            # Update the template variables passed
            content = content.replace(
                "recent_blog_blocks=recent_blog_blocks,",
                "astrology_blocks=astrology_blocks,"
            )
            
            # Write the updated content
            with open(routes_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated app/main/routes.py")
        else:
            print(f"ℹ️ Routes file already updated or doesn't contain expected content.")
    except Exception as e:
        print(f"❌ Error updating routes.py: {str(e)}")
    
    # Update the index.html template
    template_file = os.path.join(base_path, 'app', 'templates', 'index.html')
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Replace recent blog blocks section with astrology blocks if needed
        if '{# --- Блок з останніми блоками блогу --- #}' in template_content and '{# --- БЛОКИ ГОРОСКОПОВ --- #}' not in template_content:
            # Find start of recent blog blocks section
            recent_blog_start = '{# --- Блок з останніми блоками блогу --- #}'
            recent_blog_start_pos = template_content.find(recent_blog_start)
            
            if recent_blog_start_pos == -1:
                print("⚠️ Could not find start of recent blog blocks section")
                return
            
            # Find the end of the recent blog blocks section
            recent_blog_end = '{% endif %}'
            # We need to find the specific instance of endif that closes the recent_blog_blocks if condition
            search_start = recent_blog_start_pos + len(recent_blog_start)
            recent_blog_end_pos = template_content.find(recent_blog_end, search_start)
            
            if recent_blog_end_pos == -1:
                print("⚠️ Could not find end of recent blog blocks section")
                return
            
            # Create the new astrology blocks section
            astrology_blocks_section = '''  {# --- БЛОКИ ГОРОСКОПОВ --- #}
  {% if astrology_blocks %}
  <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4 mb-4">
    {% for block in astrology_blocks %}
    <div class="col">
      <div class="block-card horoscope-block h-100" onclick="window.location='{{ url_for('blog.block_detail', position=block.position) }}'">
        {% if block.featured_image %}
        <img src="{{ url_for('static', filename='uploads/blog/' + block.featured_image) }}" 
             alt="{{ get_blog_block_title(block) }}" class="card-img-top"
             onerror="this.src='{{ url_for('static', filename='uploads/' + block.featured_image) }}'">
        {% endif %}
        <h3>{{ get_blog_block_title(block) }}</h3>
        <p>{{ get_blog_block_summary(block)|safe }}</p>
        <div class="text-center mt-auto">
          <a href="{{ url_for('blog.block_detail', position=block.position) }}" class="btn btn-outline-primary">
            {% if g.get('lang') == 'en' %}
              {{ _('Read more') }}
            {% elif g.get('lang') == 'de' %}
              {{ _('Mehr lesen') }}
            {% elif g.get('lang') == 'ru' %}
              {{ _('Читать далее') }}
            {% else %}
              {{ _('Читати далі') }}
            {% endif %}
          </a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
  {% endif %}'''
            
            # Complete the endif of the if recent_blog_blocks condition
            recent_blog_end_pos += len(recent_blog_end)
            
            # Replace the section
            new_template = template_content[:recent_blog_start_pos] + astrology_blocks_section + template_content[recent_blog_end_pos:]
            
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(new_template)
            
            print(f"✅ Updated app/templates/index.html")
        else:
            print(f"ℹ️ Template already updated or doesn't contain expected content.")
    except Exception as e:
        print(f"❌ Error updating index.html: {str(e)}")
    
    print("\n🎉 All updates completed!")

if __name__ == "__main__":
    update_files()
