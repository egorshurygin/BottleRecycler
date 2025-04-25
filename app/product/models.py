from django.db import models
from pytz import unicode


class DisplayCode(models.Model):
    code = models.CharField(max_length=2000)

    def __str__(self):
        return unicode(self.code)


class CardBalance(models.Model):
    code = models.CharField(max_length=2000)

    def __str__(self):
        return unicode(self.code)

