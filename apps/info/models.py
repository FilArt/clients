from django.contrib.auth import get_user_model
from django.db import models


class Info(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    users = models.ManyToManyField(to=get_user_model())
