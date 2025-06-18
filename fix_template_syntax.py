#!/usr/bin/env python3
"""
Script to fix the Jinja2 template syntax error in index.html
"""
import os
import re

def fix_template_syntax():
    """Fix template syntax issues in index.html"""
    # Get the base path for the project
    base_path = os.getcwd()
    
    print(f"Working in directory: {base_path}")
    
    # Path to the index.html template
    template_path = os.path.join(base_path, 'app', 'templates', 'index.html')
    
    # Read the current template content
    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create a backup of the original file
    backup_path = template_path + '.bak'
    with open(backup_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Created backup of original template at: {backup_path}")

    # Fix the template by making sure we only have {% block %} with {% endblock %} 
    # and {% if %} with {% endif %}
    
    # Simplified template that only shows:
    # 1. Top admin-editable block (with image, title, topic, and body)
    # 2. Shop section at the bottom
    fixed_content = """{% extends 'base.html' %}
{% block title %}{{ _('Головна') }}{% endblock %}

{% block content %}
<div class="container py-5">
  <!-- Main info block (top) -->
  <div class="row justify-content-center">
    <div class="col-md-10">
      <div class="main-info-block">
        {% if top_block %}
          <div class="text-center">
            {% if top_block.image %}
              <img src="{{ url_for('static', filename='uploads/' ~ top_block.image) }}" alt="{{ get_block_title(top_block) }}" class="block-image img-fluid">
            {% endif %}
            <h1>{{ get_block_title(top_block) }}</h1>
          </div>
          <div class="content">
            {{ get_block_content(top_block)|safe }}
          </div>
        {% else %}
          <div class="text-center">
            <h1>
              {% if g.get('lang') == 'en' %}
                {{ _('Astrology Portal') }}
              {% elif g.get('lang') == 'de' %}
                {{ _('Astrologie-Portal') }}
              {% elif g.get('lang') == 'ru' %}
                {{ _('Астрологический портал') }}
              {% else %}
                {{ _('Астрологічний портал') }}
              {% endif %}
            </h1>
          </div>
          <div class="content">
            <p class="lead text-center">
              {% if g.get('lang') == 'en' %}
                {{ _('Welcome to our professional astrology portal, where you can discover daily horoscopes, personal forecasts, and astrological consultations.') }}
              {% elif g.get('lang') == 'de' %}
                {{ _('Willkommen auf unserem professionellen Astrologieportal, wo Sie tägliche Horoskope, persönliche Vorhersagen und astrologische Beratungen entdecken können.') }}
              {% elif g.get('lang') == 'ru' %}
                {{ _('Добро пожаловать на наш профессиональный астрологический портал, где вы можете открыть для себя ежедневные гороскопы, персональные прогнозы и астрологические консультации.') }}
              {% else %}
                {{ _('Вітаємо на нашому професійному астрологічному порталі, де ви можете дізнатися щоденні гороскопи, персональні прогнози та отримати астрологічні консультації.') }}
              {% endif %}
            </p>
          </div>
        {% endif %}
      </div>
    </div>
  </div>
  
  <!-- Shop section (bottom) -->
  <div class="row justify-content-center">
    <div class="col-md-10">
      <div class="featured-shop-section">
        <h2>
          {% if g.get('lang') == 'en' %}
            {{ _('Featured Products') }}
          {% elif g.get('lang') == 'de' %}
            {{ _('Ausgewählte Produkte') }}
          {% elif g.get('lang') == 'ru' %}
            {{ _('Избранные товары') }}
          {% else %}
            {{ _('Вибрані товари') }}
          {% endif %}
        </h2>
        
        <div class="shop-description">
          {% if g.get('lang') == 'en' %}
            {{ _('Discover our collection of professional astrological services and products for your spiritual journey.') }}
          {% elif g.get('lang') == 'de' %}
            {{ _('Entdecken Sie unsere Sammlung professioneller astrologischer Dienstleistungen und Produkte für Ihre spirituelle Reise.') }}
          {% elif g.get('lang') == 'ru' %}
            {{ _('Откройте для себя нашу коллекцию профессиональных астрологических услуг и товаров для вашего духовного пути.') }}
          {% else %}
            {{ _('Відкрийте для себе нашу колекцію професійних астрологічних послуг та товарів для вашої духовної подорожі.') }}
          {% endif %}
        </div>
        
        {% if featured_products %}
          <div class="row row-cols-1 row-cols-md-3 g-4">
            {% for product in featured_products %}
              <div class="col">
                <a href="{{ url_for('shop.product', slug=product.slug) }}" class="text-decoration-none">
                  <div class="product-card">
                    {% if product.image %}
                      <img src="{{ url_for('static', filename='uploads/' ~ product.image) }}" alt="{{ get_product_name(product) }}" class="img-fluid">
                    {% endif %}
                    <div class="card-body">
                      <h5 class="card-title">{{ get_product_name(product) }}</h5>
                      <p class="card-price">{{ product.price }} {% if settings %}{{ settings.currency_symbol or '€' }}{% else %}€{% endif %}</p>
                    </div>
                  </div>
                </a>
              </div>
            {% endfor %}
          </div>
        {% else %}
          <div class="text-center my-4">
            <p>
              {% if g.get('lang') == 'en' %}
                {{ _('No products available at the moment.') }}
              {% elif g.get('lang') == 'de' %}
                {{ _('Derzeit keine Produkte verfügbar.') }}
              {% elif g.get('lang') == 'ru' %}
                {{ _('На данный момент нет доступных товаров.') }}
              {% else %}
                {{ _('На даний момент немає доступних товарів.') }}
              {% endif %}
            </p>
          </div>
        {% endif %}
        
        <div class="shop-button-container">
          <a href="{{ url_for('shop.index') }}" class="btn btn-primary btn-shop">
            {% if g.get('lang') == 'en' %}
              {{ _('Visit Shop') }}
            {% elif g.get('lang') == 'de' %}
              {{ _('Shop besuchen') }}
            {% elif g.get('lang') == 'ru' %}
              {{ _('Перейти в магазин') }}
            {% else %}
              {{ _('Перейти до магазину') }}
            {% endif %}
          </a>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}

{% macro get_block_title(block) -%}
  {%- if g.get('lang') == 'en' and block.title_en %}
    {{ block.title_en|striptags }}
  {%- elif g.get('lang') == 'de' and block.title_de %}
    {{ block.title_de|striptags }}
  {%- elif g.get('lang') == 'ru' and block.title_ru %}
    {{ block.title_ru|striptags }}
  {%- elif g.get('lang') == 'ua' and block.title_ua %}
    {{ block.title_ua|striptags }}
  {%- else %}
    {{ block.title|striptags or '' }}
  {%- endif %}
{%- endmacro %}

{% macro get_block_content(block) -%}
  {%- if g.get('lang') == 'en' and block.content_en %}
    {{ block.content_en }}
  {%- elif g.get('lang') == 'de' and block.content_de %}
    {{ block.content_de }}
  {%- elif g.get('lang') == 'ru' and block.content_ru %}
    {{ block.content_ru }}
  {%- elif g.get('lang') == 'ua' and block.content_ua %}
    {{ block.content_ua }}
  {%- else %}
    {{ block.content or '' }}
  {%- endif %}
{%- endmacro %}

{% macro get_blog_block_title(block) -%}
  {# Используем фильтр striptags для удаления HTML-тегов #}
  {%- if g.get('lang') == 'en' and block.title_en %}
    {{ block.title_en|striptags }}
  {%- elif g.get('lang') == 'de' and block.title_de %}
    {{ block.title_de|striptags }}
  {%- elif g.get('lang') == 'ru' and block.title_ru %}
    {{ block.title_ru|striptags }}
  {%- else %}
    {{ block.title|striptags or '' }}
  {%- endif %}
{%- endmacro %}

{% macro get_blog_block_summary(block) -%}
  {# Используем фильтр striptags для удаления HTML-тегов #}
  {%- if g.get('lang') == 'en' and block.summary_en %}
    {{ block.summary_en|striptags }}
  {%- elif g.get('lang') == 'de' and block.summary_de %}
    {{ block.summary_de|striptags }}
  {%- elif g.get('lang') == 'ru' and block.summary_ru %}
    {{ block.summary_ru|striptags }}
  {%- else %}
    {{ block.summary|striptags or '' }}
  {%- endif %}
{%- endmacro %}

{% macro get_blog_block_content(block) -%}
  {%- if g.get('lang') == 'en' and block.content_en %}
    {{ block.content_en }}
  {%- elif g.get('lang') == 'de' and block.content_de %}
    {{ block.content_de }}
  {%- elif g.get('lang') == 'ru' and block.content_ru %}
    {{ block.content_ru }}
  {%- else %}
    {{ block.content or '' }}
  {%- endif %}
{%- endmacro %}"""

    # Write the fixed template content
    with open(template_path, 'w', encoding='utf-8') as file:
        file.write(fixed_content)
    
    print(f"Fixed template syntax in: {template_path}")

if __name__ == "__main__":
    fix_template_syntax()
