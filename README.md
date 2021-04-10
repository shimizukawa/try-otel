# OpenTelemetry demo with django/celery

## invoke docker components

* OpenTelemetry Collector process
* Jaeger process for TRACING monitor
* MySQL process for django app

```bash
$ cd $REPOROOT
$ cd docker
$ docker-compse up
```

And open http://localhost:16686/

## invoke django app and celery

setup

```bash
$ cd $REPOROOT
$ cd dj
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -U pip setuptools
(venv) $ pip install -r requirements.txt
```

invoke celery
```python
(venv) $ python <TBD>
```

invoke django
```python
(venv) $ python manage.py runserver
```

And open http://localhost:8000/

## run console client

setup

```bash
$ cd $REPOROOT
$ cd console
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -U pip setuptools
(venv) $ pip install -r requirements.txt
```

run client
```python
(venv) $ python client.py
```

