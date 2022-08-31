# OpenTelemetry demo with django/celery

OpenTelemetry DEMO for:

* Python
* Django
* MySQL with Django ORM
* Python logging
* Redis
* Celery
* requests

## invoke docker components

* OpenTelemetry Collector process
* Jaeger process for TRACING monitor
* MySQL process for django app

```bash
$ docker compse up
```

And open http://localhost:16686/

## invoke django app and celery

setup

```console
$ cd dj
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser --username=joe --email=joe@example.com
```

invoke celery
```console
$ python <TBD>
```

invoke django
```console
$ python manage.py runserver
```

And open http://localhost:8000/

## run console client

setup

```console
$ cd console
$ pip install -r requirements.txt
```

run client
```console
$ python client.py
```

