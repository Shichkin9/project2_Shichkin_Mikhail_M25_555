# linux_practicum

***Проект "Примитивная база данных"***
***Описание***

Консольное приложение на Python, имитирующее работу с реляционной базой данных через интерактивный интерфейс. Позволяет создавать, удалять таблицы и управлять их структурой. Проект упакован как самостоятельный Python-пакет для установки через pip.
Технологический стек

    - Python 3.12+ - основной язык разработки
    - Poetry - управление зависимостями и сборка пакета
    - Ruff - линтинг и форматирование кода
    - PrettyTable - красивый вывод табличных данных
    - Prompt - удобный интерактивный ввод от пользователя
    - Git - контроль версий

***Структура проекта***


project2_Shichkin_Mikhail_M25_555/
├── src/primitive_db/          # Исходный код приложения
│   ├── __init__.py
│   ├── main.py               # Точка входа
│   ├── engine.py             # Игровой цикл и парсинг команд
│   ├── core.py               # Логика работы с таблицами
│   ├── utils.py              # Вспомогательные функции
│   └── constants.py          # Константы
├── pyproject.toml            # Конфигурация Poetry
├── poetry.lock               # Фиксированные зависимости
├── Makefile                  # Автоматизация команд
├── README.md                 # Документация
├── db_meta.json              # Файл метаданных БД
└── .gitignore

Установка (Ubuntu/Linux)
1. Предварительные требования
bash

# Проверьте версию Python и pip
python3 --version
python3 -m pip --version

# Если pip нет или устарел:
sudo apt update
sudo apt install python3-pip
python3 -m pip install --upgrade pip

2. Установка Poetry
bash

# Установите Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Добавьте Poetry в PATH (добавьте в ~/.bashrc или ~/.zshrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Проверьте установку
poetry --version

# Настройте создание виртуального окружения в проекте
poetry config virtualenvs.in-project true

# 3. Клонирование и установка проекта
bash

## Клонируйте репозиторий
git clone git@github.com:Shichkin9/project2_Shichkin_Mikhail_M25_555.git
cd project2_Shichkin_Mikhail_M25_555

## Установите зависимости
poetry install

## Активируйте виртуальное окружение
poetry shell

# 4. Установка пакета в систему
bash

## Соберите пакет
poetry build

## Установите собранный пакет
pip install dist/*.whl

Использование
Запуск приложения
bash

# После установки пакета
project

# Или через Poetry
poetry run project

Доступные команды
text

create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...
    Создать новую таблицу с указанными столбцами

drop_table <имя_таблицы>
    Удалить существующую таблицу

list_tables
    Показать список всех таблиц в базе

help
    Показать справку по командам

exit
    Выйти из приложения

Поддерживаемые типы данных: int, str, bool
Пример работы
text

***База данных***

Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

Введите команду: list_tables
- users

Введите команду: drop_table users
Таблица "users" успешно удалена

Введите команду: exit

Разработка
Автоматизация через Makefile
bash

make install      # Установка зависимостей
project     # Запуск приложения
make build        # Сборка пакета
make publish      # Тест публикации (dry-run)
make lint         # Проверка кода линтером

Проверка качества кода
bash

# Проверить весь проект
poetry run ruff check .

# Автоматически исправить ошибки
poetry run ruff check --fix .