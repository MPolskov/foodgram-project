# Проект Foodgram
### Описание
Учебный проект по Django REST framework.

Cайт для публикации рецептов блюд.
Возможности:
- публиковать рецерты блюд;
- добавлять блюда в избоанное и список покупок;
- подписываться на других авторов;
- выгружать ингредиенты из блюд, добавленных в список покупок, в текстовый файл;
- доступна фильтрация по тегам, автору.

### Технологии
* Python 3.9
* Django 3.2
* Django REST framework 3.12
* Djoser 2.1

## Установка и запуск проекта локально:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:MPolskov/foodgram-project-react.git
```
```
cd foodgram-project-react
```

Выполнить сборку Docker образов:
```
docker compose up
```
Список ингредиентов можно загрузить из csv коммандой:
```
docker compose exec backend python manage.py load_data -i
```

## Развертывание проекта на рабочем сервере:
```
# загрузка и развертывание контейнеров: 
sudo docker compose -f docker-compose.production.yml up -d
# применение миграций:
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
# сборка статики backend:
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --no-input
```

## Размещение учебного проекта: 

https://mpolsh-foodgram.ddns.net/recipes

Данные для входа суперпользователя:
email: super@user.ru
password: admin

### Автор
Полшков Михаил

