"""
Скрипт для настройки блогов под разные астрологические системы
"""
import os
import sys
from datetime import datetime
from app import create_app, db
from app.models import BlogBlock

app = create_app()

ASTRO_SYSTEMS = [
    {
        'name': 'Європейська астрологія',
        'name_en': 'European Astrology',
        'name_de': 'Europäische Astrologie',
        'name_ru': 'Европейская астрология',
        'title': 'Щоденний гороскоп за європейською астрологією',
        'title_en': 'Daily Horoscope by European Astrology',
        'title_de': 'Tägliches Horoskop nach europäischer Astrologie',
        'title_ru': 'Ежедневный гороскоп по европейской астрологии',
        'content': 'Прогноз на сьогодні від європейської астрологічної системи. Дізнайтеся, що чекає на ваш знак зодіаку.',
        'content_en': 'Today\'s forecast from the European astrological system. Find out what awaits your zodiac sign.',
        'content_de': 'Die heutige Prognose aus dem europäischen astrologischen System. Finden Sie heraus, was Ihr Sternzeichen erwartet.',
        'content_ru': 'Прогноз на сегодня от европейской астрологической системы. Узнайте, что ждет ваш знак зодиака.'
    },
    {
        'name': 'Китайська астрологія',
        'name_en': 'Chinese Astrology',
        'name_de': 'Chinesische Astrologie',
        'name_ru': 'Китайская астрология',
        'title': 'Прогноз згідно китайської астрології',
        'title_en': 'Forecast According to Chinese Astrology',
        'title_de': 'Prognose nach chinesischer Astrologie',
        'title_ru': 'Прогноз согласно китайской астрологии',
        'content': 'Сьогоднішній прогноз базується на китайському календарі та системі тварин-покровителів.',
        'content_en': 'Today\'s forecast is based on the Chinese calendar and animal patron system.',
        'content_de': 'Die heutige Prognose basiert auf dem chinesischen Kalender und dem Tierpatronensystem.',
        'content_ru': 'Сегодняшний прогноз основан на китайском календаре и системе животных-покровителей.'
    },
    {
        'name': 'Індійська астрологія',
        'name_en': 'Indian Astrology',
        'name_de': 'Indische Astrologie',
        'name_ru': 'Индийская астрология',
        'title': 'Ведичний прогноз на сьогодні',
        'title_en': 'Vedic Forecast for Today',
        'title_de': 'Vedische Prognose für heute',
        'title_ru': 'Ведический прогноз на сегодня',
        'content': 'Прогноз на день згідно з традиційною індійською астрологією. Вплив планет на вашу долю.',
        'content_en': 'Daily forecast according to traditional Indian astrology. The influence of planets on your destiny.',
        'content_de': 'Tagesprognose nach traditioneller indischer Astrologie. Der Einfluss der Planeten auf Ihr Schicksal.',
        'content_ru': 'Прогноз на день согласно традиционной индийской астрологии. Влияние планет на вашу судьбу.'
    },
    {
        'name': 'Лал Кітаб',
        'name_en': 'Lal Kitab',
        'name_de': 'Lal Kitab',
        'name_ru': 'Лал Китаб',
        'title': 'Прогноз за системою Лал Кітаб',
        'title_en': 'Forecast According to Lal Kitab',
        'title_de': 'Prognose nach dem Lal Kitab-System',
        'title_ru': 'Прогноз по системе Лал Китаб',
        'content': 'Передбачення згідно з давньою індійською книгою Лал Кітаб, яка поєднує астрологію та народну мудрість.',
        'content_en': 'Predictions according to the ancient Indian book Lal Kitab, which combines astrology and folk wisdom.',
        'content_de': 'Vorhersagen nach dem alten indischen Buch Lal Kitab, das Astrologie und Volksweisheit kombiniert.',
        'content_ru': 'Предсказания согласно древней индийской книге Лал Китаб, которая сочетает астрологию и народную мудрость.'
    },
    {
        'name': 'Джйотіш',
        'name_en': 'Jyotish',
        'name_de': 'Jyotish',
        'name_ru': 'Джйотиш',
        'title': 'Денний прогноз Джйотіш',
        'title_en': 'Daily Jyotish Forecast',
        'title_de': 'Tägliche Jyotish-Prognose',
        'title_ru': 'Дневной прогноз Джйотиш',
        'content': 'Ведична астрологія Джйотіш розкриває глибинний вплив космічних сил на ваше життя.',
        'content_en': 'Vedic astrology Jyotish reveals the deep influence of cosmic forces on your life.',
        'content_de': 'Die vedische Astrologie Jyotish enthüllt den tiefgreifenden Einfluss kosmischer Kräfte auf Ihr Leben.',
        'content_ru': 'Ведическая астрология Джйотиш раскрывает глубинное влияние космических сил на вашу жизнь.'
    },
    {
        'name': 'Нумерологія',
        'name_en': 'Numerology',
        'name_de': 'Numerologie',
        'name_ru': 'Нумерология',
        'title': 'Нумерологічний прогноз дня',
        'title_en': 'Numerological Forecast of the Day',
        'title_de': 'Numerologische Prognose des Tages',
        'title_ru': 'Нумерологический прогноз дня',
        'content': 'Пізнайте вплив чисел на події дня. Нумерологія розкриває приховану гармонію світу.',
        'content_en': 'Discover the influence of numbers on the events of the day. Numerology reveals the hidden harmony of the world.',
        'content_de': 'Entdecken Sie den Einfluss von Zahlen auf die Ereignisse des Tages. Numerologie enthüllt die verborgene Harmonie der Welt.',
        'content_ru': 'Познайте влияние чисел на события дня. Нумерология раскрывает скрытую гармонию мира.'
    },
    {
        'name': 'Таро',
        'name_en': 'Tarot',
        'name_de': 'Tarot',
        'name_ru': 'Таро',
        'title': 'Таро-прогноз на сьогодні',
        'title_en': 'Tarot Forecast for Today',
        'title_de': 'Tarot-Prognose für heute',
        'title_ru': 'Таро-прогноз на сегодня',        'content': 'Карти Таро відкривають таємниці дня та підказують оптимальні рішення в різних ситуаціях.',
        'content_en': 'Tarot cards reveal the secrets of the day and suggest optimal solutions in different situations.',
        'content_de': 'Tarotkarten enthüllen die Geheimnisse des Tages und schlagen optimale Lösungen in verschiedenen Situationen vor.',
        'content_ru': 'Карты Таро раскрывают тайны дня и подсказывают оптимальные решения в различных ситуациях.'
    },
    {
        'name': 'Планетарна астрологія',
        'name_en': 'Planetary Astrology',
        'name_de': 'Planetenastrologie',
        'name_ru': 'Планетарная астрология',
        'title': 'Прогноз планетарної астрології на сьогодні',
        'title_en': 'Planetary Astrology Forecast for Today',
        'title_de': 'Planetenastrologie-Prognose für heute',
        'title_ru': 'Прогноз планетарной астрологии на сегодня',
        'content': 'Детальний аналіз розташування та аспектів планет, їх вплив на енергетичний фон дня та ваше життя.',
        'content_en': 'Detailed analysis of the position and aspects of planets, their influence on the energy background of the day and your life.',
        'content_de': 'Detaillierte Analyse der Stellung und Aspekte der Planeten, ihr Einfluss auf den energetischen Hintergrund des Tages und Ihr Leben.',
        'content_ru': 'Детальный анализ расположения и аспектов планет, их влияние на энергетический фон дня и вашу жизнь.'
    }
]

