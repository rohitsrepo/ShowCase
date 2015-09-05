from django.db import models

from ShowCase.slugger import unique_slugify

from compositions.models import Composition
from compositions.imageTools import compress
from posts.models import Post, bind_post
from accounts.models import User


def get_upload_file_name_background(instance, filename):
    return '%s/buckets/%s' % (instance.owner.id, filename.split('/')[-1] + '.jpg')

class Bucket(models.Model):
    name = models.CharField(max_length=25, blank=False)
    description = models.CharField(max_length=111, blank=True)
    background = models.ImageField(upload_to=get_upload_file_name_background, blank=True, null=True)
    compositions = models.ManyToManyField(Composition, related_name='holders', through='BucketMembership')
    slug = models.SlugField(max_length=100, unique=True)

    owner = models.ForeignKey(User, related_name='buckets')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Bucket, self).save(*args, **kwargs)

        if self.background:
            compress(self.background.path)

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



class BucketMembership(models.Model):
    bucket = models.ForeignKey(Bucket, related_name='membership')
    composition = models.ForeignKey(Composition)
    added = models.DateTimeField(auto_now_add=True)

    def create_post(self):
        return Post(
            composition=self.composition,
            creator=self.bucket.owner,
            post_type = Post.BUCKET,
            content_object=self.bucket)

bind_post(BucketMembership)
