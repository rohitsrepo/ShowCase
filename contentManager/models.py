from django.db import models
from compositions.models import Composition
from django.conf import settings

class ReportAbuse(models.Model):
    composition = models.ForeignKey(Composition)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL)