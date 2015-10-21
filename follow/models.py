from django.db import models

from allaccess.models import AccountAccess

class SocialTracker(models.Model):
	access = models.ForeignKey(AccountAccess, related_name='social_tracker')
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	remarks = models.TextField(blank=True)
	status = models.BooleanField(default=False)
