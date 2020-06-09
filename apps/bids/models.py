from django.db import models


class Bid(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    offer = models.OneToOneField('calculator.Offer', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
