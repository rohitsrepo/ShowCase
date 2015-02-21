from django.db import models
from compositions.models import Composition
from interpretations.models import Interpretation


class EditorsListPost(models.Model):
    composition = models.ForeignKey(Composition)
    interpretation = models.ForeignKey(Interpretation)

    
class FeedPost(models.Model):
    painting_image = models.FileField()
    painting_name = models.CharField(max_length=100, blank=False, verbose_name='Painting_name')
    painter = models.CharField(max_length=100, blank=False, verbose_name='Painter')
    interpretation = models.CharField(max_length=500, verbose_name='Top Interpretation')
    interpretation_writer = models.CharField(max_length=100, blank=False, verbose_name='Interpretation Writer')
    interpretation_votes = models.PositiveIntegerField(default=0)
    
