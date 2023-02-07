from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from .models import Dish


@shared_task
def notify():
    updated_dishes = Dish.objects.filter(last_update__gte=datetime.now() - timedelta(hours=24))
    users = User.objects.all()

    dishes = []
    for dish in updated_dishes:
        dishes.append(dish.title)
    
    mails = []
    for user in users:
        if user.email:
            mails.append(user.email)

    if len(dishes) > 0:
        if len(mails) > 0:
            for mail in mails:
                subject = 'List of recently added or updated dishes'
                message = f'Here is a list of recently added or updated dishes on our site {dishes}'
                send_mail(subject, message, 'restaurant@gmail.com', [mail])