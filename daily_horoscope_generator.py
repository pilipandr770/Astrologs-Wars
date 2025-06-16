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
    }
]

class HoroscopeGenerator:
    """Класс для генерации ежедневных гороскопов"""
    
    def __init__(self, app=None):
        self.app = app or create_app()
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.translation_assistant_id = os.environ.get('OPENAI_TRANSLATION_ASSISTANT_ID')
        
        # Загружаем ID ассистентов из переменных окружения
        for system in ASTRO_SYSTEMS:
            env_var = system['assistant_id']
            system['assistant_id'] = os.environ.get(env_var, '')
    
    def generate_all_horoscopes(self):
        """Генерирует гороскопы для всех астрологических систем"""
        with self.app.app_context():
            logger.info(f"Начинаем генерацию гороскопов на {datetime.now().strftime('%Y-%m-%d')}")
            
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
        """Генерирует гороскоп для конкретной астрологической системы"""
        if not system['assistant_id']:
            logger.error(f"ID ассистента для {system['name']} не указан")
            return None
            
        today = datetime.now().strftime('%Y-%m-%d')
        
        prompt = f"""
        Создай ежедневный гороскоп на {today} в стиле {system['name']} ({system['style']}).
        
        Гороскоп должен включать:
        1. Общее влияние планет/энергий на день
        2. Прогноз для каждого знака зодиака (или соответствующего элемента в данной системе)
        3. Советы и рекомендации на день
        4. Благоприятные часы и цвета дня
        
        Используй профессиональную терминологию, характерную для {system['name']}.
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
                assistant_id=system['assistant_id']
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
        
        # Формируем заголовок
        today = datetime.now().strftime('%d.%m.%Y')
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
            # Генерируем промпт для DALL-E
            image_prompt = f"""
            Создай профессиональную иллюстрацию для астрологического прогноза в стиле {system['name']}.
            Изображение должно быть мистическим, духовным и содержать символы, характерные для {system['style']}.
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

# Точка входа для запуска скрипта
if __name__ == "__main__":
    generator = HoroscopeGenerator()
    generator.generate_all_horoscopes()
    print("Ежедневные гороскопы сгенерированы!")
