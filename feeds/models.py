from django.db import models
from compositions.models import Composition
from interpretations.models import Interpretation


class StaffPost(models.Model):
    composition = models.ForeignKey(Composition)
    interpretation = models.ForeignKey(Interpretation) 


    def get_search_parameter(self):
        return 'feed=editors&post={0}'.format(self.id)
