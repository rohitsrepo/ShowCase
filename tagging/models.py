from django.db import models

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=26, default='ART', verbose_name = 'Tag name')
    tag_def = models.CharField(max_length = 200, blank = True, verbose_name = 'Tag definition')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):   
        return self.tag_name
    
    class Meta:
        ordering = ('tag_name',)    
