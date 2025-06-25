"""
Скрипт для проверки и исправления проблем с переводами гороскопов.
Проверяет наличие полей для переводов, инициализирует NULL значения и тестирует перевод.
"""

import os
import sys
import time
import logging
from dotenv import load_dotenv
from sqlalchemy import inspect
from translator import HoroscopeTranslator

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("translation_fix.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("TranslationFix")

# Загружаем переменные окружения
load_dotenv()

# Подключаемся к приложению только после загрузки переменных окружения
from app import create_app, db
from app.models import BlogBlock

app = create_app()

def check_translation_variables():
    """Проверяет наличие необходимых переменных окружения для перевода"""
    required_vars = [
        'OPENAI_API_KEY',
        'OPENAI_TRANSLATION_ASSISTANT_ID',
        'USE_TRANSLATIONS'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
            
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return False
        
    # Проверяем значение USE_TRANSLATIONS
    use_translations = os.environ.get('USE_TRANSLATIONS', 'true').lower() == 'true'
    if not use_translations:
        logger.warning("Translations are disabled (USE_TRANSLATIONS is not 'true')")
        
    logger.info(f"Translation Assistant ID: {os.environ.get('OPENAI_TRANSLATION_ASSISTANT_ID')}")
    logger.info(f"USE_TRANSLATIONS: {os.environ.get('USE_TRANSLATIONS')}")
    return True

def check_db_fields():
    """
    Проверяет наличие необходимых полей в базе данных для переводов
    и инициализирует их NULL значениями, если они не содержат данных
    """
    with app.app_context():
        try:
            # Проверяем наличие всех полей
            insp = inspect(db.engine)
            columns = {column['name']: column for column in insp.get_columns('blog_block')}
            
            required_fields = [
                'title_ua', 'content_ua', 'summary_ua',
                'title_en', 'content_en', 'summary_en', 
                'title_de', 'content_de', 'summary_de',
                'title_ru', 'content_ru', 'summary_ru'
            ]
            
            missing_fields = [field for field in required_fields if field not in columns]
            
            if missing_fields:
                logger.error(f"Missing fields in database: {', '.join(missing_fields)}")
                return False
                
            # Проверяем и инициализируем NULL поля
            blocks = BlogBlock.query.all()
            fixed_count = 0
            
            for block in blocks:
                updated = False
                
                # Если основные поля на украинском, копируем их в поля _ua
                if block.title and not block.title_ua:
                    block.title_ua = block.title
                    updated = True
                    
                if block.content and not block.content_ua:
                    block.content_ua = block.content
                    updated = True
                    
                if block.summary and not block.summary_ua:
                    block.summary_ua = block.summary
                    updated = True
                
                if updated:
                    fixed_count += 1
                    db.session.add(block)
            
            if fixed_count > 0:
                db.session.commit()
                logger.info(f"Fixed {fixed_count} blocks with missing Ukrainian language fields")
                
            # Подсчитываем количество блоков с отсутствующими переводами
            missing_translations = {}
            for lang in ['en', 'de', 'ru']:
                missing_count = 0
                for block in blocks:
                    if ((not getattr(block, f'title_{lang}') or 
                         not getattr(block, f'content_{lang}')) and
                        block.is_active):
                        missing_count += 1
                        
                missing_translations[lang] = missing_count
                
            for lang, count in missing_translations.items():
                if count > 0:
                    logger.info(f"Found {count} active blocks missing {lang} translations")
                
            return True
                
        except Exception as e:
            logger.error(f"Error checking database fields: {str(e)}")
            return False
            
def test_translator():
    """Тестирует функциональность переводчика"""
    logger.info("Testing translator functionality")
    
    translator = HoroscopeTranslator()
    if not translator.is_available():
        logger.error("Translator is not available - check API key and Assistant ID")
        return False
        
    test_text = "Сьогодні зорі віщують важливі зміни. День сприятливий для нових починань."
      # Тестируем перевод для каждого поддерживаемого языка
    success_count = 0
    for lang_code in ['en', 'de', 'ru']:
        logger.info(f"Testing translation to {lang_code}")
        
        result = translator.translate_content(test_text, lang_code)
        
        if result is None:
            logger.error(f"Translation to {lang_code} failed: got None result")
            continue
            
        if result.get('success'):
            translated_text = result.get('content')
            logger.info(f"Translation to {lang_code} successful: {translated_text}")
            success_count += 1
        else:
            logger.error(f"Translation to {lang_code} failed: {result.get('error')}")
            
    return success_count == 3

def fix_missing_translations(max_blocks=3):
    """
    Исправляет отсутствующие переводы в активных блогах
    
    Args:
        max_blocks: Максимальное количество блоков для исправления за один запуск
    """
    with app.app_context():
        try:
            # Получаем активные блоки с отсутствующими переводами
            blocks = BlogBlock.query.filter_by(is_active=True).all()
            blocks_to_fix = []
            
            for block in blocks:
                missing_langs = []
                
                for lang in ['en', 'de', 'ru']:
                    if (not getattr(block, f'title_{lang}') or 
                        not getattr(block, f'content_{lang}')):
                        missing_langs.append(lang)
                        
                if missing_langs:
                    blocks_to_fix.append((block, missing_langs))
            
            # Ограничиваем количество блоков для обработки
            blocks_to_fix = blocks_to_fix[:max_blocks]
            
            if not blocks_to_fix:
                logger.info("No blocks with missing translations found")
                return True
                
            logger.info(f"Found {len(blocks_to_fix)} blocks with missing translations, fixing up to {max_blocks}")
            
            # Инициализируем переводчик
            translator = HoroscopeTranslator()
            if not translator.is_available():
                logger.error("Translator is not available")
                return False
                
            # Исправляем переводы
            for block, missing_langs in blocks_to_fix:
                logger.info(f"Fixing translations for block {block.id} (position: {block.position})")
                
                # Используем украинское содержимое или основное содержимое
                source_title = block.title_ua or block.title
                source_content = block.content_ua or block.content
                source_summary = block.summary_ua or block.summary
                
                for lang in missing_langs:
                    logger.info(f"Translating to {lang}")
                      # Переводим заголовок
                    if not getattr(block, f'title_{lang}') and source_title:
                        title_result = translator.translate_content(source_title, lang)
                        if title_result is not None and title_result.get('success'):
                            setattr(block, f'title_{lang}', title_result.get('content'))
                            logger.info(f"Title translated to {lang}")
                        elif title_result is None:
                            logger.error(f"Title translation to {lang} failed: got None result")
                            
                    # Переводим содержимое
                    if not getattr(block, f'content_{lang}') and source_content:
                        content_result = translator.translate_content(source_content, lang)
                        if content_result is not None and content_result.get('success'):
                            setattr(block, f'content_{lang}', content_result.get('content'))
                            logger.info(f"Content translated to {lang}")
                        elif content_result is None:
                            logger.error(f"Content translation to {lang} failed: got None result")
                    
                    # Переводим резюме, если оно есть
                    if not getattr(block, f'summary_{lang}') and source_summary:
                        summary_result = translator.translate_content(source_summary, lang)
                        if summary_result is not None and summary_result.get('success'):
                            setattr(block, f'summary_{lang}', summary_result.get('content'))
                            logger.info(f"Summary translated to {lang}")
                        elif summary_result is None:
                            logger.error(f"Summary translation to {lang} failed: got None result")
                    
                    # Небольшая пауза между переводами
                    time.sleep(2)
                    
                # Сохраняем изменения
                db.session.add(block)
                db.session.commit()
                logger.info(f"Translations for block {block.id} saved")
                
            return True
            
        except Exception as e:
            logger.error(f"Error fixing translations: {str(e)}")
            return False

def main():
    """Основная функция для проверки и исправления проблем с переводами"""
    logger.info("Starting translation fix script")
    
    # Проверяем переменные окружения
    if not check_translation_variables():
        logger.error("Failed to verify translation environment variables")
        return False
        
    # Проверяем поля базы данных
    if not check_db_fields():
        logger.error("Failed to verify database fields")
        return False
        
    # Тестируем переводчик
    if not test_translator():
        logger.error("Translator test failed")
        return False
        
    # Исправляем отсутствующие переводы
    if not fix_missing_translations(max_blocks=5):
        logger.error("Failed to fix missing translations")
        return False
        
    logger.info("Translation fix completed successfully")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
