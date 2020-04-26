from django.db import models
from picklefield.fields import PickledObjectField

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=50, help_text='Player name')
    steam_id = models.IntegerField(help_text='Steam id')
    elo = PickledObjectField(help_text='Dictionary with Elos')
    rank = PickledObjectField(help_text='Dictionary with ranking')
