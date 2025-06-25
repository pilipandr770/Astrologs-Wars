#!/usr/bin/env python
"""
Универсальный скрипт для запуска генерации гороскопов 
с поддержкой DALL-E и переводов.
Работает на любой ОС.
"""

import os
import sys
import subprocess

def run_horoscope_generation():
    """Запуск генерации гороскопов с активированными DALL-E и переводами"""
    print("Running horoscope generator with DALL-E images and translations...")
    
    # Установка переменных окружения
    os.environ["USE_DALLE_IMAGES"] = "true"
    os.environ["USE_TRANSLATIONS"] = "true"
    
    # Определяем команду для запуска Python
    # (python, python3, py - в зависимости от того, что доступно)
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
    
    # Запускаем генерацию гороскопов
    try:
        result = subprocess.run(
            [python_command, "daily_horoscope_replace.py"], 
            env=os.environ
        )
        
        if result.returncode == 0:
            print("Horoscope generation completed successfully.")
            return True
        else:
            print(f"Horoscope generation failed with error code {result.returncode}")
            return False
    except Exception as e:
        print(f"Error running horoscope generator: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_horoscope_generation()
    
    if not success:
        print("\nSome issues occurred during generation.")
        
    input("Press Enter to exit...")
    sys.exit(0 if success else 1)
