#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для обновления внешнего вида блоков гороскопов на главной странице
Обновляет CSS и шаблон для улучшения визуального представления
Работает как в локальной среде, так и на Render
"""

import os
import sys
import shutil
from pathlib import Path

def update_horoscope_blocks_css():
    """Обновляет CSS файл для блоков гороскопов"""
    css_path = Path('app/static/css/horoscope-blocks.css')
    
    # Если файл не существует, создаем его директорию
    css_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Создаем новый CSS контент
    css_content = """/* Стили для блоков гороскопов на главной странице */
.horoscope-block {
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12);
  padding: 20px;
  height: 100%;
  cursor: pointer;
  background-color: #fff;
  position: relative;
  overflow: hidden;
  min-height: 420px; /* Ensure consistent height */
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.horoscope-block:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.horoscope-block h3 {
  font-size: 1.25rem;
  margin-bottom: 12px;
  color: #222;
  font-weight: 600;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
  height: 2.8em; /* Fixed height for title - 2 lines */
}

.horoscope-block p {
  font-size: 1rem;
  color: #555;
  flex-grow: 1;
  margin-bottom: 20px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 4; /* Limit to 4 lines of text */
  line-clamp: 4;
  -webkit-box-orient: vertical;
  line-height: 1.5;
  max-height: 6em; /* 4 lines * 1.5 line height */
}

