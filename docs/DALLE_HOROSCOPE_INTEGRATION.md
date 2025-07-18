# Интеграция DALL-E 3 для изображений гороскопов

**Дата обновления:** 25.06.2025

## Введение

Этот документ описывает интеграцию DALL-E 3 API от OpenAI для генерации высококачественных изображений для каждого из 8 астрологических систем в нашем генераторе гороскопов.

## Обзор функциональности

Улучшение генерации изображений в скрипте `daily_horoscope_replace.py` с использованием DALL-E 3 включает:

1. **Адаптивный подход к генерации изображений**
   - Использование DALL-E 3, когда API ключ доступен
   - Автоматический переход на локальную генерацию, если DALL-E недоступен

2. **Уникальные промты для каждой астрологической системы**
   - Европейская астрология: зодиакальные символы в космической композиции
   - Китайская астрология: элементы китайского зодиака и инь-янь
   - Индийская астрология: ведические астрологические символы
   - Лал Китаб: символы планет и кармы в космических цветах
   - Джйотиш: планетарные символы и ведические духовные элементы
   - Нумерология: числовые символы и священная геометрия
   - Таро: мистические символы и космические элементы
   - Планетарная астрология: планеты, орбиты и космические тела

3. **Контроль активации через переменные окружения**
   - `USE_DALLE_IMAGES`: `true`/`false` - включить или отключить DALL-E
   - Настраивается в `.env` и в конфигурации Render

## Технические детали

### Функция генерации DALL-E

```python
def generate_dalle_image(system_name, title, current_date, upload_dir, filename, width=1024, height=1024):
    # Инициализация клиента OpenAI
    client = OpenAI()
    
    # Формирование промта в зависимости от астрологической системы
    prompt = system_prompts.get(system_name, fallback_prompt)
    
    # Вызов DALL-E API
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=f"{width}x{height}",
        quality="standard",
        n=1
    )
    
    # Загрузка и сохранение изображения
    image_url = response.data[0].url
    image_response = requests.get(image_url)
    with open(full_path, 'wb') as f:
        f.write(image_response.content)
```

### Интеграция с существующим кодом

Функция `create_astrology_image` была модифицирована для проверки доступности DALL-E:

```python
if use_dalle:
    # Try generating with DALL-E
    success, result = generate_dalle_image(...)
    if success:
        return filename
    
# Fallback to local image generation
```

## Настройка и управление

### Активация/деактивация DALL-E

В файле `.env`:
```
USE_DALLE_IMAGES=true  # Использовать DALL-E для гороскопов
```

В `render.yaml` (для продакшена):
```yaml
envVars:
  - key: USE_DALLE_IMAGES
    value: "true"
```

### Управление расходами

Генерация изображений DALL-E 3 потребляет API токены. Для экономии:

1. Установите `USE_DALLE_IMAGES=false` когда тестируете другую функциональность
2. Рассмотрите возможность генерации раз в неделю, а не ежедневно
3. Отслеживайте использование API токенов в панели управления OpenAI

## Рекомендации

1. **Поддержание API ключа OpenAI**
   - Регулярно проверяйте баланс и обновляйте ключ
   - Имейте резервный ключ для критических периодов

2. **Оптимизация промтов**
   - Периодически обновляйте промты для получения лучших результатов
   - Тестируйте новые промты перед использованием в продакшене

## Устранение неполадок

### Распространенные проблемы

1. **Ошибка аутентификации API**
   - Проверьте актуальность OPENAI_API_KEY
   - Убедитесь в наличии средств на счету

2. **Таймаут соединения**
   - API OpenAI может быть перегружен
   - Увеличьте время ожидания или повторите запрос позже

3. **Проблемы с изображениями**
   - Изображения не соответствуют ожиданиям? Отредактируйте промты
   - Низкое качество? Увеличьте параметр quality до "hd"
