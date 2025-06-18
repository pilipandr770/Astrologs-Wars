#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для обновления главной страницы на простой информационный блок
Работает как в локальной среде, так и на Render
"""

import os
import sys
from pathlib import Path
import shutil

def update_main_route():
    """Обновляет маршрут главной страницы в app/main/routes.py"""
    routes_path = Path('app/main/routes.py')
    
    if not routes_path.exists():
        print(f"✗ Файл маршрутов не найден: {routes_path}")
        return False
    
    # Читаем файл routes.py
    with open(routes_path, 'r', encoding='utf-8') as f:
        content = f.read()    # Используем более простой подход с поиском вместо сложной регулярки
    old_index_header = '@main.route(\'/\')\ndef index():'
    old_index_return = 'return render_template(\'index.html\', blocks=blocks, settings=settings'
    
    new_index_route = r"""@main.route('/')
def index():
    """Головна сторінка з інформацією про проект"""
    # Получаем только главный блок (is_top=True) - информационный блок о проекте
    top_block = Block.query.filter_by(is_active=True, is_top=True).first()
    
    # Обязательно передаем вспомогательные функции для локализации
    return render_template('index.html', 
                           top_block=top_block,
                           get_block_title=get_block_title,
                           get_block_content=get_block_content)"""
      # Используем поиск по маркерам
    start_marker = old_index_header
    
    if start_marker in content:
        # Находим начало функции index()
        start_idx = content.find(start_marker)
        
        # Ищем следующую функцию или конец файла
        next_func = content.find("@main.route", start_idx + len(start_marker))
        if next_func == -1:
            # Если следующей функции нет, берем до конца файла
            end_idx = len(content)
        else:
            end_idx = next_func
        
        # Заменяем только найденный раздел
        updated_content = content[:start_idx] + new_index_route + content[end_idx:]
        
        # Записываем обновленный файл routes.py
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"✓ Маршрут главной страницы обновлен: {routes_path}")
        return True
    else:
        print("✗ Не удалось найти маршрут главной страницы")
        return False

def update_index_template():
    """Обновляет шаблон главной страницы"""
    template_path = Path('app/templates/index.html')
    
    if not template_path.exists():
        print(f"✗ Шаблон не найден: {template_path}")
        return False
    
    # Новый контент для шаблона
    new_template = """{% extends 'base.html' %}
{% block title %}{{ _('Головна') }}{% endblock %}

{% block content %}
<div class="project-info-section">
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="project-info-card">
          {% if top_block %}
          <div class="text-center mb-4">
            {% if top_block.image %}
            <img src="{{ url_for('static', filename='uploads/' ~ top_block.image) }}" alt="{{ get_block_title(top_block) }}" class="project-logo img-fluid mb-4">
            {% endif %}
            <h1 class="display-4 mb-3">{{ get_block_title(top_block) }}</h1>
          </div>
          <div class="project-description">
            {{ get_block_content(top_block)|safe }}
          </div>
          {% else %}
          <div class="text-center mb-4">
            <h1 class="display-4 mb-3">
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
          <div class="project-description">
            <p class="lead text-center mb-4">
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

          <div class="row mt-5">
            <div class="col-md-6 mb-4">
              <div class="feature-card">
                <i class="fas fa-star-half-alt mb-3"></i>
                <h3>
                  {% if g.get('lang') == 'en' %}
                    {{ _('Daily Horoscopes') }}
                  {% elif g.get('lang') == 'de' %}
                    {{ _('Tägliche Horoskope') }}
                  {% elif g.get('lang') == 'ru' %}
                    {{ _('Ежедневные гороскопы') }}
                  {% else %}
                    {{ _('Щоденні гороскопи') }}
                  {% endif %}
                </h3>
                <p>
                  {% if g.get('lang') == 'en' %}
                    {{ _('Check your daily horoscope based on different astrological systems.') }}
                  {% elif g.get('lang') == 'de' %}
                    {{ _('Überprüfen Sie Ihr tägliches Horoskop basierend auf verschiedenen astrologischen Systemen.') }}
                  {% elif g.get('lang') == 'ru' %}
                    {{ _('Проверьте свой ежедневный гороскоп на основе различных астрологических систем.') }}
                  {% else %}
                    {{ _('Перевірте свій щоденний гороскоп на основі різних астрологічних систем.') }}
                  {% endif %}
                </p>
                <a href="{{ url_for('blog.index') }}" class="btn btn-primary">
                  {% if g.get('lang') == 'en' %}
                    {{ _('View Horoscopes') }}
                  {% elif g.get('lang') == 'de' %}
                    {{ _('Horoskope anzeigen') }}
                  {% elif g.get('lang') == 'ru' %}
                    {{ _('Смотреть гороскопы') }}
                  {% else %}
                    {{ _('Переглянути гороскопи') }}
                  {% endif %}
                </a>
              </div>
            </div>
            
            <div class="col-md-6 mb-4">
              <div class="feature-card">
                <i class="fas fa-shopping-cart mb-3"></i>
                <h3>
                  {% if g.get('lang') == 'en' %}
                    {{ _('Astrological Shop') }}
                  {% elif g.get('lang') == 'de' %}
                    {{ _('Astrologischer Shop') }}
                  {% elif g.get('lang') == 'ru' %}
                    {{ _('Астрологический магазин') }}
                  {% else %}
                    {{ _('Астрологічний магазин') }}
                  {% endif %}
                </h3>
                <p>
                  {% if g.get('lang') == 'en' %}
                    {{ _('Purchase personal forecasts, birth charts, and compatibility analyses.') }}
                  {% elif g.get('lang') == 'de' %}
                    {{ _('Kaufen Sie persönliche Prognosen, Geburtshoroskope und Kompatibilitätsanalysen.') }}
                  {% elif g.get('lang') == 'ru' %}
                    {{ _('Приобретайте персональные прогнозы, натальные карты и анализы совместимости.') }}
                  {% else %}
                    {{ _('Придбайте персональні прогнози, натальні карти та аналізи сумісності.') }}
                  {% endif %}
                </p>
                <a href="{{ url_for('shop.index') }}" class="btn btn-primary">
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
    </div>
  </div>
