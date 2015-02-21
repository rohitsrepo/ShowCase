from django.db import models
from compositions.models import Composition
from interpretations.models import Interpretation


class StaffPost(models.Model):
    composition = models.ForeignKey(Composition)
    interpretation = models.ForeignKey(Interpretation) 
