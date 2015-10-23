from __future__ import absolute_import

from celery import shared_task
from follow.contacts import update_follow_from_social

@shared_task
def follow_from_social(access_id):
    update_follow_from_social(access_id)
