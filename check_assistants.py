
from daily_horoscope_generator import HoroscopeGenerator

if __name__ == "__main__":
    print("Проверка настройки ассистентов для астрологических систем")
    print("=" * 80)
    
    generator = HoroscopeGenerator()
    generator.check_assistants_setup()
    
    print("\nДля правильной работы генерации гороскопов необходимо настроить всех ассистентов.")
    print("Добавьте ID ассистентов в файл .env в соответствующие переменные.")
    print("\nПример:")
    print("EUROPEAN_ASTROLOGY_ASSISTANT_ID=asst_xxxxxxx")
    print("CHINESE_ASTROLOGY_ASSISTANT_ID=asst_yyyyyyy")
    print("...")
