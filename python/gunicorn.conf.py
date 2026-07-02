# https://gunicorn.org/configure/
## https://gunicorn.org/reference/settings/
## https://oneuptime.com/blog/post/2026-02-03-python-uvicorn-production/view
bind = "0.0.0.0:8000"
workers = 4
accesslog = "-"
worker_class= "uvicorn_worker.UvicornWorker"
asgi_loop = "auto"

# To suppress 'ASGI 'lifespan' protocol appears unsupported.' messages
asgi_lifespan="off"