.horoscope-block img {
  border-radius: 8px;
  margin-bottom: 15px;
  height: 180px; /* Fixed consistent height */
  object-fit: cover;
  width: 100%;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.horoscope-block .btn {
  align-self: center;
  font-weight: 500;
  padding: 8px 20px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.horoscope-block .btn:hover {
  transform: scale(1.05);
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .horoscope-block {
    min-height: 380px;
    padding: 15px;
  }
  
  .horoscope-block img {
    height: 160px;
  }
  
  .horoscope-block h3 {
    font-size: 1.2rem;
  }
  
  .horoscope-block p {
    font-size: 0.9rem;
  }
}

/* Animation for blocks */
.row-cols-1 .col:nth-child(1) .horoscope-block { animation: fadeInUp 0.5s 0.1s both; }
.row-cols-1 .col:nth-child(2) .horoscope-block { animation: fadeInUp 0.5s 0.2s both; }
.row-cols-1 .col:nth-child(3) .horoscope-block { animation: fadeInUp 0.5s 0.3s both; }
.row-cols-1 .col:nth-child(4) .horoscope-block { animation: fadeInUp 0.5s 0.4s both; }
.row-cols-1 .col:nth-child(5) .horoscope-block { animation: fadeInUp 0.5s 0.5s both; }
.row-cols-1 .col:nth-child(6) .horoscope-block { animation: fadeInUp 0.5s 0.6s both; }
.row-cols-1 .col:nth-child(7) .horoscope-block { animation: fadeInUp 0.5s 0.7s both; }
.row-cols-1 .col:nth-child(8) .horoscope-block { animation: fadeInUp 0.5s 0.8s both; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Horoscope section styling */
.horoscope-section {
  background-color: #f8f9fa;
  border-radius: 16px;
  padding: 30px 15px;
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.horoscope-section:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, #8e44ad, #3498db);
}

.horoscope-section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 30px;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  display: inline-block;
}

.horoscope-section-title:after {
  content: '';
  position: absolute;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #3498db, #8e44ad);
  bottom: -10px;
  left: calc(50% - 30px);
  border-radius: 2px;
}"""

    # Записываем обновленный CSS
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"✓ CSS файл обновлен: {css_path}")
    return True

def update_index_template():
    """Обновляет шаблон index.html для улучшения отображения блоков гороскопов"""
    template_path = Path('app/templates/index.html')
    
    if not template_path.exists():
        print(f"✗ Шаблон не найден: {template_path}")
        return False
    
    # Читаем шаблон
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем секцию блоков гороскопов на обновленную версию
    old_section = r'''{# --- БЛОКИ ГОРОСКОПОВ --- #}
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
    
    new_section = r'''{# --- БЛОКИ ГОРОСКОПОВ --- #}
  {% if astrology_blocks %}
  <div class="horoscope-section mt-4 mb-5">
    <div class="container">
      <h2 class="text-center mb-4 horoscope-section-title">
        {% if g.get('lang') == 'en' %}
          {{ _('Daily Horoscopes') }}
        {% elif g.get('lang') == 'de' %}
          {{ _('Tägliche Horoskope') }}
        {% elif g.get('lang') == 'ru' %}
          {{ _('Ежедневные гороскопы') }}
        {% else %}
          {{ _('Щоденні гороскопи') }}
        {% endif %}
      </h2>
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
    </div>
  </div>
  {% endif %}'''
    
    # Если секция не найдена, пробуем искать другие варианты
    if old_section not in content:
        # Пробуем найти более общий шаблон для замены
        start_marker = '{# --- БЛОКИ ГОРОСКОПОВ --- #}'
        end_marker = '{% endif %}'
        
        start_pos = content.find(start_marker)
        if start_pos == -1:
            print("✗ Не найдена секция блоков гороскопов в шаблоне")
            return False
            
        # Ищем ближайший {% endif %} после начала секции
        end_pos = content.find(end_marker, start_pos)
        if end_pos == -1:
            print("✗ Не найдена конечная метка блока гороскопов")
            return False
            
        end_pos += len(end_marker)
        
        # Получаем весь фрагмент для замены
        fragment_to_replace = content[start_pos:end_pos]
        updated_content = content.replace(fragment_to_replace, new_section)
    else:
        # Используем стандартную замену, если секция найдена как есть
        updated_content = content.replace(old_section, new_section)
    
    # Записываем обновленный шаблон
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✓ Шаблон обновлен: {template_path}")
    return True

def verify_css_included():
    """Проверяет, что CSS файл подключен в базовом шаблоне"""
    base_template_path = Path('app/templates/base.html')
    
    if not base_template_path.exists():
        print(f"✗ Базовый шаблон не найден: {base_template_path}")
        return False
    
    # Читаем базовый шаблон
    with open(base_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, подключен ли наш CSS файл
    css_include = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/horoscope-blocks.css\') }}">'
    
    if css_include in content:
        print("✓ CSS файл уже подключен в базовом шаблоне")
        return True
    
    # Если CSS не подключен, ищем место для подключения
    css_section_marker = "{% block extra_css %}{% endblock %}"
    
    if css_section_marker not in content:
        print("✗ Невозможно найти место для вставки CSS в базовом шаблоне")
        return False
    
    # Добавляем подключение CSS перед блоком extra_css
    updated_content = content.replace(css_section_marker, 
                                    f'    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/horoscope-blocks.css\') }}">\n    {css_section_marker}')
    
    # Записываем обновленный базовый шаблон
    with open(base_template_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✓ CSS файл подключен в базовом шаблоне: {base_template_path}")
    return True

def main():
    """Основная функция скрипта"""
    print("📊 Обновление визуального представления блоков гороскопов на главной странице")
    
    # Проверяем, находимся ли мы в корне проекта
    if not Path('app').exists():
        # Проверяем, является ли текущая директория work-site
        if Path('..').resolve().name == 'work-site':
            os.chdir('..')
        # Если мы в astrolog_wars, перейдем в work-site
        elif Path('work-site').exists():
            os.chdir('work-site')
    
    success = True
    
    # Обновляем CSS файл
    if not update_horoscope_blocks_css():
        success = False
    
    # Обновляем шаблон
    if not update_index_template():
        success = False
    
    # Проверяем подключение CSS
    if not verify_css_included():
        success = False
    
    if success:
        print("✅ Обновление внешнего вида блоков гороскопов завершено успешно!")
        print("\nТеперь блоки гороскопов на главной странице имеют:")
        print("✓ Улучшенный внешний вид и единообразный размер")
        print("✓ Заголовок секции \"Щоденні гороскопи\"")
        print("✓ Правильную обрезку текста, если он слишком длинный")
        print("✓ Отзывчивый дизайн для мобильных устройств")
        print("✓ Анимацию появления блоков")
    else:
        print("⚠️ Обновление завершено с ошибками. Проверьте вывод выше.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
