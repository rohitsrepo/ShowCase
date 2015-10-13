from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from ShowCase.slugger import unique_slugify

from accounts.models import User
from admirations.models import Admiration
from bookmarks.models import BookMark
from compositions.models import Composition
from compositions.imageTools import compress
from feeds.models import Fresh, bind_fresh_feed, Staff, bind_staff_feed
from posts.models import Post, bind_post


def get_upload_file_name_background(instance, filename):
    return '%s/buckets/%s' % (instance.owner.id, filename.split('/')[-1] + '.jpg')

class Bucket(models.Model):
    name = models.CharField(max_length=25, blank=False)
    description = models.CharField(max_length=111, blank=True)
    background = models.ImageField(upload_to=get_upload_file_name_background, blank=True, null=True)
    compositions = models.ManyToManyField(Composition, related_name='holders', through='BucketMembership')
    slug = models.SlugField(max_length=100, unique=True)
    views = models.IntegerField(default=0)

    owner = models.ForeignKey(User, related_name='buckets')
    created = models.DateTimeField(auto_now_add=True)
    bookers = GenericRelation(BookMark, related_query_name='booked_buckets')
    admirers = GenericRelation(Admiration, related_query_name='admired_buckets')

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Bucket, self).save(*args, **kwargs)

        if self.background:
            compress(self.background.path)

    def get_absolute_url(self):
        return '/@' + self.owner.slug + '/series/' + self.slug

    def has_ownership(self, user_id):
        return self.owner.id == user_id

    @property
    def compositions_count(self):
        return self.compositions.all().count()

    @property
    def has_background(self):
        return bool(self.background)

    @property
    def background_url(self):
        try:
            return self.background.url
        except ValueError:
            pass

    @property
    def picture(self):
        try:
            return self.background.url
        except:
            try:
                composition = self.compositions.exclude(nsfw=True).order_by('bucketmembership__added').last()
                return composition.get_350_url()
            except:
                return ''

    def is_bookmarked(self, user_id):
        return self.bookers.filter(owner=user_id).exists()

    @property
    def bookmarks_count(self):
        return self.bookers.count()

    def is_admired(self, user_id):
        return self.admirers.filter(owner=user_id).exists()

    @property
    def admirers_count(self):
        return self.admirers.count()

    def add_to_staff_feed(self):
        Staff.objects.create(feed_type=Staff.BUCKET,
            content_object=self)

    def is_composition_added(self, composition_id):
        return self.compositions.filter(id=composition_id).exists()

    def getNotificationTarget(self, post):
        if post.post_type == Post.BUCKET:
            targets = [post.composition.artist]
            if not (post.composition.artist.id == post.composition.uploader.id):
                targets.append(post.composition.uploader)

            return targets

        elif post.post_type == Post.ADMIRE_BUCKET:
            return [self.owner]

        return None


class BucketMembership(models.Model):
    bucket = models.ForeignKey(Bucket, related_name='membership')
    composition = models.ForeignKey(Composition)
    added = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, blank=True)

    def add_to_fresh_feed(self):
        if self.bucket.compositions.count() >= 3 and not self.get_fresh_post().exists():
            Fresh.objects.create(feed_type=Fresh.BUCKET,
                content_object=self.bucket)

    def get_fresh_post(self):
        return Fresh.objects.filter(feed_type=Fresh.BUCKET,
                object_id=self.bucket.id,
                content_type=ContentType.objects.get_for_model(Bucket))

    def remove_fresh_post(self):
        try:
            if bucket.compositions.count() == 0:
                Fresh.objects.filter(feed_type=Fresh.BUCKET,
                    object_id=self.bucket.id,
                    content_type=ContentType.objects.get_for_model(Bucket)).delete()
        except:
            pass

    def remove_staff_post(self):
        try:
            if bucket.compositions.count() == 0:
                Staff.objects.filter(feed_type=Fresh.BUCKET,
                    object_id=self.bucket.id,
                    content_type=ContentType.objects.get_for_model(Bucket)).delete()
        except:
            pass

    def add_to_staff_feed(self):
        if self.bucket.compositions.count() > 5 and not self.get_staff_post().exists():
            Staff.objects.create(feed_type=Staff.BUCKET,
                content_object=self.bucket)

    def get_staff_post(self):
        return Staff.objects.filter(feed_type=Staff.BUCKET,
                object_id=self.bucket.id,
                content_type=ContentType.objects.get_for_model(Bucket))

    def create_post(self):
        return Post(
            composition=self.composition,
            creator=self.bucket.owner,
            post_type = Post.BUCKET,
            content_object=self.bucket)

    def get_post(self):
        return Post.objects.filter(composition=self.composition,
            creator=self.bucket.owner,
            post_type=POST.BUCKET,
            object_id=self.bucket.id,
            content_type=ContentType.objects.get_for_model(BUCKET))

bind_post(BucketMembership)
bind_fresh_feed(BucketMembership)
bind_staff_feed(BucketMembership)