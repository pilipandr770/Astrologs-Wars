"""
Скрипт для проверки отображения блоков блога без HTML-тегов на главной странице
"""
from app import create_app, db
from app.models import BlogBlock
from app.utils.text_utils import strip_html_tags
import requests
import re

def check_blog_html_tags():
    print("Проверка отображения блоков блога...")
    app = create_app()
    
    with app.app_context():
        # Получаем последние 7 блоков блога
        recent_blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).limit(7).all()
        
        print(f"Найдено {len(recent_blocks)} блоков блога\n")
        
        # Проверяем на наличие HTML-тегов в заголовках и описаниях
        for block in recent_blocks:
            print(f"Блок #{block.position}: {block.title}")
            
            # Проверяем заголовок
            if re.search(r'<[^>]+>', block.title):
                print(f"  Найдены HTML-теги в заголовке!")
                print(f"  Исходный заголовок: {block.title[:50]}...")
                print(f"  Очищенный заголовок: {strip_html_tags(block.title)[:50]}...")
            else:
                print(f"  Заголовок чист от HTML-тегов")
            
            # Проверяем описание
            if re.search(r'<[^>]+>', block.summary):
                print(f"  Найдены HTML-теги в описании!")
                print(f"  Исходное описание: {block.summary[:50]}...")
                print(f"  Очищенное описание: {strip_html_tags(block.summary)[:50]}...")
            else:
                print(f"  Описание чисто от HTML-тегов\n")
        
        print("\nВерификация завершена.")
        print("Теперь на главной странице блоки блога должны отображаться без HTML-тегов.")
        print("Проверьте главную страницу в браузере.")

if __name__ == "__main__":
    check_blog_html_tags()
