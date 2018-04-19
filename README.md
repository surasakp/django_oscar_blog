# Project Django Oscar Blog

Develop blog with Oscar framework

## Install docker
- for Ubutu go to this page `https://docs.docker.com/install/linux/docker-ce/ubuntu/` and follow first step

- for Window go to this page `https://docs.docker.com/docker-for-windows/install/` and follow first step

- for Mac go to this page `https://docs.docker.com/docker-for-mac/install/` and follow first step

## How to run develop environment
1 change diractory to folder django_oscar_blog

2 run this command `docker-compose -f docker/docker-compose.yml build --pull web_blog` pull service image web_blog

3 run this command `docker-compose -f docker/docker-compose.yml run --rm web_blog pip install -r requirements.txt` for run service without service web_blog and install python package requirements file in developer environment

4 run this command `docker-compose -f docker/docker-compose.yml run --rm web_blog python manage.py migrate` for run service without service web_blog and migrate database in developer environment

5 run this command `docker-compose -f docker/docker-compose.yml up -d --build` for start services in detached mode

6 in web browser go to `http://localhost/8000` to view oscar homepage

## How to stop develop environment
- run this command `docker-compose -f docker/docker-compose.yml stop` for stop all services
