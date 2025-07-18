# Astrologs Wars

## Астрологический блог с персональными прогнозами

Проект представляет собой веб-приложение - астроблог с ежедневными гороскопами, предсказаниями и возможностью заказа персональных астрологических прогнозов.

## Основные функции

- **Главная страница** с блоками различных астрологических систем
- **Ежедневные гороскопы** из разных астрологических систем (Европейская, Китайская, Индийская астрология, Лал Китаб, Джйотиш, Нумерология, Таро, Планетарная астрология)
- **Магазин персональных астрологических прогнозов** с возможностью заказа и оплаты
- **Административный интерфейс** для управления контентом, категориями и товарами
- **Многоязычность** (Украинский, Английский, Русский, Немецкий)

## Технологии

- Flask (Python)
- SQLAlchemy
- Bootstrap
- JavaScript
- SQLite (для разработки)

## Установка и запуск

### Windows

```bash
# Запуск приложения
run_astro_site.bat
# или
run_astro_site.ps1
```

### Linux

```bash
# Запуск приложения
./run_astro_site.sh
```

## Структура проекта

- **app/** - основной код приложения
  - **main/** - основные маршруты
  - **blog/** - функционал блога
  - **blog_automation/** - автоматизация публикации прогнозов
  - **shop/** - функционал магазина персональных прогнозов
  - **admin/** - административный интерфейс
  - **static/** - статические файлы (CSS, JS, изображения)
  - **templates/** - шаблоны страниц

- **scripts/**
  - **setup_astro_blogs.py** - заполнение блога данными
  - **create_astro_products.py** - создание товаров астромагазина
  - **recreate_admin.py** - создание аккаунта администратора
  - **daily_horoscope_generator.py** - ежедневная генерация гороскопов
  - **schedule_horoscopes.py** - планировщик автоматической генерации гороскопов
  - **setup_astro_assistants.py** - настройка ассистентов для разных астрологических систем

## Автоматизация гороскопов

Проект включает систему автоматической генерации и публикации ежедневных гороскопов для 8 различных астрологических систем:

1. Европейская астрология
2. Китайская астрология
3. Индийская астрология
4. Лал Китаб
5. Джйотиш
6. Нумерология
7. Таро
8. Планетарная астрология

Генерация происходит ежедневно в 7:00 утра с использованием OpenAI API. Для запуска автоматизации:

### Windows
```
run_horoscope_scheduler.bat
```

### Linux
```
chmod +x run_horoscope_scheduler.sh
./run_horoscope_scheduler.sh
```

### PowerShell
```
.\run_horoscope_scheduler.ps1
```

## Доступ в админку

- **Логин:** andrii770
- **Пароль:** Dnepr75ok10

## Автор

Andrii
