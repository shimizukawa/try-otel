# OpenTelemetry demo with django/celery

This is a OpenTelemetry DEMO.

Applications:

* Django as Python Web Application Server
* Postgres with Django ORM
* Python logging
* Requests as Python HTTP Client
* React as Web Frontend by JavaScript
* Redis (NOT READY)
* Celery (NOT READY)

Monitoring/Visualizing

* OpenTelemetry Collector process
* Uptrace monitor
* Jaeger process for TRACING monitor
* Zipkin process for TRACING monitor
* Prometheus process for Metrics monitor

Email server

* MailHog to receive alert

## invoke docker components

```bash
$ docker compse up
```

And open:

* Uptrace:http://localhost:14318/
- Jaeger: http://localhost:16686/
- Zipkin: http://localhost:9411/
- Prometheus: http://localhost:9090/
- Email: http://localhost:8025/

## invoke django app and celery

setup

```console
$ cd backend
$ pip install -r requirements.txt -c ../constraints.txt
$ python manage.py migrate
$ python manage.py createsuperuser --username=joe --email=joe@example.com
```

invoke celery (NOT READY)
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
