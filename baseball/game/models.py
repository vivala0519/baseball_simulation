
from django.db import models


class Batter(models.Model):
    # id = models.IntegerField(primary_key=True, null=False)
    player = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    team = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    hit = models.IntegerField(blank=True, null=True)
    secbase = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    thrbase = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    homerun = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    fourballs = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    onbase = models.FloatField(blank=True, null=True)  # Field name made lowercase.


class Pitcher(models.Model):
    player = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    team = models.TextField(blank=True, null=True)
    inning = models.FloatField(blank=True, null=True)
    strikeout = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    onbase = models.FloatField(blank=True, null=True)  # Field name made lowercase.