from django.db import models
from compositions.models import Composition
from accounts.models import User

class Bucket(models.Model):
    name = models.CharField(max_length=25, blank=False)
    compositions = models.ManyToManyField(Composition, related_name='holders')
    owner = models.ForeignKey(User, related_name='buckets')
    created = models.DateTimeField(auto_now_add=True)

    @property
    def compositions_count(self):
        return self.compositios.all().count()

    @property
    def picture(self):
        try:
            composition = self.compositions.all()[0]
            return composition.get_350_url()
        except:
            return ''