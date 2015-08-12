from django.db import models
from compositions.models import Composition
from accounts.models import User

class Bucket(models.Model):
    name = models.CharField(max_length=25, blank=False)
    compositions = models.ManyToManyField(Composition, related_name='holders', through='BucketMembership')
    owner = models.ForeignKey(User, related_name='buckets')
    created = models.DateTimeField(auto_now_add=True)

    @property
    def compositions_count(self):
        return self.compositions.all().count()

    @property
    def picture(self):
        try:
            composition = self.compositions.order_by('bucketmembership__added').last()
            return composition.get_350_url()
        except:
            return ''


class BucketMembership(models.Model):
    bucket = models.ForeignKey(Bucket, related_name='membership')
    composition = models.ForeignKey(Composition)
    added = models.DateTimeField(auto_now_add=True)