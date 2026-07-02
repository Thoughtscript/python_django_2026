# python_django_2026

[![](https://img.shields.io/badge/Python-3.12.3-yellow.svg)](https://www.python.org/downloads/) [![](https://img.shields.io/badge/Docker-blue.svg)](https://www.docker.com/) [![](https://img.shields.io/badge/MySQL-9.7.1-blue.svg)](https://dev.mysql.com/doc/refman/8.4/en/preface.html) [![](https://img.shields.io/badge/Django-6.0.6-green.svg)](https://www.djangoproject.com/) 

Spent a few hours refreshing/reviewing latest greatest Django in 2026.

## Comments

1. Adding some recent changes to an [existing barebones example](https://github.com/Thoughtscript/python_django_2024).
1. Incorporating and retaining a handful of overlooked, lesser-known, interesting, or advanced techniques from the former (or `6.x` documentation, dev blogs, etc.).
1. Curiosity about newer features.

## Use and Setup

```bash
docker compose up
```

> For simplicity's sake, I've left `sleep` commands within the [run.sh](./python/run.sh) executed on the `python` service start-run sequence. Such an approach is one of 2-3 that are often recommended in these scenarios. Why? Docker Compose healthchecks typically evaluate the state of the Container or general runtime (and not say the status of a Web Application running within such runtime), migrations vary a bit in terms of execution time, and lastly Docker Compose isn't typically used to deploy code to Production (only to run code locally on the same machine). 

> So, this is admittedly not ideal but I think suffices here to demonstrate basic Django initialization, launching, running, etc. easily and simply without much configuration fuss. However, one must a bit patient for the entire sequence to successfully complete. Please review and tweak the `run.sh` Bash command to your liking to optimizing for your local hardware.

Endpoints available after everything spins up:
1. http://localhost:8000/
1. http://localhost:8000/test
1. GET http://localhost:8000/api/examples
1. GET http://localhost:8000/api/subexamples
1. GET http://localhost:8000/api/subexamples/disjoint?name=sub_example_one
1. GET http://localhost:8000/api/examples/one?pk=3
1. PUT `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X PUT "http://localhost:8000/api/subexamples/update?sub_example_pk=1&example_pk=3" --insecure`
1. POST `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X POST "http://localhost:8000/api/examples/create" -d '{"name": "example"}' --insecure`
1. POST `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X POST "http://localhost:8000/api/subexamples/create" -d '{"name": "subexample"}' --insecure`
1. DELETE `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X DELETE "http://localhost:8000/api/examples/delete" -d '{"names_to_delete": ["example_one","example_two"]}' --insecure`

### Django Admin

Create Migrations:
1. `exec` into the Docker Container Interactive Terminal.
1. Due to the `dockerfile` configuration, it should drop you into the correct directory. Then run: `≈`. Django will automatically detect and pick up Models that have been added and create the necessary scripts to initialize the database.

## Techniques and Interesting Topics

1. Many [examples on the internet](https://adamj.eu/tech/2020/02/04/how-to-use-pymysql-with-django/) used to demonstrate the use of `Django` with `PyMySQL` but this is unnecessary for basic connections. It can be [configured without additional dependencies](./python/djangoexample/config/settings.py) (thereby reducing complexity, attack surface, configuration, distribution size, etc.) for examples such as this.
1. This uses [barebones configurations](./docker-compose.yml) for MySQL (e.g. - `MYSQL_ALLOW_EMPTY_PASSWORD`) which is useful for local, scratch-style, databases. This is using the official MySQL `environment` (ENV VAR) configuration and more closely corresponds to the actual settings one would configure in real-world professional scenarios (although one shouldn't use that setting Production obviously).
1. This uses `asgi` and `uvicorn-worker` for Asychronous support (an ongoing target in the [core Django specification](https://github.com/django/deps/blob/main/accepted/0009-async.rst#async-wrapper)). It also uses `gunicorn` to [manage](./python/run.sh) the Asynchronous `uvicorn` [workers](./python/gunicorn.conf.py) now. This is still the default configuration combination for Production deployments (combining `asgi` support with Worker Management).
1. A mostly Headless REST API with common CRUD operations. Why? It's standard-practice to seperate concerns by deploying compiled/transpiled/bundled/minified client-side sourcecode through Content Delivery Networks (since these are low latency, serve quickly through aggressive localized caching, reduce resource overhead from serving static content, reduce OWASP security concerns like [file directory traversal](https://owasp.org/www-community/attacks/Path_Traversal) vulnerabilities, etc.). I'vgunicoe left a View or two in here just for demostration purposes. For full-fledged React examples, please see my other demos.
1. Moving `manage.py` out of the default `django-admin startproject djangoexample` (initialization) root directory.
1. Uses modules (`__init__.py`) for better grouping and organization of default files, namespaces, etc. within the root directory. Remember that there are limits to this approach (`models.py` [remains reserved](https://docs.djangoproject.com/en/6.0/topics/db/models/) and cannot be replaced with `models/__init__.py`).
    * Make sure to double-check `imports` and paths! (Some frameworks now infer the file location.)
1. Seed data is injected at web application initialization (in addition to `migrations`) using [Command](https://docs.djangoproject.com/en/6.0/howto/custom-management-commands/).
1. Does not use [class-based generic views](https://docs.djangoproject.com/en/6.0/topics/class-based-views/generic-display/).
1. Uses [`@cache_page`](https://docs.djangoproject.com/en/6.0/ref/utils/#django.utils.functional.cached_property).
1. Uses `@cache_property`.
    * Caches on first access (by type or all instances of a type, not by specific instance).
    * Mutations are preserved.
    * Regeneration.
1. Regarding the **N+1 Problem**, this term is widely used. 
    * In Django this is usually the result of default **Lazy-Loading** (and generally that's true). `selected_related` for complex relationships (**Many-to-Many**, etc.)
    * In Java, ["Although this problem often is connected to lazy loading, it’s not always the case."](https://www.baeldung.com/spring-hibernate-n1-problem) - **Lazy-Loading** can solve certain really specific scenarios.
    * From core contributors to [Rails, Postgres](https://brandur.org/two-phase-render) - this problem is also not always solved the same way (**Eager-Loading**). In the example a **two-phase load and render** had to be implemented.
    * But to be clear though, Django also [sometimes requires](https://blog.sentry.io/finding-and-fixing-django-n-1-problems/) using `prefetch_related` which is arguably not **Eager**.
1. [QueryDict](https://docs.djangoproject.com/en/6.0/ref/request-response/#django.http.QueryDict) for parsing HTTP Query Parameters.
1. [Model Methods](https://docs.djangoproject.com/en/6.0/topics/db/models/#model-methods)
1. `.filter().first()` vs. `.get()`.
1. `asyncio` vs. `asgiref`:
    * `asyncio` - **keyword** syntax from core Python, handles asynchronous contexts under the hood.
    * `asgiref` - specific to Django/ORM, synchronous to asynchronous (and vice-versa) context switching, context preservation ([thread-local data](https://docs.python.org/3/library/threading.html#thread-local-data)), **wrapper** or **decorator**.
    * `@async_to_sync()` - More powerful than `asyncio` alone. [Runs the async function in a new sub-thread](https://docs.djangoproject.com/en/6.0/topics/async/#async-to-sync), supports threadlocals and thread_sensitive (running all `thread_sensitive=True` on the same but new thread or force a new thread if `False`).
1. Using `json.loads(serializers.serialize('json', scan))` and `JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)` for pleasing JSON HTTP Responses.
1. Confirming some basic `.exists()` and `is not None` comparisons.

## Resources and Links

1. https://github.com/Thoughtscript/python_django_2024
1. https://docs.djangoproject.com/en/6.0/releases/
1. https://docs.djangoproject.com/en/6.0/
1. https://docs.djangoproject.com/en/6.0/ref/settings/#databases
1. https://docs.djangoproject.com/en/6.0/internals/deprecation/
1. https://uvicorn.dev/settings/
1. https://medium.com/@toimrank/uvicorn-for-fastapi-00a1ddb5ca4d
1. https://oneuptime.com/blog/post/2026-02-03-python-uvicorn-production/view
1. https://gunicorn.org/configure/
1. https://gunicorn.org/reference/settings/
1. https://docs.djangoproject.com/en/6.0/topics/class-based-views/generic-display/
1. https://docs.djangoproject.com/en/6.0/ref/request-response/
1. https://docs.djangoproject.com/en/6.0/ref/request-response/#django.http.QueryDict
1. https://erdimollahseyin.medium.com/django-query-optimizations-how-to-make-your-app-faster-eb4b25877dce
1. https://docs.djangoproject.com/en/6.0/topics/db/models/#model-methods
1. https://engineering.kraken.tech/news/2026/01/12/using-django-async.html
1. https://docs.djangoproject.com/en/6.0/topics/async/#async-to-sync
1. https://docs.python.org/3/library/threading.html#thread-local-data
1. https://docs.djangoproject.com/en/6.0/howto/custom-management-commands/