from django.db import models
from compositions.models import Composition
from interpretations.models import Interpretation


def get_upload_file_name_composition(instance, filename):
    return 'Users/%s/Compositions/%s/%s' % (instance.artist.id, instance.created, filename)


class EditorsListPost(models.Model):
    composition = models.ForeignKey(Composition)
    interpretation = models.ForeignKey(Interpretation)

    
class TempFeedPosts(models.Model):
    painting_image = models.FileField(upload_to=get_upload_file_name_composition)
    painting_name = models.CharField(max_length=100, blank=False, verbose_name='Painting_name')
    painter = models.CharField(max_length=100, blank=False, verbose_name='Painter')
    interpretation = models.CharField(max_length=500, verbose_name='Top Interpretation')
    interpretation_writer = models.CharField(max_length=100, blank=False, verbose_name='Interpretation Writer')
    interpretation_votes = models.PositiveIntegerField(default=0)
    
