from django.contrib.postgres.fields import JSONField
from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'sources'


class Card(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)

    data = JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cards'
