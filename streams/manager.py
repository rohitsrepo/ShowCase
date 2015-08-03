from .conf import USER_FEED
from django.db.models.signals import post_delete, post_save
from streams.client import stream_client

def get_feed(feed, user_id):
        return stream_client.feed(feed, user_id)

def activity_created(sender, instance, created, raw, **kwargs):
    if created and not raw:
        activity = instance.create_activity()
        feed_type = USER_FEED
        feed = get_feed(feed_type, instance.activity_actor_id)
        result = feed.add_activity(activity)
        return result

def activity_delete(sender, instance, **kwargs):
    feed_type = USER_FEED
    feed = get_feed(feed_type, instance.activity_actor_id)
    result = feed.remove_activity(foreign_id=instance.activity_foreign_id)
    return result

def bind_stream(sender, **kwargs):
    post_save.connect(activity_created, sender=sender)
    post_delete.connect(activity_delete, sender=sender)