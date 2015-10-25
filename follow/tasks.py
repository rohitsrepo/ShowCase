from __future__ import absolute_import

from celery import shared_task
from .contacts import update_follow_from_social
from .mails import send_follow

@shared_task
def follow_from_social(access_id):
    return update_follow_from_social(access_id)

@shared_task
def send_follow_mail(user_id, target_user_id):
    return send_follow(user_id, target_user_id)
