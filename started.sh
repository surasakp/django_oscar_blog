#!/bin/bash

docker-compose -f docker/docker-compose.yml build --pull web_blog adhoc

docker-compose -f docker/docker-compose.yml run --rm web_blog pip install -r requirements.txt

docker-compose -f docker/docker-compose.yml run --rm web_blog python manage.py migrate

docker-compose -f docker/docker-compose.yml up --build