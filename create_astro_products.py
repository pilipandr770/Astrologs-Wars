from app import create_app, db
from app.models import Category, Product
import uuid
import os

app = create_app()

# Создаем пример астрологической категории и продукта
with app.app_context():
    # Проверяем, есть ли категория "Персональные гороскопы"
    astro_category = Category.query.filter_by(name="Персональные гороскопы").first()
    if not astro_category:
        # Создаем категорию
        astro_category = Category(
            name="Персональные гороскопы",
            name_en="Personal Horoscopes",
            name_de="Persönliche Horoskope",
            name_ru="Персональные гороскопы",
            name_ua="Персональні гороскопи",
            slug="personal-horoscopes",
            description="Индивидуальные астрологические прогнозы, составленные профессиональными астрологами по вашей натальной карте",
            description_en="Individual astrological forecasts created by professional astrologers based on your natal chart",
            description_de="Individuelle astrologische Vorhersagen, erstellt von professionellen Astrologen basierend auf Ihrem Geburtshoroskop",
            description_ru="Индивидуальные астрологические прогнозы, составленные профессиональными астрологами по вашей натальной карте",
            description_ua="Індивідуальні астрологічні прогнози, складені професійними астрологами за вашою натальною картою",
            is_active=True,
            order=1
        )
        db.session.add(astro_category)
        db.session.commit()
        print(f"Создана категория: {astro_category.name}")

    # Создаем продукты для категории, если их нет
    products_data = [
        {
            "name": "Личный гороскоп на месяц",
            "name_en": "Personal Monthly Horoscope",
            "name_ru": "Личный гороскоп на месяц",
            "name_ua": "Особистий гороскоп на місяць",
            "slug": "monthly-horoscope",
            "description": "Подробный прогноз на месяц, учитывающий аспекты планет, транзиты и прогрессии вашей натальной карты. Включает анализ всех сфер жизни: карьера, финансы, отношения, здоровье.",
            "description_en": "Detailed forecast for the month, taking into account the aspects of planets, transits and progressions of your natal chart. Includes analysis of all areas of life: career, finances, relationships, health.",
            "description_ru": "Подробный прогноз на месяц, учитывающий аспекты планет, транзиты и прогрессии вашей натальной карты. Включает анализ всех сфер жизни: карьера, финансы, отношения, здоровье.",
            "description_ua": "Детальний прогноз на місяць, що враховує аспекти планет, транзити та прогресії вашої натальної карти. Включає аналіз усіх сфер життя: кар'єра, фінанси, стосунки, здоров'я.",
            "price": 29.99,
            "features": ["Полный анализ основных событий месяца", "Рекомендации по благоприятным дням", "Предупреждения о сложных периодах", "Индивидуальный подход", "Формат PDF", "Консультация со специалистом"],
            "image_name": "monthly_horoscope.jpg"
        },
        {
            "name": "Натальная карта с интерпретацией",
            "name_en": "Natal Chart with Interpretation",
            "name_ru": "Натальная карта с интерпретацией",
            "name_ua": "Натальна карта з інтерпретацією",
            "slug": "natal-chart",
            "description": "Полный разбор вашей натальной карты с детальным описанием положения планет, домов и аспектов. Анализ вашего характера, талантов, потенциальных вызовов и рекомендации по самореализации.",
            "description_en": "Complete analysis of your natal chart with a detailed description of the positions of planets, houses and aspects. Analysis of your character, talents, potential challenges and recommendations for self-realization.",
            "description_ru": "Полный разбор вашей натальной карты с детальным описанием положения планет, домов и аспектов. Анализ вашего характера, талантов, потенциальных вызовов и рекомендации по самореализации.",
            "description_ua": "Повний розбір вашої натальної карти з детальним описом положення планет, будинків і аспектів. Аналіз вашого характеру, талантів, потенційних викликів та рекомендації щодо самореалізації.",
            "price": 49.99,
            "features": ["Подробная 20-30 страничная интерпретация", "Графическое изображение натальной карты", "Анализ карьерной предрасположенности", "Разбор любовной совместимости", "Консультация со специалистом", "Формат PDF с иллюстрациями"],
            "image_name": "natal_chart.jpg"
        },
        {
            "name": "Годовой прогноз по всем сферам жизни",
            "name_en": "Annual Forecast for All Life Areas",
            "name_ru": "Годовой прогноз по всем сферам жизни",
            "name_ua": "Річний прогноз по всіх сферах життя",
            "slug": "annual-forecast",
            "description": "Комплексный прогноз на год, раскрывающий тенденции и важные события во всех сферах жизни. Поможет спланировать год, избежать ошибок и использовать благоприятные периоды для достижения целей.",
            "description_en": "Comprehensive forecast for the year, revealing trends and important events in all areas of life. Will help plan the year, avoid mistakes and use favorable periods to achieve goals.",
            "description_ru": "Комплексный прогноз на год, раскрывающий тенденции и важные события во всех сферах жизни. Поможет спланировать год, избежать ошибок и использовать благоприятные периоды для достижения целей.",
            "description_ua": "Комплексний прогноз на рік, що розкриває тенденції та важливі події в усіх сферах життя. Допоможе спланувати рік, уникнути помилок і використовувати сприятливі періоди для досягнення цілей.",
            "price": 99.99,
            "features": ["Прогноз по месяцам", "Анализ ключевых событий года", "Рекомендации по карьере и финансам", "Анализ личной жизни и отношений", "Индивидуальная карта года", "Две консультации со специалистом"],
            "image_name": "annual_forecast.jpg"
        }
    ]

    for prod_data in products_data:
        # Проверяем, существует ли уже такой продукт
        product = Product.query.filter_by(slug=prod_data["slug"]).first()
        if not product:
            # Создание продукта
            product = Product(
                name=prod_data["name"],
                name_en=prod_data["name_en"],
                name_ru=prod_data["name_ru"],
                name_ua=prod_data["name_ua"],
                slug=prod_data["slug"],
                description=prod_data["description"],
                description_en=prod_data["description_en"],
                description_ru=prod_data["description_ru"],
                description_ua=prod_data["description_ua"],
                category_id=astro_category.id,
                price=prod_data["price"],
                features=prod_data["features"],
                is_active=True,
                is_digital=True
            )
            
            # Загрузка заглушки для изображения (здесь можно было бы создать реальное изображение)
            filename = f"{str(uuid.uuid4())}.jpg"
            # Просто сохраняем имя файла, в реальности нужно бы создать файл
            product.image = filename
            
            db.session.add(product)
            db.session.commit()
            print(f"Создан продукт: {product.name}")
        else:
            print(f"Продукт {prod_data['name']} уже существует")

    print("Готово! Астрологические услуги добавлены в магазин.")
