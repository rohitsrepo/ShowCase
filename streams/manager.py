from .conf import USER_FEED, NEWS_FEEDS, BUCKET_FEED
from django.db.models.signals import post_delete, post_save
from streams.client import stream_client

def get_feed(feed, user_id):
        return stream_client.feed(feed, user_id)

def activity_created(sender, instance, created, raw, **kwargs):
    if created and not raw:
        activity_data = instance.create_activity()
        for data in activity_data:
            feed_type = data['feed_type']
            feed = get_feed(feed_type, data['feed_id'])
            feed.add_activity(data['activity'])

def activity_delete(sender, instance, **kwargs):
    feed_type = USER_FEED
    feed = get_feed(feed_type, instance.activity_actor_id)
    result = feed.remove_activity(foreign_id=instance.activity_foreign_id)
    return result

def bind_stream(sender, **kwargs):
    post_save.connect(activity_created, sender=sender)
    post_delete.connect(activity_delete, sender=sender)

def get_user_feed(user_id, feed_type=None):
        if feed_type is None:
            feed_type = USER_FEED
        feed = stream_client.feed(feed_type, user_id)
        return feed

def get_feed(feed, user_id):
        return stream_client.feed(feed, user_id)

def get_news_feeds(user_id):
    feeds = {}
    for feed in NEWS_FEEDS:
        feeds[feed] = get_feed(feed, user_id)
    return feeds

def follow_user(user_id, target_user_id):
    news_feeds = get_news_feeds(user_id)
    target_feed = get_user_feed(target_user_id)
    for feed in news_feeds.values():
        feed.follow(target_feed.slug, target_feed.user_id)

def unfollow_user(user_id, target_user_id):
    news_feeds = get_news_feeds(user_id)
    target_feed = get_user_feed(target_user_id)
    for feed in news_feeds.values():
        feed.unfollow(target_feed.slug, target_feed.user_id)

def get_bucket_feed(bucket_id, feed_type=None):
        if feed_type is None:
            feed_type = BUCKET_FEED
        feed = stream_client.feed(feed_type, bucket_id)
        return feed

def follow_bucket(user_id, target_bucket_id):
    news_feeds = get_news_feeds(user_id)
    target_feed = get_bucket_feed(target_bucket_id)
    for feed in news_feeds.values():
        feed.follow(target_feed.slug, target_feed.user_id)

def unfollow_bucket(user_id, target_bucket_id):
    news_feeds = get_news_feeds(user_id)
    target_feed = get_bucket_feed(target_bucket_id)
    for feed in news_feeds.values():
        feed.unfollow(target_feed.slug, target_feed.user_id)
