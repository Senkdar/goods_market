# goods_market

## Описание
API сервиса для заказа товаров.
Для начала пользователю необходимо добавить товары, после чего создать заказ.  
Заказы могут быть одобрены или отклонены администратором.

## Для запуска проекта:  
1. Клонировать репозиторий и перейти в него в командной строке:

```bash
  git clone https://github.com/Senkdar/goods_market
  
  cd goods_market
```
2. Создать файл .env с настройками:
 ```
SECRET_KEY=<КЛЮЧ>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<ИМЯ БАЗЫ ДАННЫХ>
POSTGRES_USER=<ИМЯ ПОЛЬЗОВАТЕЛЯ>
POSTGRES_PASSWORD=<ПАРОЛЬ>
DB_HOST=db
DB_PORT=5432
```
3. Выполнить команды:
```
docker-compose up -d
docker-compose exec backend python manage.py migrate
```

4. Создать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
## API Reference

К проекту по адресу ```http://<ip-адрес>/doc/```
подключена документация API. В ней описаны возможные запросы к API и структура ожидаемых ответов.
