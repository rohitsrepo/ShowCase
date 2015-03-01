from django.db import models

class StaffPost(models.Model):
    composition = models.ForeignKey('compositions.Composition')
    interpretation = models.ForeignKey('interpretations.Interpretation') 
    
class FreshPost(models.Model):
    composition = models.ForeignKey('compositions.Composition')
    interpretation = models.ForeignKey('interpretations.Interpretation', blank=True, null=True)
    