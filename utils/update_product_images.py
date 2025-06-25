from app import create_app, db
from app.models import Product
import os
import glob

app = create_app()

with app.app_context():
    # Получаем все созданные изображения
    upload_dir = os.path.join(app.root_path, 'static', 'uploads')
    image_files = glob.glob(os.path.join(upload_dir, '*.jpg'))
    image_files = [os.path.basename(f) for f in image_files]
    
    # Распределяем изображения по продуктам
    products = Product.query.all()
    
    # Для каждого продукта устанавливаем изображение, если его нет
    for i, product in enumerate(products):
        if not product.image and i < len(image_files):
            product.image = image_files[i]
            print(f"Установлено изображение {image_files[i]} для продукта {product.name}")
    
    db.session.commit()
    print("Изображения успешно обновлены в базе данных!")
