# Foodgram

Cервис для публикаций и обмена рецептами.

Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное и в список покупок, а также скачивать список покупок в txt-формате. Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.

![workflow](https://github.com/EscapeFromHell/foodgram-project-react/actions/workflows/main.yml/badge.svg)

> Сайт:
>> http://84.252.137.162/

## Технологии
Python 3.7.9, Django 3.2.7, Django REST Framework 3.12.4, PostgresQL, Docker, Yandex.Cloud.

## Env
- DJANGO_KEY= _здесь указать секретный ключ_
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=postgres
- POSTGRES_USER=_здесь задать имя пользователя БД_
- POSTGRES_PASSWORD=_здесь написать пароль от БД_
- DB_HOST=db
- DB_PORT=5432

## Запуск проекта локально
- После скачивания проекта, перейдите в папку проекта и установите виртуальное окружение.

python -m venv venv

- Активируйте его

source venv/scripts/activate

- Перейдите в папку Backend

cd backend/

- Установите зависимости из файла requirements.txt

pip install -r requirements.txt

- Выполните команду

python manage.py runserver

## Запуск в контейнерах
- Для сборки образов и контейнеров перейдите в папку infra

cd infra/

- Выполните команду

docker-compose up -d --build 
