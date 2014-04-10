from django.db import models
from django.conf import settings

class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL)
    composition = models.ForeignKey('compositions.Composition')
    edited = models.BooleanField(default=False)
 
    def __str__(self):
	if len(self.comment) > 12:
	    comment = self.comment[:12] + '...'
	else:
	    comment = self.comment

	return 'Composition : %s : Composition: %s' % (comment, self.composition)
    
    def timesince(self, now=None):
        from django.utils.timesince import timesince as _
	return _(self.created, now)


