from __future__ import absolute_import

from celery import shared_task

from .mails import send_admired

@shared_task
def send_admired_mail(admiration_id):
    return send_admired(admiration_id)
