# Shorty.

This is a demo project of the link reduction service.

## Dependencies

* Python 3.10
* MySQL
* Redis

## Get up and running

1. Clone this repo
2. Create a virtual environment and install the requirements:

```
cd shorty_django
pipenv install
```

3. Initialize virtual environment:

```
pipenv shell
```

4. Create a file named `.env`

Inside add:

```
SECRET_KEY={create_and_add_your_own_SECRET_KEY_here_with_no_spaces}
DEBUG=True
# mysql
DB_HOST={your_host}
DB_PORT={post}
DB_NAME={database}
DB_USER={user}
DB_PASSWORD={password}
# redis 
REDIS_LOCATION={location}
```

NOTE:

For more information on how you can generate a secret key visit [here](https://foxrow.com/generating-django-secret-keys)
or you can generate a key online [here](https://www.miniwebtool.com/django-secret-key-generator/).
For redis, see [here](https://github.com/jazzband/django-redis).

5. Run migrations:

```
python manage.py migrate
```

6. Run collect static:

```
python manage.py collectstatic
```

7. Get the server up and running:

```
python manage.py runserver
```
