#!/bin/bash

function gen_secret_key() { python -c "from secrets import token_urlsafe;print(f'SECRET_KEY={token_urlsafe(64)}')"; }
function gen_password() { python -c "import string; import random; password = ''.join(random.choices(string.digits + string.ascii_letters + string.punctuation, k=20)); print(f'DB_PASSWORD={password}')"; }
echo "DEBUG=True" > .env
gen_secret_key >> .env
echo "DB_HOST=db" >> .env  # default value for docker
echo "DB_NAME=db_shorty" >> .env
echo "DB_USER=root" >> .env
gen_password >> .env
echo "REDIS_LOCATION=redis://cache:6379" >> .env  # default value for docker
