"""
Скрипт запуска генератора гороскопов с улучшенными изображениями
"""
import os
import sys
import subprocess
import platform

def print_colored(text, color="green"):
    """Print colored text in console"""
    colors = {
        "green": "\033[92m",
        "blue": "\033[94m",
        "red": "\033[91m",
        "end": "\033[0m"
    }
    
    # Windows cmd doesn't support ANSI colors by default
    if platform.system() == "Windows" and "TERM" not in os.environ:
        print(text)
    else:
        print(f"{colors.get(color, '')}{text}{colors['end']}")

if __name__ == "__main__":
    print_colored("Running enhanced daily horoscope generator with improved images...")
    
    try:
        # Запускаем скрипт генерации гороскопов
        subprocess.run([sys.executable, "daily_horoscope_replace.py"], check=True)
        print_colored("Done!")
    except FileNotFoundError:
        print_colored(f"Error: File 'daily_horoscope_replace.py' not found!", "red")
        print(f"Current directory: {os.getcwd()}")
        print("Files in current directory:")
        for file in os.listdir():
            if file.endswith('.py'):
                print(f"  - {file}")
    except subprocess.CalledProcessError as e:
        print_colored(f"Error running horoscope generator: {e}", "red")
    except Exception as e:
        print_colored(f"Unexpected error: {e}", "red")
    
    # Ждем нажатия Enter перед закрытием окна
    input("Press Enter to exit...")
