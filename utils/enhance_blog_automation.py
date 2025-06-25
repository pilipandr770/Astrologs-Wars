"""
Скрипт для улучшения и настройки блога и его автоматизации.
"""

import os
import sys
from datetime import datetime
from app import create_app, db
from app.models import BlogBlock
from app.blog_automation.models import AutopostingSchedule, BlogTopic

app = create_app()

def enhance_blog_automation():
    """
    Улучшает настройки автоматизации блога:
    - Активирует расписание автопостинга
    - Настраивает частоту публикаций
    - Включает мультиязычный перевод
    - Настраивает генерацию изображений
    """
    with app.app_context():
        # Получаем текущие настройки или создаем новые
        schedule = AutopostingSchedule.query.first()
        if not schedule:
            schedule = AutopostingSchedule()
            db.session.add(schedule)
        
        # Активируем автопостинг
        schedule.is_active = True
        
        # Устанавливаем расписание на публикацию каждые 2 дня (пн,ср,пт)
        schedule.days_of_week = '0,2,4'  # 0=Monday, 2=Wednesday, 4=Friday
        
        # Устанавливаем время публикации на 10 утра
        schedule.posting_time = '10:00'
        
        # Включаем автоматический перевод
        schedule.auto_translate = True
        schedule.target_languages = 'en,de,ru'  # Все поддерживаемые языки
        
        # Включаем генерацию изображений
        schedule.generate_images = True
        schedule.image_style = 'professional, high quality, blog post, astrology'
        
        # Активируем публикацию в Telegram
        schedule.post_to_telegram = True
        
        db.session.commit()
        print("Настройки автоматизации блога обновлены!")

def add_sample_topics():
    """
    Добавляет примерные темы для генерации контента блога
    """
    topics = [
        "Астрологические прогнозы на неделю: что ждет каждый знак зодиака",
        "Влияние Луны на наше настроение и энергию: научное объяснение",
        "Ретроградный Меркурий: мифы и реальность",
        "Как планеты влияют на карьеру: астрология в профессиональной жизни",
        "Совместимость знаков зодиака: гармония в отношениях",
        "Дома гороскопа: что они значат и как влияют на нашу жизнь",
        "Восходящий знак и его влияние на личность",
        "Транзиты планет и их влияние на повседневную жизнь",
        "Астрология здоровья: связь между знаками зодиака и самочувствием",
        "Как составить персональный гороскоп: основы для начинающих"
    ]
    
    with app.app_context():
        for title in topics:
            # Проверяем, существует ли тема
            exists = BlogTopic.query.filter_by(title=title).first()
            if not exists:
                topic = BlogTopic(title=title)
                db.session.add(topic)
        
        db.session.commit()
        print(f"Добавлено {len(topics)} тем для блога!")

def update_blog_blocks():
    """
    Обновляет блоки блога для улучшения их отображения и функциональности
    """
    with app.app_context():
        blocks = BlogBlock.query.all()
        
        # Для каждого блока добавляем краткое описание, если его нет
        for block in blocks:
            if not block.summary:
                # Создаем краткое описание из первых 200 символов контента
                content_plain = block.content.replace('<p>', '').replace('</p>', ' ')
                summary = content_plain[:200] + '...' if len(content_plain) > 200 else content_plain
                block.summary = summary
                
                # Обновляем также переводы
                for lang in ['en', 'de', 'ru']:
                    lang_content = getattr(block, f'content_{lang}')
                    if lang_content:
                        content_plain = lang_content.replace('<p>', '').replace('</p>', ' ')
                        summary = content_plain[:200] + '...' if len(content_plain) > 200 else content_plain
                        setattr(block, f'summary_{lang}', summary)
        
        db.session.commit()
        print(f"Обновлено {len(blocks)} блоков блога!")

if __name__ == "__main__":
    print("Улучшение блога и его автоматизации...")
    
    enhance_blog_automation()
    add_sample_topics()
    update_blog_blocks()
    
    print("Улучшения блога успешно выполнены!")
