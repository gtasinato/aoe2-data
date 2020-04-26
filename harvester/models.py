from django.db import models
# Create your models here.


class Leaderboard(models.Model):
    game = models.CharField(max_length=10, help_text='AoE2:DE o AoE2:HD')
    leaderboard_id = models.IntegerField(help_text='Id type of the leaderboard')
    date = models.DateTimeField(help_text='Collection date')
    csv_table = models.FilePathField(help_text='Path to the CSV file storing the dataset')
    population = models.IntegerField(help_text='Total number of players')
    average_elo = models.FloatField(help_text='Average elo')
    plot = models.TextField(null=True, help_text='Path to the HTML plot of the dataset')
    top_player = models.CharField(null=True, help_text='Top ranking player', max_length=100)
