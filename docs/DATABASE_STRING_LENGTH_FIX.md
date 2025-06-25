# Исправление проблем со строками в базе данных

## Проблема

В процессе работы скрипта `daily_horoscope_replace.py` была обнаружена ошибка, связанная с длиной строк, сохраняемых в базе данных:

```
Error processing system 8: (psycopg2.errors.StringDataRightTruncation) value too long for type character varying(255)
```

Эта ошибка возникала при попытке сохранить значения в поля `title_ru`, `title_en`, `title_de`, `summary_ru`, `summary_en` и `summary_de`, которые имеют ограничение по длине (255 символов) в базе данных.

## Решение

1. Добавлена функция `truncate_string_safe()`, которая безопасно обрезает строки, превышающие заданную длину:

```python
def truncate_string_safe(value, max_length=255):
    """
    Safely truncate a string to the specified length
    
    Args:
        value (str): String to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated string
    """
    if value is None:
        return None
        
    if isinstance(value, str) and len(value) > max_length:
        logger.warning(f"Truncating value from {len(value)} to {max_length} characters")
        return value[:max_length-3] + '...'
    return value
```

2. Обновлены все места в коде, где происходит присвоение значений полям базы данных, для использования функции `truncate_string_safe()`
   - При создании нового блока
   - При обновлении существующего блока
   - При сохранении переведенных значений

## Где применяется обрезка

- Поля заголовков (`title`, `title_ua`, `title_en`, `title_de`, `title_ru`)
- Поля сводок (`summary`, `summary_ua`, `summary_en`, `summary_de`, `summary_ru`)

Поля с содержимым (`content`, `content_ua`, `content_en`, `content_de`, `content_ru`) не обрезаются, поскольку они имеют тип `TEXT` в базе данных, который позволяет хранить строки неограниченной длины.

## Логирование

Если значение обрезается, в лог записывается предупреждение:

```
Truncating value from X to 255 characters
```

где X - исходная длина строки.

## Рекомендации

В будущем рекомендуется:
1. Рассмотреть возможность увеличения длины полей в базе данных (особенно для title_* и summary_*)
2. Ограничить длину текста на стороне генерации (через инструкции для OpenAI API)
3. Добавить проверку длины строк во всех местах, где происходит запись в базу данных
