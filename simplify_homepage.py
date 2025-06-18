#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для обновления главной страницы - один информационный блок и магазин
"""

import os
import sys
from pathlib import Path
import shutil

def create_project_info_css():
    """Создает CSS для информационного блока на главной странице"""
    css_path = Path('app/static/css/main-block.css')
    os.makedirs(os.path.dirname(css_path), exist_ok=True)
    
    css_content = """/* Стили для главной страницы с одним блоком */
.main-info-block {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 3rem 0;
  margin-bottom: 2rem;
}

.content-card {
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 2.5rem;
  transition: all 0.3s ease;
  height: 100%;
}

.content-card:hover {
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
}

.content-image {
  max-height: 300px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 2rem;
}

.content-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #333;
}

.content-body {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #444;
}

.shop-section {
  background-color: #f8f9fa;
  padding: 3rem 0;
  border-radius: 15px;
  margin-bottom: 3rem;
}

.shop-title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  text-align: center;
}

.shop-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  transition: all 0.3s ease;
  height: 100%;
}

.shop-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.shop-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.shop-card h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.shop-card p {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.shop-button {
  font-weight: 600;
  padding: 0.7rem 2rem;
  border-radius: 50px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.shop-button:hover {
  transform: scale(1.05);
}

@media (max-width: 768px) {
  .content-card {
    padding: 1.5rem;
  }
  
  .content-title {
    font-size: 1.8rem;
  }
  
  .shop-section {
    padding: 2rem 0;
  }
}"""
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"✓ CSS файл создан: {css_path}")
    return True

def update_base_html():
    """Обновляет базовый шаблон, добавляя ссылку на CSS"""
    base_path = Path('app/templates/base.html')
    
    if not base_path.exists():
        print(f"✗ Базовый шаблон не найден: {base_path}")
        return False
    
    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, подключен ли CSS файл
    if '{{ url_for(\'static\', filename=\'css/main-block.css\') }}' in content:
        print("✓ CSS файл уже подключен в базовом шаблоне")
        return True
    
    # Ищем место для вставки нового CSS файла
    css_marker = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/button_alignment.css\') }}">'
    
    if css_marker not in content:
        print("✗ Не найдено место для вставки CSS файла в базовом шаблоне")
        return False
    
    # Добавляем CSS файл после существующего CSS
    updated_content = content.replace(
        css_marker,
        f"{css_marker}\n    <link rel=\"stylesheet\" href=\"{{{{ url_for('static', filename='css/main-block.css') }}}}\">")
    
    with open(base_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✓ Базовый шаблон обновлен: {base_path}")
    return True

def update_index_html():
    """Обновляет шаблон главной страницы"""
    template_path = Path('app/templates/index.html')
    
    if not template_path.exists():
        print(f"✗ Шаблон главной страницы не найден: {template_path}")
        return False
    
    new_template = """{% extends 'base.html' %}
{% block title %}{{ _('Головна') }}{% endblock %}

{% block content %}
<!-- Основной информационный блок -->
<section class="main-info-block">
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="content-card">
          {% if top_block %}
            {% if top_block.image %}
              <img src="{{ url_for('static', filename='uploads/' ~ top_block.image) }}" 
                   alt="{{ get_block_title(top_block) }}" class="img-fluid content-image">
            {% endif %}
            <h1 class="content-title">{{ get_block_title(top_block) }}</h1>
            <div class="content-body">{{ get_block_content(top_block)|safe }}</div>
          {% else %}
            <h1 class="content-title text-center mb-4">
              {% if g.get('lang') == 'en' %}
                {{ _('Welcome to our Astrology Portal') }}
              {% elif g.get('lang') == 'de' %}
                {{ _('Willkommen auf unserem Astrologie-Portal') }}
              {% elif g.get('lang') == 'ru' %}
                {{ _('Добро пожаловать на наш астрологический портал') }}
              {% else %}
                {{ _('Ласкаво просимо до нашого астрологічного порталу') }}
              {% endif %}
            </h1>
            <div class="content-body text-center">
              <p>
                {% if g.get('lang') == 'en' %}
                  {{ _('Discover your destiny through professional astrological forecasts and analyses.') }}
                {% elif g.get('lang') == 'de' %}
                  {{ _('Entdecken Sie Ihr Schicksal durch professionelle astrologische Vorhersagen und Analysen.') }}
                {% elif g.get('lang') == 'ru' %}
                  {{ _('Откройте свою судьбу с помощью профессиональных астрологических прогнозов и анализов.') }}
                {% else %}
                  {{ _('Відкрийте свою долю за допомогою професійних астрологічних прогнозів та аналізів.') }}
                {% endif %}
              </p>
            </div>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Секция магазина -->
<section class="shop-section">
  <div class="container">
    <h2 class="shop-title">
      {% if g.get('lang') == 'en' %}
        {{ _('Astrology Shop') }}
      {% elif g.get('lang') == 'de' %}
        {{ _('Astrologie-Shop') }}
      {% elif g.get('lang') == 'ru' %}
        {{ _('Астрологический магазин') }}
      {% else %}
        {{ _('Астрологічний магазин') }}
      {% endif %}
    </h2>
    
    <div class="row">
      {% if featured_products and featured_products|length > 0 %}
        {% for product in featured_products[:3] %}
          <div class="col-md-4 mb-4">
            <div class="shop-card">
              {% if product.image %}
                <img src="{{ url_for('static', filename='uploads/products/' + product.image) }}" 
                     alt="{{ get_product_name(product) }}" class="img-fluid">
              {% endif %}
              <h3>{{ get_product_name(product) }}</h3>
              <p>{{ get_product_description(product)|truncate(100)|safe }}</p>
              <div class="text-center">
                <a href="{{ url_for('shop.product_detail', product_id=product.id) }}" class="btn btn-primary shop-button">
                  {% if g.get('lang') == 'en' %}
                    {{ _('View Details') }}
                  {% elif g.get('lang') == 'de' %}
                    {{ _('Details anzeigen') }}
                  {% elif g.get('lang') == 'ru' %}
                    {{ _('Подробнее') }}
                  {% else %}
                    {{ _('Детальніше') }}
                  {% endif %}
                </a>
              </div>
            </div>
          </div>
        {% endfor %}
      {% else %}
        <div class="col-12 text-center">
          <p class="lead">
            {% if g.get('lang') == 'en' %}
              {{ _('Discover our personalized astrological services') }}
            {% elif g.get('lang') == 'de' %}
              {{ _('Entdecken Sie unsere personalisierten astrologischen Dienstleistungen') }}
            {% elif g.get('lang') == 'ru' %}
              {{ _('Откройте для себя наши персонализированные астрологические услуги') }}
            {% else %}
              {{ _('Відкрийте для себе наші персоналізовані астрологічні послуги') }}
            {% endif %}
          </p>
        </div>
      {% endif %}
    </div>
    
    <div class="text-center mt-4">
      <a href="{{ url_for('shop.index') }}" class="btn btn-lg btn-primary shop-button">
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
</section>
{% endblock %}"""
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(new_template)
    
    print(f"✓ Шаблон главной страницы обновлен: {template_path}")
    return True

def update_routes_py():
    """Обновляет маршрут главной страницы в routes.py"""
    routes_path = Path('app/main/routes.py')
    
    if not routes_path.exists():
        print(f"✗ Файл маршрутов не найден: {routes_path}")
        return False
    
    new_index_route = """@main.route('/')
def index():
    """Головна сторінка з одним інформаційним блоком і секцією магазина"""
    # Получаем главный блок (is_top=True)
    top_block = Block.query.filter_by(is_active=True, is_top=True).first()
    
    # Получаем популярные продукты для секции магазина
    featured_products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(3).all()
    
    # Передаем только нужные данные и функции в шаблон
    return render_template('index.html', 
                           top_block=top_block,
                           featured_products=featured_products,
                           get_block_title=get_block_title,
                           get_block_content=get_block_content,
                           get_product_name=get_product_name,
                           get_product_description=get_product_description)
"""
    
    # Создаем временный файл для обновленного содержимого
    with open(routes_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Ищем начало и конец функции index()
    start_idx = None
    end_idx = None
    
    for i, line in enumerate(lines):
        if "@main.route('/')" in line:
            start_idx = i
        elif start_idx is not None and start_idx != i and "@main.route" in line:
            end_idx = i
            break
    
    if start_idx is not None:
        if end_idx is None:  # Если это последняя функция в файле
            end_idx = len(lines)
        
        # Создаем новый список строк с заменой функции index()
        new_lines = lines[:start_idx] + [new_index_route] + lines[end_idx:]
        
        # Записываем обновленный файл
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"✓ Маршрут главной страницы обновлен: {routes_path}")
        return True
    else:
        print("✗ Не найден маршрут главной страницы в файле routes.py")
        return False

def main():
    """Основная функция скрипта"""
    print("📄 Обновление главной страницы - один блок и секция магазина")
    
    # Проверяем, находимся ли мы в корне проекта
    if not Path('app').exists():
        # Проверяем, является ли текущая директория work-site
        if os.path.basename(os.getcwd()) != 'work-site' and Path('work-site').exists():
            os.chdir('work-site')
    
    success = True
    
    # Создаем CSS файл
    if not create_project_info_css():
        success = False
    
    # Обновляем базовый шаблон
    if not update_base_html():
        success = False
    
    # Обновляем шаблон главной страницы
    if not update_index_html():
        success = False
    
    # Обновляем маршрут главной страницы
    if not update_routes_py():
        success = False
    
    if success:
        print("✅ Обновление главной страницы завершено успешно!")
        print("\nТеперь главная страница:")
        print("✓ Содержит один информационный блок, редактируемый в админке")
        print("✓ Включает секцию магазина с популярными товарами")
        print("✓ Поддерживает многоязычность (UK, EN, RU, DE)")
        print("✓ Имеет современный и привлекательный дизайн")
    else:
        print("⚠️ Обновление завершено с ошибками. Проверьте вывод выше.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
