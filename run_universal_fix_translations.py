#!/usr/bin/env python
"""
Универсальный скрипт для исправления проблем с переводами.
Работает на любой ОС.
"""

import os
import sys
import subprocess

def run_translation_fix():
    """Запуск процесса исправления переводов гороскопов"""
    print("Starting translation fix with extended timeout...")
    
    # Установка переменных окружения
    os.environ["USE_TRANSLATIONS"] = "true"
    os.environ["TRANSLATION_TIMEOUT"] = "180"  # Увеличенный таймаут (3 минуты)
    
    # Определяем команду для запуска Python
    python_command = None
    for cmd in ["python", "python3", "py"]:
        try:
            subprocess.run([cmd, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            python_command = cmd
            break
        except FileNotFoundError:
            continue
    
    if not python_command:
        print("Error: Python interpreter not found. Please make sure Python is installed.")
        return False
    
    # Запускаем исправление переводов с увеличенным таймаутом
    try:
        result = subprocess.run(
            [python_command, "fix_translations.py"], 
            env=os.environ,
            timeout=600  # 10-минутный глобальный таймаут
        )
        
        if result.returncode == 0:
            print("Translation fix completed successfully.")
            return True
        else:
            print(f"Translation fix failed with error code {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        print("Translation fix operation timed out after 10 minutes.")
        return False
    except Exception as e:
        print(f"Error running translation fix: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_translation_fix()
    
    if not success:
        print("\nSome issues occurred during translation fix.")
        
    input("Press Enter to exit...")
    sys.exit(0 if success else 1)
