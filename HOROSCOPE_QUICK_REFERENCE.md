# Справочная карточка: Генерация гороскопов с изображениями

## Быстрый старт

1. **Запуск генерации с заменой старых гороскопов**:
   - Windows: `run_horoscope_replace.bat`
   - PowerShell: `.\run_horoscope_replace.ps1`
   - Linux/Mac: `./run_horoscope_replace.sh`

2. **Проверка результатов**:
   - Проверка БД: `python check_horoscope_images.py`
   - Проверка файлов: `dir app\static\uploads\blog\astro_*.png`

## Основные файлы

- `daily_horoscope_replace.py` - скрипт замены гороскопов с очисткой старых изображений
- `check_horoscope_images.py` - проверка обновлений в БД
- `force_cleanup_horoscope_images.py` - принудительная очистка старых изображений

## Плановое обслуживание

1. **Ручная очистка старых изображений** (если требуется):
   - `python force_cleanup_horoscope_images.py` (оставит только последние изображения)

2. **Документация**:
   - `HOROSCOPE_IMAGES_INTEGRATION_GUIDE.md` - подробная документация
   - `HOROSCOPE_IMAGE_FIX_FINAL_REPORT.md` - отчет о решении проблемы
   - `HOROSCOPE_REPLACEMENT_MODE.md` - описание режима замены

## Диагностика проблем

1. **Изображение не создается**:
   - Проверьте логи в `horoscope_generator.log`
   - Проверьте права доступа к директории `app/static/uploads/blog/`
   - Проверьте наличие библиотеки Pillow: `pip install Pillow`

2. **Изображения не отображаются**:
   - Проверьте значения в БД: `python check_horoscope_images.py`
   - Проверьте наличие файлов в директории
   - Проверьте шаблон блога на правильные пути к файлам
