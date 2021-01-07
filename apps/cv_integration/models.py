from django.contrib.auth import get_user_model
from django.db import models


class CallVisitUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=128)