def setup_astro_blogs():
    """Настраивает блоги под разные астрологические системы"""
    with app.app_context():
        print("Настройка блогов под разные астрологические системы...")
          # Получаем существующие блоги
        existing_blogs = BlogBlock.query.all()
        
        # Если блогов меньше 8 (по количеству астро-систем), создаем новые
        if len(existing_blogs) < 8:
            print(f"Найдено {len(existing_blogs)} блогов, создаем недостающие...")
            for i in range(len(existing_blogs), 8):
                new_blog = BlogBlock(
                    title=f"Блог #{i+1}",
                    content=f"Содержание блога #{i+1}",
                    summary=f"Краткое описание блога #{i+1}",
                    is_active=True,
                    position=i+1
                )
                db.session.add(new_blog)
            db.session.commit()
            
            # Обновляем список блогов
            existing_blogs = BlogBlock.query.all()
        
        # Обновляем первые 8 блогов под астро-системы
        for i, system in enumerate(ASTRO_SYSTEMS):
            if i < len(existing_blogs):
                blog = existing_blogs[i]
                blog.title = system['title']
                blog.title_en = system['title_en']
                blog.title_de = system['title_de']
                blog.title_ru = system['title_ru']
                
                # Добавляем если контента еще нет или короткий
                if not blog.content or len(blog.content) < 100:
                    blog.content = system['content'] + " " + generate_mock_content()
                    blog.content_en = system['content_en'] + " " + generate_mock_content_en()
                    blog.content_de = system['content_de'] + " " + generate_mock_content_de()
                    blog.content_ru = system['content_ru'] + " " + generate_mock_content_ru()
                
                # Обновляем краткие описания
                blog.summary = system['content']
                blog.summary_en = system['content_en']
                blog.summary_de = system['content_de']
                blog.summary_ru = system['content_ru']
                
                # Обновляем даты
                blog.updated_at = datetime.utcnow()
                
                print(f"Блог #{i+1} обновлен как {system['name']}")
        
        db.session.commit()
        print("Блоги успешно настроены под разные астрологические системы!")

