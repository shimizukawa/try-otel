# OpenTelemetry demo with django/celery

OpenTelemetry DEMO for:

* Python
* Django
* Postgres with Django ORM
* Python logging
* Redis
* Celery
* requests

## invoke docker components

* OpenTelemetry Collector process
* Jaeger process for TRACING monitor
* Zipkin process for TRACING monitor
* Prometheus process for Metrics monitor
* Postgres process for django app

```bash
$ docker compse up
```

And open:

- Jaeger: http://localhost:16686/
- Zipkin: http://localhost:9411/
- Prometheus: http://localhost:9090/

## invoke django app and celery

setup

```console
$ cd backend
$ pip install -r requirements.txt -c ../constraints.txt
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
$ pip install -r requirements.txt -c ../constraints.txt
```

run client
```console
$ python client.py
```

## run react frontend

setup

```console
$ cd frontend
$ npm install
```

run client
```console
$ npm run dev
```

And open http://localhost:3000 (instead of 127.0.0.1:3000 !)
