# OpenTelemetry demo with django/celery

This is a OpenTelemetry DEMO.

Applications:

* Nginx as Web Server (TRACE)
* WSGI as Python Web Application Server (TRACE, METRIC)
* Django as Python Web Application Server (TRACE, METRIC, LOG)
* Django ORM with Postgres (TRACE, LOG)
* Python logging (LOG)
* Requests as Python HTTP Client (TRACE, LOG)
* React as Web Frontend by JavaScript (TRACE, LOG)
* Postgres (NOT READY)
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
$ docker compose up
```

And open:

* Uptrace:http://uptrace.lvh.me/  - Select "My project" from Top-Left dropdown.
- Jaeger: http://jaeger.lvh.me/
- Zipkin: http://zipkin.lvh.me/
- Prometheus: http://prometheus.lvh.me/
- Email: http://mailhog.lvh.me/

## invoke django app and celery

setup

```console
$ docker compose run --rm backend python manage.py migrate
$ docker compose run --rm backend python manage.py createsuperuser --username=joe --email=joe@example.com
```

invoke celery (NOT READY)
```console
$ python <TBD>
```

invoke django
```console
$ docker compose run --rm backend
```

And open http://api.lvh.me/

## Run console client

run client with **manual** instrumentation

```console
$ docker compose run --rm console
```

run client with **auto** instrumentation

```console
$ docker compose run --rm console-auto
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

And open http://lvh.me/