</div>
{% endblock %}"""
    
    # Записываем новый шаблон
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(new_template)
    
    print(f"✓ Шаблон главной страницы обновлен: {template_path}")
    return True

def create_project_info_css():
    """Создает файл CSS для информационного блока о проекте"""
    css_path = Path('app/static/css/project-info.css')
    
    # Если директория не существует, создаем ее
    css_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Содержимое CSS файла
    css_content = """/* Стили для информационного блока о проекте на главной странице */
.project-info-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  padding: 3rem 0;
}

.project-info-card {
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.project-info-card:hover {
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
}

.project-logo {
  max-height: 200px;
  margin-bottom: 2rem;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.project-description {
  font-size: 1.1rem;
  color: #444;
  line-height: 1.8;
  margin-bottom: 2rem;
}

.project-description p {
  margin-bottom: 1.2rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.feature-card i {
  font-size: 2.5rem;
  color: #6a11cb;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.4rem;
  margin-bottom: 1rem;
  color: #333;
}

.feature-card p {
  color: #666;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.feature-card .btn {
  align-self: center;
  padding: 0.5rem 1.5rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .project-info-card {
    padding: 2rem;
  }
  
  .project-description {
    font-size: 1rem;
  }
  
  .feature-card {
    padding: 1.2rem;
    margin-bottom: 1rem;
  }
}"""
    
    # Записываем CSS файл
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"✓ CSS файл создан: {css_path}")
    return True

def update_base_template():
    """Обновляет базовый шаблон, добавляя ссылку на CSS файл проекта"""
    base_path = Path('app/templates/base.html')
    
    if not base_path.exists():
        print(f"✗ Базовый шаблон не найден: {base_path}")
        return False
    
    # Читаем базовый шаблон
    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, подключен ли CSS файл проекта
    if '{{ url_for(\'static\', filename=\'css/project-info.css\') }}' in content:
        print("✓ CSS файл проекта уже подключен в базовом шаблоне")
        return True
    
    # Ищем место для вставки нового CSS файла
    css_marker = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/horoscope-blocks.css\') }}">'
    
    if css_marker not in content:
        print("✗ Не найдено место для вставки CSS файла проекта в базовом шаблоне")
        return False
    
    # Добавляем CSS файл проекта после CSS файла блоков гороскопа
    updated_content = content.replace(
        css_marker,
        f"{css_marker}\n    <link rel=\"stylesheet\" href=\"{{{{ url_for('static', filename='css/project-info.css') }}}}\">")
    
    # Записываем обновленный базовый шаблон
    with open(base_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✓ Базовый шаблон обновлен: {base_path}")
    return True

def main():
    """Основная функция скрипта"""
    print("📄 Обновление главной страницы на информационный блок о проекте")
    
    # Проверяем, находимся ли мы в корне проекта
    if not Path('app').exists():
        # Проверяем, является ли текущая директория work-site
        if Path('..').resolve().name == 'work-site':
            os.chdir('..')
        # Если мы в astrolog_wars, перейдем в work-site
        elif Path('work-site').exists():
            os.chdir('work-site')
    
    success = True
    
    # Создаем CSS файл проекта
    if not create_project_info_css():
        success = False
    
    # Обновляем шаблон базовой страницы
    if not update_base_template():
        success = False
    
    # Обновляем шаблон главной страницы
    if not update_index_template():
        success = False
    
    # Обновляем маршрут главной страницы
    if not update_main_route():
        success = False
    
    if success:
        print("✅ Обновление главной страницы завершено успешно!")
        print("\nТеперь главная страница:")
        print("✓ Содержит информационный блок о проекте")
        print("✓ Имеет ссылки на разделы гороскопов и магазин")
        print("✓ Имеет современный и красивый дизайн")
        print("✓ Решена проблема с Jinja-шаблоном, вызывавшая ошибку на Render")
    else:
        print("⚠️ Обновление завершено с ошибками. Проверьте вывод выше.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
