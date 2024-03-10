from celery import Celery


BROKER_URL = "redis://localhost:6379/0"
BACKEND_URL = "redis://localhost:6379/1"

cel = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL)


@cel.task(name="Add two numbers")
def add(x, y):
    return x + y


@cel.task(name="Sub two numbers")
def sub(x, y):
    return x - y
