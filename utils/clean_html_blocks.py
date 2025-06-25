"""
Скрипт для очистки существующих блогов от HTML обрамления.
Это предотвратит мерцание блоков на странице.
"""
import re
import logging
from app import create_app, db
from app.models import BlogBlock

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("clean_html_blocks.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("html_cleaner")

def clean_html_wrapper(html_content):
    """
    Очищает HTML-контент от обрамляющих тегов DOCTYPE, html, head, body
    чтобы предотвратить мерцание и дрижание блоков при рендере.
    """
    if not html_content:
        return html_content
        
    # Удаляем DOCTYPE
    content = re.sub(r'<!DOCTYPE[^>]*>', '', html_content)
    # Удаляем открывающий html тег
    content = re.sub(r'<html[^>]*>', '', content)
    # Удаляем закрывающий html тег
    content = re.sub(r'</html>', '', content)
    # Удаляем тег head с содержимым
    content = re.sub(r'<head>.*?</head>', '', content, flags=re.DOTALL)
    # Удаляем открывающий body тег
    content = re.sub(r'<body[^>]*>', '', content)
    # Удаляем закрывающий body тег
    content = re.sub(r'</body>', '', content)
    
    # Удаляем лишние пробелы и переносы строк
    content = re.sub(r'^\s+', '', content)
    content = re.sub(r'\s+$', '', content)
    
    return content

def clean_all_blogs():
    """Очищает все блоги от обрамляющих HTML-тегов"""
    blogs = BlogBlock.query.all()
    logger.info(f"Найдено {len(blogs)} блогов для очистки")
    
    for blog in blogs:
        logger.info(f"Обрабатываем блог ID: {blog.id}, позиция: {blog.position}")
        
        # Основной контент
        if blog.content:
            blog.content = clean_html_wrapper(blog.content)
            logger.info(f"Очищен основной контент блога {blog.id}")
        
        # Украинский контент
        if blog.content_ua:
            blog.content_ua = clean_html_wrapper(blog.content_ua)
            logger.info(f"Очищен украинский контент блога {blog.id}")
        
        # Английский контент
        if blog.content_en:
            blog.content_en = clean_html_wrapper(blog.content_en)
            logger.info(f"Очищен английский контент блога {blog.id}")
        
        # Немецкий контент
        if blog.content_de:
            blog.content_de = clean_html_wrapper(blog.content_de)
            logger.info(f"Очищен немецкий контент блога {blog.id}")
        
        # Русский контент
        if blog.content_ru:
            blog.content_ru = clean_html_wrapper(blog.content_ru)
            logger.info(f"Очищен русский контент блога {blog.id}")
    
    # Сохраняем изменения в базе данных
    db.session.commit()
    logger.info("Все блоги успешно очищены от HTML обрамления")
    return len(blogs)

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print("Начинаем процесс очистки HTML в блогах...")
        count = clean_all_blogs()
        print(f"Очистка завершена. Обработано блогов: {count}")
