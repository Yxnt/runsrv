from apps import celery


@celery.task
def hello():
    print("123123")
    return "hello"
