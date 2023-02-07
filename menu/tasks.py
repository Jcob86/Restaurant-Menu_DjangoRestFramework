from celery import shared_task



@shared_task
def add():
    return "sending 1000 emails"