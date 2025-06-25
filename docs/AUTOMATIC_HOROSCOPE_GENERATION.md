# Настройка автоматической генерации гороскопов с эфемеридами

## Общая информация

В рамках последнего обновления проекта реализована автоматизация генерации гороскопов с использованием точных астрономических данных (эфемерид). Гороскопы генерируются автоматически каждый день в 3:00 утра.

## Настройки шедулера

### Render.yaml (облачное исполнение)

```yaml
- type: cron
  name: astrolog-horoscope-generator
  runtime: python
  region: frankfurt
  schedule: "0 3 * * *"  # Run once a day at 3:00 AM
  buildCommand: pip install -r requirements.txt
  startCommand: python daily_horoscope_replace.py
  envVars:
    # ... другие переменные окружения ...
    
    # DALL-E image generation setting (true/false)
    - key: USE_DALLE_IMAGES
      value: "true"
    # Translation setting (true/false)
    - key: USE_TRANSLATIONS
      value: "true"
    # Ephemeris data inclusion setting (true/false)
    - key: USE_EPHEMERIS_DATA
      value: "true"
```

### Локальный шедулер (schedule_horoscopes.py)

```python
# Планируем запуск каждый день в 3:00 ночи
schedule.every().day.at("03:00").do(run_horoscope_generation)
```

## Контроль и управление функциями

### Переменные окружения

Через переменные окружения можно управлять разными аспектами генерации гороскопов:

- **USE_DALLE_IMAGES** - использование DALL-E для генерации изображений (true/false)
- **USE_TRANSLATIONS** - включение автоматического перевода гороскопов (true/false)
- **USE_EPHEMERIS_DATA** - включение астрономических данных (true/false)

### Запуск шедулера

Запуск шедулера осуществляется через скрипты:

- Windows: `run_horoscope_scheduler.bat`
- Linux/Mac: `run_horoscope_scheduler.sh`
- PowerShell: `run_horoscope_scheduler.ps1`

### Ручной запуск

Для ручного запуска генерации гороскопов:

```bash
python daily_horoscope_replace.py
```

## Интеграция астрономических данных

### Как это работает

1. Модуль `ephemeris.py` рассчитывает точные положения планет на текущую дату
2. Данные добавляются к запросу для OpenAI Assistant
3. Ассистент использует эти данные для генерации более точного и астрономически корректного гороскопа

### Что включено в данные эфемерид

- Положения планет и знаки зодиака
- Фаза луны
- Аспекты между планетами (соединения, трины, квадраты и т.д.)
- Величины яркости небесных тел

## Мониторинг и отладка

### Логи

Логи генерации гороскопов сохраняются в файле `horoscope_generator.log`
Логи работы шедулера сохраняются в файле `horoscope_scheduler.log`

Для проверки работы:
```bash
tail -f horoscope_generator.log
```

### Проверка работоспособности

Для проверки доступности и работоспособности эфемерид:
```bash
python test_ephemeris.py
```

## Дополнительная информация

Полная документация доступна в файлах:
- `docs/EPHEMERIS_INTEGRATION.md` - подробное описание интеграции эфемерид
- `docs/HOROSCOPE_SCHEDULER_UPDATE.md` - обновленная информация о шедулере

## Первоначальная настройка на сервере

После деплоя на новый сервер выполните:
```bash
bash init_scheduler.sh
```

Это создаст и запустит системный сервис для автоматического запуска шедулера даже после перезагрузки сервера.
