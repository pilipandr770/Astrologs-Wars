from app import create_app, db
from app.models import BlogBlock

app = create_app()

with app.app_context():
    blocks = BlogBlock.query.all()
    print(f'Всего блоков блога: {len(blocks)}')
    print('Позиции опубликованных блоков:', [b.position for b in blocks])
    
    # Выводим подробную информацию о блоках
    print("\nПодробная информация о блоках:")
    for block in blocks:
        print(f"Позиция: {block.position}, Название: {block.title}, Обновлено: {block.updated_at}")
        print(f"Есть изображение: {'Да' if block.featured_image else 'Нет'}")
        print(f"Переводы: EN: {'Есть' if block.content_en else 'Нет'}, DE: {'Есть' if block.content_de else 'Нет'}, RU: {'Есть' if block.content_ru else 'Нет'}")
        print("-" * 50)
