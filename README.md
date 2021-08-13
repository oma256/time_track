# Work Time

# Описание проекта
Административная панель а также `API` для `iOS/Android` приложений, 
для предоставления потенциальным клиентам/партнерам возможность
получать отчетную информацию о посещаемости/опозданиях своих 
сотрудников на работу, посредством факта фиксации прибытия/убытия сотрудника 
на рабочее место с помощью `QR-код` технологии.

# Как поднять локально проект?
Зависимости:
- Nginx
- PostgreSQL
- Python 3.7
- Django 2.2
- gunicorn

## Переменные окружения для продакшена, для локальной разработки можно и не указывать:
| Key    | Description   |    Default value  |
| :---         |     :---      |          :--- |
| `DJANGO_SECRET_KEY`  | secret key  | secret-key              |
| `DJANGO_DEBUG`  | Debug mode True or False  | True              |
| `DJANGO_ALLOWED_HOST`| Allowed host | 0.0.0.0,127.0.0.1 |
| `DEFAULT_DATABASE_URL`  | postgres://user:password@host:port/database_name | postgres://postgres:postgres@db:5432/video_converter |

## Последовательность действий
```.bash
    $ git clone https://gitlab.com/sunrise-studio/worktime-backend.git
    $ cd worktime-backend/ 
    $ virtualenv venv
    $ pip install -r requirements/local.txt
```
Необходимо создать в PostgreSQL создать БД:
```.bash
    $ sudo -u postgres psql
    $ create database worktime_db encoding 'UTF-8';
    $ \q
```
После создания БД, необходимо применить миграцию, после запуск тестового сервера:
```.bash
    $ python manage.py migrate
    $ python manage.py runserver
```
Если все успешно то переходите по ссылке ==> `http://locahost:8000`
