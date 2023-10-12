# nimagaplar.uz Yangiliklar filter service

![image](main.jpg)

## Live: [nimagaplar.uz](http://65.109.138.63/))

![python](https://img.shields.io/badge/-python-grey?style=for-the-badge&logo=python&logoColor=white&labelColor=306998)
![django](https://img.shields.io/badge/-django-grey?style=for-the-badge&logo=django&logoColor=white&labelColor=092e20)
![MySQL](https://img.shields.io/badge/-django-grey?style=for-the-badge&logo=django&logoColor=white&labelColor=092e20)
![ElasticSearch](https://img.shields.io/badge/-django-grey?style=for-the-badge&logo=django&logoColor=white&labelColor=092e20)
![Cronjobs](https://img.shields.io/badge/-django-grey?style=for-the-badge&logo=django&logoColor=white&labelColor=092e20)
![Redis](https://img.shields.io/badge/-django-grey?style=for-the-badge&logo=django&logoColor=white&labelColor=092e20)
![linux](https://img.shields.io/badge/linux-grey?style=for-the-badge&logo=linux&logoColor=white&labelColor=072c61)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![HTML](https://img.shields.io/badge/-html/css-grey?style=for-the-badge&&logoColor=white&labelColor=306998)


### Language: python 3.9 +

### Frameworks : Django 4+

### Technologies: ElasticSearch, Redis, CronJobs, BeautifulSoup

### Deployment: gunicorn, NGINX, Docker, docker-compose

### Database : MySql+



# About

Easy Search and Filter news that are real time scraped from several news websites. Stamming words, and get keywords to see most commond words in news.

#### Django project run

```bash
>>> docker-compose -f docker-compose.prod.yaml up -d --build
```
#### Build Index for database

```
>>> docker exec -it django_container /bin/bash

>>> python3 manage.py search-index --build
```


# Architecture

## Docker Container: 

```
CONTAINER ID   IMAGE                    COMMAND                  CREATED        STATUS          PORTS                                                  NAMES
080ef6c82397   redis:alpine             "docker-entrypoint.s…"   9 months ago   Up 19 minutes   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp              nimagaplar_redis_1
c2987c14e09a   nimagaplar_nginx         "/docker-entrypoint.…"   9 months ago   Up 19 minutes   0.0.0.0:80->80/tcp, :::80->80/tcp                      nimagaplar_nginx_1
4913766d9e4c   nimagaplar_celery-beat   "sh /django/entrypoi…"   9 months ago   Up 19 minutes                                                          nimagaplar_celery-beat_1
e5c0d27cc945   nimagaplar_celery        "sh /django/entrypoi…"   9 months ago   Up 19 minutes                                                          nimagaplar_celery_1
daff97d12fa9   app:django               "sh /django/entrypoi…"   9 months ago   Up 19 minutes   8000/tcp                                               django_container
7d8440225e27   elasticsearch:8.4.0      "/bin/tini -- /usr/l…"   9 months ago   Up 19 minutes   0.0.0.0:9200->9200/tcp, :::9200->9200/tcp, 9300/tcp    nimagaplar_es_1
6383db947b1b   mysql:8                  "docker-entrypoint.s…"   9 months ago   Up 19 minutes   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060/tcp   nimagaplar_mysql_1
```

```
.
└── app
    └── nutrition
        ├──  migrations
        ├──  __init__.py
        ├──  admin.py
        ├──  apps.py
        ├──  models.py
        ├──  serializer.py
        ├──  service.py
        ├──  tests.py
        ├──  urls.py
        ├──  views.py
    └──  config
        ├──  __init__.py
        ├──  asgi.py
        ├──  urls.py
        ├──  settings.py
        ├──  wsgi.py
        
    ├── .gitignore
    ├── .gitlab-ci.yml
    ├──  manage.py
    ├──  requirements.txt
```

### models.py

```python
from core.base_model import BaseModel
from django.db import models


class MyModel(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
```

### views.py

## urls.py

```python
from django.urls import path

'from .views import MyView'

urlpatterns = [
    path("article/", views.article, name="article"),
]
```

### main.urls.py

```python
from django.urls import path, include

urlpatterns = [
    path('/api/v1/{app_name}/', include('{app_name.urls}'))
]
```
