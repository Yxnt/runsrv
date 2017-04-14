from apps import celery
from flask import current_app


@celery.task
def system_operator(key,value):
    current_app.redis.hset('celery:task:system',key,value)