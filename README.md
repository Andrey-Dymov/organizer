# Личный Органайзер на Kivy

Многофункциональное приложение для управления личной информацией, разработанное с использованием фреймворка Kivy и KivyMD.

## Функциональность

Приложение включает три основных раздела:

- **Контакты** - управление контактной информацией (имя, телефон, адрес)
- **Книги** - отслеживание прочитанных и планируемых к прочтению книг
- **Фильмы** - каталогизация просмотренных и планируемых к просмотру фильмов и сериалов

## Особенности

- Современный Material Design интерфейс
- Хранение данных в JSON-файлах
- Группировка записей по категориям
- Удобные формы для добавления и редактирования записей
- Статусы для отслеживания прогресса (план, в процессе, завершено)

## Требования

- Python 3.6+
- Kivy 2.2.1
- KivyMD 1.1.1

## Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/ваш-аккаунт/personal-organizer.git
cd personal-organizer
```

2. Установите зависимости:
```
pip install -r requirements.txt
```

3. Запустите приложение:
```
python main.py
```

## Структура проекта

```
├── main.py           # Основной файл приложения
├── requirements.txt  # Зависимости проекта
├── models/           # Модели данных и формы
│   ├── __init__.py
│   ├── base.py       # Базовый класс для менеджеров данных
│   ├── book_form.py  # Форма для книг
│   ├── book_list.py  # Список книг
│   ├── movie_form.py # Форма для фильмов
│   ├── movie_list.py # Список фильмов
│   ├── contact_form.py # Форма для контактов
│   └── contact_list.py # Список контактов
└── db/               # Директория для хранения данных
    ├── books.json    # Данные о книгах
    ├── movies.json   # Данные о фильмах
    └── contacts.json # Данные о контактах
```

## Скриншоты

![Главный экран](https://via.placeholder.com/800x600.png?text=Главный+экран)
![Форма редактирования](https://via.placeholder.com/800x600.png?text=Форма+редактирования)

## Лицензия

MIT

## Автор

Ваше имя 