def generate_mock_content():
    """Генерирует временный контент для демонстрации"""
    return """
    <p>Сьогоднішній день буде насичений енергією змін. Для знаків води - час інтуїтивних рішень. Знаки повітря відчують приплив творчої енергії. Земні знаки знайдуть стабільність у робочих питаннях. Вогняні знаки можуть розраховувати на успіх у нових починаннях.</p>
    <p>Детальний прогноз для кожного знаку:</p>
    <ul>
        <li><strong>Овен</strong>: Ваша енергія на піку, спрямуйте її на важливі проєкти.</li>
        <li><strong>Телець</strong>: Фінансові питання вимагають уваги, але результат буде позитивним.</li>
        <li><strong>Близнюки</strong>: Спілкування сьогодні принесе нові можливості та контакти.</li>
        <li><strong>Рак</strong>: День підходить для вирішення сімейних питань.</li>
    </ul>
    <p>Сприятливі години для важливих справ: з 10:00 до 15:00. Колір дня: синій.</p>
    """

def generate_mock_content_en():
    """Generates temporary content for demonstration (English)"""
    return """
    <p>Today will be filled with the energy of change. For water signs - it's time for intuitive decisions. Air signs will feel an influx of creative energy. Earth signs will find stability in work matters. Fire signs can count on success in new beginnings.</p>
    <p>Detailed forecast for each sign:</p>
    <ul>
        <li><strong>Aries</strong>: Your energy is at its peak, direct it to important projects.</li>
        <li><strong>Taurus</strong>: Financial matters require attention, but the result will be positive.</li>
        <li><strong>Gemini</strong>: Communication today will bring new opportunities and contacts.</li>
        <li><strong>Cancer</strong>: The day is suitable for resolving family issues.</li>
    </ul>
    <p>Favorable hours for important matters: from 10:00 to 15:00. Color of the day: blue.</p>
    """

def generate_mock_content_de():
    """Generates temporary content for demonstration (German)"""
    return """
    <p>Der heutige Tag wird mit der Energie der Veränderung erfüllt sein. Für Wasserzeichen ist es Zeit für intuitive Entscheidungen. Luftzeichen werden einen Zustrom kreativer Energie spüren. Erdzeichen werden Stabilität in Arbeitsfragen finden. Feuerzeichen können mit Erfolg bei neuen Anfängen rechnen.</p>
    <p>Detaillierte Prognose für jedes Zeichen:</p>
    <ul>
        <li><strong>Widder</strong>: Ihre Energie ist auf dem Höhepunkt, lenken Sie sie auf wichtige Projekte.</li>
        <li><strong>Stier</strong>: Finanzielle Angelegenheiten erfordern Aufmerksamkeit, aber das Ergebnis wird positiv sein.</li>
        <li><strong>Zwillinge</strong>: Kommunikation wird heute neue Möglichkeiten und Kontakte bringen.</li>
        <li><strong>Krebs</strong>: Der Tag eignet sich gut für die Lösung von Familienproblemen.</li>
    </ul>
    <p>Günstige Stunden für wichtige Angelegenheiten: von 10:00 bis 15:00 Uhr. Farbe des Tages: Blau.</p>
    """

def generate_mock_content_ru():
    """Generates temporary content for demonstration (Russian)"""
    return """
    <p>Сегодняшний день будет наполнен энергией перемен. Для знаков воды - время интуитивных решений. Знаки воздуха почувствуют приток творческой энергии. Земные знаки найдут стабильность в рабочих вопросах. Огненные знаки могут рассчитывать на успех в новых начинаниях.</p>
    <p>Подробный прогноз для каждого знака:</p>
    <ul>
        <li><strong>Овен</strong>: Ваша энергия на пике, направьте ее на важные проекты.</li>
        <li><strong>Телец</strong>: Финансовые вопросы требуют внимания, но результат будет положительным.</li>
        <li><strong>Близнецы</strong>: Общение сегодня принесет новые возможности и контакты.</li>
        <li><strong>Рак</strong>: День подходит для решения семейных вопросов.</li>
    </ul>
    <p>Благоприятные часы для важных дел: с 10:00 до 15:00. Цвет дня: синий.</p>
    """

if __name__ == "__main__":
    setup_astro_blogs()
    print("Готово!")
