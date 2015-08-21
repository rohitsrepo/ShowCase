from django.db import models

from compositions.models import Composition
from posts.models import Post, bind_post
from accounts.models import User

def get_upload_file_name_background(instance, filename):
    return '%s/buckets/%s' % (instance.owner.id, filename.split('/')[-1] + '.jpg')

class Bucket(models.Model):
    name = models.CharField(max_length=25, blank=False)
    background = models.ImageField(upload_to=get_upload_file_name_background, blank=True, null=True)
    compositions = models.ManyToManyField(Composition, related_name='holders', through='BucketMembership')
    owner = models.ForeignKey(User, related_name='buckets')
    created = models.DateTimeField(auto_now_add=True)

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
            composition = self.compositions.order_by('bucketmembership__added').last()
            return composition.get_350_url()
        except:
            try:
                return self.background_url
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
