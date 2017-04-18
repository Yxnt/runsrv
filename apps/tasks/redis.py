from apps import celery
from flask import current_app


@celery.task
def system_operator(key, value):
    current_app.redis.hset('celery:task:system', key, value)


@celery.task
def redis_save(key, value):
    current_app.redis.set(key, value, time=24 * 3600)
