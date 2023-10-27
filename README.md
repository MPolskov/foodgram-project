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
Cоздать .env файл в корневой папке проекта (пример содержания в .env.example) 

Выполнить сборку Docker образов и применить миграции:
```
# Сборка образов:
docker compose up

# Миграции:
docker compose exec backend python manage.py migrate
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

### Автор
Полшков Михаил

