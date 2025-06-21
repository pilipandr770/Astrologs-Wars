# Updated on 2025-06-21 to use replacement mode horoscope generator

# Updated on 2025-06-21 to use integrated horoscope generator with images

"""
Скрипт для планирования ежедневной генерации гороскопов в 7:00 утра
"""
import schedule
import time
import subprocess
import logging
import os
from datetime import datetime

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='horoscope_scheduler.log',
    filemode='a'
)
logger = logging.getLogger("horoscope_scheduler")

def run_horoscope_generation():
    """Запускает скрипт генерации гороскопов"""
    try:
        logger.info(f"Начало запуска генерации гороскопов: {datetime.now()}")
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'daily_horoscope_replace.py')
        
        # Запускаем скрипт генерации
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Генерация гороскопов выполнена успешно")
            logger.info(f"Вывод: {result.stdout}")
        else:
            logger.error(f"Ошибка при генерации гороскопов: {result.returncode}")
            logger.error(f"Вывод ошибки: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Исключение при запуске генерации гороскопов: {str(e)}")

# Планируем запуск каждый день в 7:00 утра
schedule.every().day.at("07:00").do(run_horoscope_generation)

# Запускаем при первом запуске (если необходимо)
# run_horoscope_generation()

logger.info("Планировщик гороскопов запущен")
print("Планировщик гороскопов запущен. Генерация будет выполняться ежедневно в 7:00.")

# Основной цикл
while True:
    schedule.run_pending()
    time.sleep(60)  # Проверяем каждую минуту
