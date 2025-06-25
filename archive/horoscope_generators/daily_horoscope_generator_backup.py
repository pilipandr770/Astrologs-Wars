"""
Скрипт для ежедневной генерации гороскопов для разных астрологических систем.
Будет запускаться автоматически в 7:00 утра.
"""
import os
import time
import json
from datetime import datetime
import logging
from openai import OpenAI
import requests
from flask import current_app
import io
from werkzeug.utils import secure_filename
import pytz

# Импорты для астрологических расчетов
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib.const import LIST_SIGNS, LIST_PLANETS, LIST_ASPECTS

from app import create_app, db
from app.models import BlogBlock
from app.blog_automation.models import ContentGenerationLog
from app.utils.file_utils import save_uploaded_file

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("horoscope_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("daily_horoscope")

# Астрологические системы с их особенностями и ассистентами
ASTRO_SYSTEMS = [
    {
        'name': 'Європейська астрологія',
        'position': 1,
        'assistant_id': 'EUROPEAN_ASTROLOGY_ASSISTANT_ID',  # ID будет заменен из .env
        'style': 'классическая европейская астрология, зодиакальные знаки, влияние планет',
        'name_en': 'European Astrology',
        'name_de': 'Europäische Astrologie',
        'name_ru': 'Европейская астрология',
    },
    {
        'name': 'Китайська астрологія',
        'position': 2,
        'assistant_id': 'CHINESE_ASTROLOGY_ASSISTANT_ID',
        'style': 'китайская астрология, животные-покровители, взаимодействие энергий инь и ян',
        'name_en': 'Chinese Astrology',
        'name_de': 'Chinesische Astrologie',
        'name_ru': 'Китайская астрология',
    },
    {
        'name': 'Індійська астрологія',
        'position': 3,
        'assistant_id': 'INDIAN_ASTROLOGY_ASSISTANT_ID',
        'style': 'ведическая астрология, накшатры, влияние карм и дош',
        'name_en': 'Indian Astrology',
        'name_de': 'Indische Astrologie',
        'name_ru': 'Индийская астрология',
    },
    {
        'name': 'Лал Кітаб',
        'position': 4,
        'assistant_id': 'LAL_KITAB_ASSISTANT_ID',
        'style': 'Лал Китаб, народная астрология, простые средства для устранения негативных влияний',
        'name_en': 'Lal Kitab',
        'name_de': 'Lal Kitab',
        'name_ru': 'Лал Китаб',
    },
    {
        'name': 'Джйотіш',
        'position': 5,
        'assistant_id': 'JYOTISH_ASSISTANT_ID',
        'style': 'глубокий анализ Джйотиш, древние ведические тексты, духовные аспекты',
        'name_en': 'Jyotish',
        'name_de': 'Jyotish',
        'name_ru': 'Джйотиш',
    },
    {
        'name': 'Нумерологія',
        'position': 6,
        'assistant_id': 'NUMEROLOGY_ASSISTANT_ID',
        'style': 'числовые вибрации, суммирование дат, взаимосвязи чисел, жизненные циклы',
        'name_en': 'Numerology',
        'name_de': 'Numerologie',
        'name_ru': 'Нумерология',
    },
    {
        'name': 'Таро',
        'position': 7,
        'assistant_id': 'TAROT_ASSISTANT_ID',
        'style': 'символизм карт Таро, расклады на день, толкования арканов',
        'name_en': 'Tarot',
        'name_de': 'Tarot',
        'name_ru': 'Таро',
    },
    {
        'name': 'Планетарна астрологія',
        'position': 8,
        'assistant_id': 'PLANETARY_ASTROLOGY_ASSISTANT_ID',
        'style': 'влияние планет, транзиты, ретроградность, аспекты планет и их влияние на повседневную жизнь',
        'name_en': 'Planetary Astrology',
        'name_de': 'Planetenastrologie',
        'name_ru': 'Планетарная астрология',
    }
]

class HoroscopeGenerator:
    """Класс для генерации ежедневных гороскопов"""
    
    def __init__(self, app=None):
        self.app = app or create_app()
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.translation_assistant_id = os.environ.get('OPENAI_TRANSLATION_ASSISTANT_ID')
        
        # Загружаем ID ассистентов из переменных окружения
        for system in ASTRO_SYSTEMS:            env_var = system.get('assistant_id')
            if env_var:
                assistant_id = os.environ.get(env_var, '')
                system['assistant_id_value'] = assistant_id
                logger.info(f"Загружен ассистент для {system['name']}: переменная {env_var}, ID {assistant_id}")
            else:
                system['assistant_id_value'] = ''
                logger.warning(f"Для системы {system['name']} не указана переменная окружения assistant_id")
    
    def generate_all_horoscopes(self):
        """Генерирует гороскопы для всех астрологических систем"""
        with self.app.app_context():
            european_time = self._get_european_datetime()
            logger.info(f"Начинаем генерацию гороскопов на {european_time.strftime('%Y-%m-%d %H:%M')} (европейское время)")
            for system in ASTRO_SYSTEMS:
                try:
                    logger.info(f"Генерация гороскопа для системы: {system['name']}")
                    
                    # Генерируем контент
                    content = self.generate_horoscope(system)
                    if not content:
                        logger.error(f"Не удалось сгенерировать контент для {system['name']}")
                        continue
                    
                    # Обновляем блог
                    self.update_blog(system, content)
                    
                    # Добавляем лог
                    self._log_activity(f"generate_horoscope_{system['position']}", 
                                    "success", f"Гороскоп для {system['name']} успешно сгенерирован")
                    
                    # Делаем небольшую паузу между запросами
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Ошибка при генерации гороскопа для {system['name']}: {str(e)}")
                    self._log_activity(f"generate_horoscope_{system['position']}", 
                                    "failed", f"Ошибка: {str(e)}")
            
            logger.info("Генерация всех гороскопов завершена")
      def generate_horoscope(self, system):
        """Генерирует гороскоп для конкретной астрологической системы с использованием астрологических данных"""
        if not system.get('assistant_id_value'):
            logger.error(f"ID ассистента для {system['name']} не указан или не настроен")
            return None
            
        # Получаем европейское время
        european_time = self._get_european_datetime()
        today = european_time.strftime('%Y-%m-%d')
        current_time = european_time.strftime('%H:%M')
        
        # Получаем астрологические данные
        planet_positions = self._calculate_planet_positions()
        astrological_events = self._get_astrological_events()
        
        prompt = f"""
        Создай ежедневный гороскоп на {today} (текущее европейское время: {current_time}) 
        в стиле {system['name']} ({system['style']}).
        
        АСТРОЛОГИЧЕСКИЕ ДАННЫЕ НА СЕГОДНЯ:
        
        {planet_positions}
        
        {astrological_events}
        
        Гороскоп должен включать:
        1. Общее влияние планет/энергий на день, ОСНОВЫВАЯСЬ НА РЕАЛЬНОМ ПОЛОЖЕНИИ ПЛАНЕТ, указанном выше
        2. Прогноз для каждого знака зодиака (или соответствующего элемента в данной системе)
        3. Советы и рекомендации на день, учитывая текущие астрологические события
        4. Благоприятные часы и цвета дня
        
        Используй профессиональную терминологию, характерную для {system['name']}.
        ВАЖНО: Опирайся на предоставленные астрологические данные для создания точного и аутентичного прогноза.
        Отформатируй текст с использованием HTML тегов для структурирования (параграфы, списки, выделения).
        Объем: 300-500 слов.
        """
        
        try:
            # Создаем тред для общения с ассистентом
            thread = self.client.beta.threads.create()
            
            # Добавляем сообщение
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt
            )
            
            # Запускаем ассистента
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=system['assistant_id_value']
            )
            
            # Ожидаем завершения
            response = self._wait_for_run(thread.id, run.id)
            if not response or not response.get('success'):
                logger.error(f"Ошибка при работе с ассистентом: {response.get('error')}")
                return None
                
            return response.get('content')
            
        except Exception as e:
            logger.error(f"Ошибка при генерации гороскопа: {str(e)}")
            return None
    
    def update_blog(self, system, content):
        """Обновляет блог с новым контентом"""
        # Находим блок по позиции
        blog_block = BlogBlock.query.filter_by(position=system['position']).first()
        
        if not blog_block:
            logger.error(f"Блок блога для позиции {system['position']} не найден")
            return False
          # Формируем заголовок с европейским временем
        today = self._get_european_datetime().strftime('%d.%m.%Y')
        title = f"{system['name']} - прогноз на {today}"
        
        # Обновляем контент
        blog_block.title = title
        blog_block.content = content
        blog_block.summary = content[:200] + "..." if len(content) > 200 else content
        blog_block.updated_at = datetime.utcnow()
        
        # Переводим контент
        self._translate_content(blog_block)
        
        # Генерируем изображение
        self._generate_image(blog_block, system)
        
        # Сохраняем изменения
        db.session.commit()
        logger.info(f"Блог {system['name']} успешно обновлен")
        return True
    
    def _translate_content(self, blog_block):
        """Переводит контент на другие языки"""
        try:
            # Переводим на английский
            en_result = self._translate_to_language(blog_block.content, "английский")
            if en_result:
                blog_block.title_en = f"{blog_block.title} (EN)"
                blog_block.content_en = en_result
                blog_block.summary_en = en_result[:200] + "..." if len(en_result) > 200 else en_result
                logger.info("Контент переведен на английский")
            
            # Переводим на немецкий
            de_result = self._translate_to_language(blog_block.content, "немецкий")
            if de_result:
                blog_block.title_de = f"{blog_block.title} (DE)"
                blog_block.content_de = de_result
                blog_block.summary_de = de_result[:200] + "..." if len(de_result) > 200 else de_result
                logger.info("Контент переведен на немецкий")
            
            # Переводим на русский
            ru_result = self._translate_to_language(blog_block.content, "русский")
            if ru_result:
                blog_block.title_ru = f"{blog_block.title} (RU)"
                blog_block.content_ru = ru_result
                blog_block.summary_ru = ru_result[:200] + "..." if len(ru_result) > 200 else ru_result
                logger.info("Контент переведен на русский")
                
        except Exception as e:
            logger.error(f"Ошибка при переводе контента: {str(e)}")
    
    def _translate_to_language(self, content, language):
        """Переводит текст на указанный язык"""
        if not content or not self.translation_assistant_id:
            return None
            
        translation_prompt = f"""
        Переведи следующий астрологический прогноз на {language} язык. 
        Сохрани HTML форматирование и стиль оригинала:
        
        {content}
        """
        
        try:
            # Создаем тред для перевода
            thread = self.client.beta.threads.create()
            
            # Добавляем сообщение
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=translation_prompt
            )
            
            # Запускаем ассистента-переводчика
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.translation_assistant_id
            )
            
            # Ожидаем завершения
            response = self._wait_for_run(thread.id, run.id)
            if not response or not response.get('success'):
                logger.error(f"Ошибка при переводе: {response.get('error')}")
                return None
                
            return response.get('content')
            
        except Exception as e:
            logger.error(f"Ошибка при переводе: {str(e)}")
            return None
    
    def _generate_image(self, blog_block, system):
        """Генерирует изображение для блога"""
        try:
            # Генерируем промпт для DALL-E            # Получаем планетарные данные для изображения
            try:
                date = self._get_european_datetime()
                planet_data = self._get_significant_planets()
                date_str = date.strftime('%d.%m.%Y')
            except:
                planet_data = ""
                date_str = "текущей даты"
                
            image_prompt = f"""
            Создай профессиональную иллюстрацию для астрологического прогноза в стиле {system['name']} на {date_str}.
            Изображение должно быть мистическим, духовным и содержать символы, характерные для {system['style']}.
            {planet_data}
            Визуализируй космические силы и планетарные влияния с помощью символизма.
            Стиль: цифровая графика, высококачественная, с глубокими цветами и детализацией.
            Без текста или надписей.
            """
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Скачиваем изображение
            image_response = requests.get(image_url)
            
            if image_response.status_code == 200:
                # Сохраняем изображение
                filename = f"astro_{system['position']}_{datetime.now().strftime('%Y%m%d')}.png"
                
                with self.app.app_context():
                    save_path = save_uploaded_file(
                        file_data=io.BytesIO(image_response.content),
                        folder='uploads/blog',
                        filename=filename
                    )
                
                # Обновляем изображение в блоге
                if save_path:
                    blog_block.featured_image = filename if '/' not in save_path else save_path.split('/')[-1]
                    logger.info(f"Изображение для {system['name']} успешно сгенерировано и сохранено")
            else:
                logger.error(f"Ошибка при скачивании изображения: {image_response.status_code}")
                
        except Exception as e:
            logger.error(f"Ошибка при генерации изображения: {str(e)}")
    
    def _wait_for_run(self, thread_id, run_id, max_retries=10):
        """Ожидает завершения запуска ассистента"""
        retry_count = 0
        while retry_count < max_retries:
            try:
                # Проверяем статус
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run_id
                )
                
                # Если завершено, получаем сообщения
                if run.status == "completed":
                    messages = self.client.beta.threads.messages.list(
                        thread_id=thread_id
                    )
                    
                    # Получаем ответ ассистента
                    for message in messages.data:
                        if message.role == "assistant":
                            content = ""
                            for content_part in message.content:
                                if content_part.type == "text":
                                    content += content_part.text.value
                                    
                            return {"success": True, "content": content}
                    
                    return {"success": False, "error": "Ответ от ассистента не получен"}
                
                # Если ошибка
                elif run.status == "failed" or run.status == "expired":
                    return {"success": False, "error": f"Запуск ассистента завершился со статусом {run.status}"}
                
                # Ждем и пробуем снова
                time.sleep(3)
                retry_count += 1
                
            except Exception as e:
                logger.error(f"Ошибка при ожидании выполнения: {str(e)}")
                retry_count += 1
        
        return {"success": False, "error": "Превышено максимальное количество попыток"}
    
    def _log_activity(self, action, status, message):
        """Логирует действия генератора гороскопов"""
        try:
            with self.app.app_context():
                ContentGenerationLog.add_log(
                    topic=None,
                    action=action,
                    status=status,
                    message=message
                )
        except Exception as e:
            logger.error(f"Ошибка при логировании: {str(e)}")
    
    def check_assistants_setup(self):
        """Проверяет настройки ассистентов и выводит информацию о них"""
        print("\nНастройки ассистентов для генерации гороскопов:")
        print("-" * 80)
        
        for system in ASTRO_SYSTEMS:
            assistant_id = system.get('assistant_id_value', '')
            if assistant_id:
                status = "✓"
                info = f"ID: {assistant_id}"
            else:
                status = "✗"
                info = f"Не настроен (переменная: {system.get('assistant_id', 'не указана')})"
                
            print(f"{system['name']:<25} | {status} | {info}")
        
        print("\nAссистент для переводов:")
        if self.translation_assistant_id:
            print(f"✓ | ID: {self.translation_assistant_id}")
        else:
            print("✗ | Не настроен")
        
        print("-" * 80)
    
    def _get_european_datetime(self):
        """Возвращает текущую дату и время по европейскому времени (Киев/UTC+3)"""
        kiev_tz = pytz.timezone('Europe/Kiev')
        return datetime.now(kiev_tz)
        
    def _calculate_planet_positions(self):
        """Рассчитывает положения планет на текущую дату"""
        try:
            # Получаем текущее время по Киеву
            current_time = self._get_european_datetime()
            
            # Форматируем для flatlib (YYYY/MM/DD HH:MM)
            date_str = current_time.strftime('%Y/%m/%d %H:%M')
            
            # Создаем объект даты/времени flatlib
            date = Datetime(date_str, '+03:00')  # Киев UTC+3
            
            # Координаты Киева (можно настроить для других локаций)
            pos = GeoPos(50.45, 30.52)  # Киев: широта, долгота
            
            # Создаем карту
            chart = Chart(date, pos)
            
            # Информация о планетах
            planet_info = []
            for planet_name in LIST_PLANETS:
                try:
                    planet = chart.getObject(planet_name)
                    retrograde = " (R)" if planet.retrograde else ""
                    planet_info.append(f"{planet_name}: {planet.sign} {planet.signlon:.1f}°{retrograde}")
                except:
                    continue
            
            # Аспекты между планетами
            aspects = []
            for p1_idx, p1_name in enumerate(LIST_PLANETS[:-2]):  # Исключаем Узлы
                p1 = chart.getObject(p1_name)
                if not p1:
                    continue
                    
                for p2_name in LIST_PLANETS[p1_idx+1:-2]:
                    p2 = chart.getObject(p2_name)
                    if not p2:
                        continue
                        
                    # Получаем аспекты между планетами
                    aspect = chart.aspectType(p1, p2)
                    if aspect and aspect != 'none':
                        aspects.append(f"{p1_name} {aspect} {p2_name}")
            
            # Формируем результат
            result = "Положения планет:\n" + "\n".join(planet_info)
            if aspects:
                result += "\n\nВажные аспекты планет:\n" + "\n".join(aspects[:5])  # Ограничиваем количество аспектов
                
            return result
                
        except Exception as e:
            logger.error(f"Ошибка при расчете положений планет: {str(e)}")
            return "Информация о положении планет недоступна."
    
    def _get_astrological_events(self):
        """Определяет текущие астрологические события"""
        try:
            # Получаем текущую дату по Киеву
            current_time = self._get_european_datetime()
            
            # Список возможных событий
            events = []
            
            # Проверка на ретроградность планет
            date_str = current_time.strftime('%Y/%m/%d %H:%M')
            date = Datetime(date_str, '+03:00')
            pos = GeoPos(50.45, 30.52)
            chart = Chart(date, pos)
            
            for planet_name in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']:
                try:
                    planet = chart.getObject(planet_name)
                    if planet and planet.retrograde:
                        events.append(f"{planet_name} ретроградный")
                except:
                    continue
            
            # Проверка на затмения и другие особые события (упрощенная версия)
            month = current_time.month
            day = current_time.day
            
            # Примерные даты особых событий 2025 года
            if month == 3 and day in range(20, 22):
                events.append("Весеннее равноденствие")
            elif month == 6 and day in range(20, 22):
                events.append("Летнее солнцестояние")
            elif month == 9 and day in range(22, 24):
                events.append("Осеннее равноденствие")
            elif month == 12 and day in range(21, 23):
                events.append("Зимнее солнцестояние")
            
            # Полнолуния и Новолуния (приблизительно)
            if day in range(1, 3) or day in range(15, 17):
                # Точную фазу можно рассчитать с помощью дополнительных библиотек
                events.append("Приблизительное время Новолуния/Полнолуния")
            
            if events:
                return "Текущие астрологические события:\n" + "\n".join(events)
            else:
                return "Нет значимых астрологических событий на сегодня."
                
        except Exception as e:
            logger.error(f"Ошибка при определении астрологических событий: {str(e)}")
            return "Информация о астрологических событиях недоступна."
    
    def _get_significant_planets(self):
        """Получает информацию о наиболее значимых планетарных влияниях для изображения"""
        try:
            # Получаем текущее время по Киеву
            current_time = self._get_european_datetime()
            date_str = current_time.strftime('%Y/%m/%d %H:%M')
            
            # Создаем объекты для расчета
            date = Datetime(date_str, '+03:00')
            pos = GeoPos(50.45, 30.52)
            chart = Chart(date, pos)
            
            # Определяем важные планеты
            significant = []
            
            # Получаем Солнце и Луну
            sun = chart.getObject('Sun')
            moon = chart.getObject('Moon')
            
            # Добавляем их в результат
            if sun:
                significant.append(f"Солнце в знаке {sun.sign}")
            if moon:
                significant.append(f"Луна в знаке {moon.sign}")
            
            # Проверяем ретроградные планеты
            retrogrades = []
            for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
                try:
                    p = chart.getObject(planet)
                    if p and p.retrograde:
                        retrogrades.append(planet)
                except:
                    continue
                    
            # Добавляем информацию о ретроградности
            if retrogrades:
                significant.append(f"Ретроградные планеты: {', '.join(retrogrades)}")
                
            result = "Включи визуальные элементы, отражающие: " + "; ".join(significant) + "."
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при получении данных о значимых планетах: {str(e)}")
            return ""
# Точка входа для запуска скрипта
if __name__ == "__main__":
    generator = HoroscopeGenerator()
    
    import sys
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        generator.check_assistants_setup()
    else:
        print("\nГенерация ежедневных гороскопов...")
        generator.generate_all_horoscopes()
        print("\nЕжедневные гороскопы сгенерированы!")
        print("\nДля проверки настроек ассистентов запустите: python daily_horoscope_generator.py check")
