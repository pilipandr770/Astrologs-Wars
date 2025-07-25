# Руководство по интеграции генерации изображений в гороскопы

## Введение

В этом документе описывается интеграция процесса генерации изображений в ежедневный процесс создания гороскопов для астрологических блоков. Новый скрипт `daily_horoscope_with_images.py` объединяет функциональность генерации текстов гороскопов с созданием уникальных тематических изображений для каждого блока.

## Что делает скрипт

1. Создает текстовый контент гороскопов для 8 астрологических систем
2. Генерирует уникальные изображения для каждого гороскопа с:
   - Звездным фоном
   - Созвездиями
   - Визуальными элементами, уникальными для каждой системы
   - Заголовком и подзаголовком
3. Сохраняет изображения в директории `app/static/uploads/blog/`
4. Обновляет записи в базе данных, включая поле `featured_image` с именем файла изображения
5. Поддерживает многоязычность

## Как использовать

### Запуск скрипта

Для Windows:
```
run_horoscope_with_images.bat
```

Для PowerShell:
```
.\run_horoscope_with_images.ps1
```

Для Linux/Mac:
```
python daily_horoscope_with_images.py
```

### Периодический запуск

Рекомендуется настроить запуск скрипта через планировщик задач:

1. **Windows Task Scheduler**:
   - Создать задачу с ежедневным запуском
   - Действие: запуск `run_horoscope_with_images.bat`

2. **Cron (Linux/Mac)**:
   ```
   0 0 * * * cd /path/to/work-site && python daily_horoscope_with_images.py
   ```

## Настройка и расширение

### Добавление новых астрологических систем

Для добавления новой системы измените массив `systems` в функции `generate_daily_horoscopes`:

```python
systems = [
    {"name": "Западная астрология", "position": 1},
    {"name": "Китайская астрология", "position": 2},
    # Добавьте новую систему:
    {"name": "Новая система", "position": 9}
]
```

### Настройка внешнего вида изображений

Функция `create_astrology_image` может быть изменена для настройки:
- Размера изображений (`width`, `height`)
- Цветовой палитры (`colors`)
- Элементов дизайна (звезды, планеты, созвездия)
- Шрифтов и текста

## Решение проблем

### Типичные проблемы и решения

1. **Отсутствуют изображения на сайте**:
   - Проверьте, что директория `app/static/uploads/blog/` существует и доступна для записи
   - Убедитесь, что скрипт успешно создает файлы (проверьте лог-файл)

2. **Ошибки при создании изображений**:
   - Возможно, отсутствуют необходимые шрифты - скрипт должен корректно обрабатывать эту ситуацию
   - Проверьте установку библиотеки Pillow (`pip install Pillow`)

3. **Изображения создаются, но не отображаются в блоге**:
   - Проверьте значение поля `featured_image` в базе данных
   - Проверьте пути к файлам в шаблоне блога

## Примечания

1. Скрипт генерирует уникальные изображения для каждой системы, используя разные цвета и случайные узоры
2. Имена файлов формируются по шаблону: `astro_{system_number}_{date}.png`
3. Ежедневный запуск заменит предыдущие изображения для каждого блока
