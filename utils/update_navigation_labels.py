#!/usr/bin/env python3
"""
Script to update navigation button labels in base.html
- Change 'Blog' to 'Forecasts/Прогнозы/Прогнози'
- Change 'Shop/Магазин' to 'Personal Horoscope/Персональный гороскоп/Персональний гороскоп'
"""
import os
import re

def update_navigation_labels():
    """Update navigation labels in base.html"""
    # Get the base path
    base_path = os.getcwd()
    
    print(f"Working in directory: {base_path}")
    
    # Path to the base.html template
    template_path = os.path.join(base_path, 'app', 'templates', 'base.html')
    
    # Read the current template content
    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create a backup of the original file
    backup_path = template_path + '.nav.bak'
    with open(backup_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Created backup of original template at: {backup_path}")

    # Update the "Blog" link to "Forecasts/Прогнозы/Прогнози"
    # Find and replace the Blog link text
    blog_pattern = r'<a href="\{\{ url_for\(\'blog\.index\'\) \}\}">{{ _\(\'Блог\'\) }}</a>'
    blog_replacement = """<a href="{{ url_for('blog.index') }}">
            {% if g.get('lang') == 'en' %}
              {{ _('Forecasts') }}
            {% elif g.get('lang') == 'de' %}
              {{ _('Prognosen') }}
            {% elif g.get('lang') == 'ru' %}
              {{ _('Прогнозы') }}
            {% else %}
              {{ _('Прогнози') }}
            {% endif %}
          </a>"""
    
    content = re.sub(blog_pattern, blog_replacement, content)
    
    # Update the Shop/Магазин section to Personal Horoscope/Персональный гороскоп/Персональний гороскоп
    shop_pattern = r'''<a href="\{\{ url_for\('shop\.index'\) \}\}">
            \{% if g\.get\('lang'\) == 'en' %\}
              \{\{ _\('Shop'\) \}\}
            \{% elif g\.get\('lang'\) == 'de' %\}
              \{\{ _\('Shop'\) \}\}
            \{% elif g\.get\('lang'\) == 'ru' %\}
              \{\{ _\('Магазин'\) \}\}
            \{% else %\}
              \{\{ _\('Магазин'\) \}\}
            \{% endif %\}
          </a>'''
    shop_replacement = """<a href="{{ url_for('shop.index') }}">
            {% if g.get('lang') == 'en' %}
              {{ _('Personal Horoscope') }}
            {% elif g.get('lang') == 'de' %}
              {{ _('Persönliches Horoskop') }}
            {% elif g.get('lang') == 'ru' %}
              {{ _('Персональный гороскоп') }}
            {% else %}
              {{ _('Персональний гороскоп') }}
            {% endif %}
          </a>"""
    
    content = re.sub(shop_pattern, shop_replacement, content, flags=re.DOTALL)
    
    # Write the updated template content
    with open(template_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Updated navigation labels in: {template_path}")
    print("Changes made:")
    print("1. 'Blog' -> 'Forecasts/Prognosen/Прогнозы/Прогнози'")
    print("2. 'Shop/Магазин' -> 'Personal Horoscope/Persönliches Horoskop/Персональный гороскоп/Персональний гороскоп'")

if __name__ == "__main__":
    update_navigation_labels()
