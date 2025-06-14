# КадроМастер (Дипломный проект)
Веб-приложение для автоматизации кадрового учёта.

## Функциональность
* Аутентификация и авторизация
* Управление пользователями и группами
* Администрирование структуры компании
* Учет рабочего времени и аналитика
* Финансовый учет

## Технологии
* Python 3.8+
* Django
* MySQL
* HTML/CSS/JavaScript/AJAX

## Старт проекта
1) Клонирование репозитория
```bash
git clone https://github.com/n0maCi/KadroMaster.git
cd KadroMaster
```
2) Создание venv
```bash
python -m venv .venv
# Активировать его
.venv\Scipts\Activate.ps1
```
3) Установка библиотек
```bash
pip install -r requirements.txt
```
4) Запуск проекта
```bash
cd KadroMaster
python manage.py runserver
```

## Примечание
* Можно использовать готовый дамп БД https://github.com/n0maCi/KadroMaster/blob/main/Dump.sql
* Настройка базы происходит в https://github.com/n0maCi/KadroMaster/blob/main/KadroMaster/KadroMaster/settings.ini
