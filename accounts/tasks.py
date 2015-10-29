from __future__ import absolute_import

from celery import shared_task
from .mails import send_welcome, send_warm_welcome, send_reset_password

@shared_task
def send_warm_welcome_mail(user_id):
    return send_warm_welcome(user_id)

@shared_task
def send_welcome_mail(user_id):
    return send_welcome(user_id)

@shared_task
def send_reset_password_mail(user_id, reset_url):
    return send_reset_password(user_id, reset_url)
