from django.db import models

# Create your models here.

class Composition(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, verbose_name = 'Title')
    description = models.CharField(max_length=1000, blank=True, default='', verbose_name = 'Description')
    artist = models.ForeignKey('auth.User', related_name='compositions')
      
    
    class Meta:
        ordering = ('created',)
        
    def save(self, *args, **kwargs):
        super(Composition, self).save(*args, **kwargs)
        
    
        