from django.db import models
from django.conf import settings
from django.utils.timesince import timesince


class Message(models.Model):

    """
    A private message from user to user
    """
    sender = models.EmailField(verbose_name='sender_email', max_length=50)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='messages')
    subject = models.CharField(verbose_name='subject', max_length=100)
    body = models.TextField(verbose_name='body', max_length=500)
    read = models.BooleanField(verbose_name='read', default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def timesince(self, now=None):
        return timesince(self.created, now)
