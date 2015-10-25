from __future__ import absolute_import

from celery import shared_task
from .mails import send_added_to_bucket

@shared_task
def send_added_to_bucket_mail(bucket_membership_id):
    return send_added_to_bucket(bucket_membership_id)
