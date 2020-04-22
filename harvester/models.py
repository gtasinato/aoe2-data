from django.db import models
# Create your models here.


class Leaderboard(models.Model):
    leaderboard_id = models.IntegerField('Id type of the leaderboard')
    date = models.DateTimeField('Collection date')
    csv_table = models.FileField('CSV file storing the dataset')
    population = models.IntegerField('Total number of players')
    average_elo = models.FloatField('Average elo')
