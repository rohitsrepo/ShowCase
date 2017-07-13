from __future__ import absolute_import

from celery import shared_task
from .mails import send_interpret_added

@shared_task
def send_interpret_added_mail(interpretation_id):
    return send_interpret_added(interpretation_id)
