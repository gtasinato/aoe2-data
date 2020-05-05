from django.core.management.base import BaseCommand
from harvester.models import Leaderboard
import utils.utils as utl
import datetime
from django.conf import settings



class Command(BaseCommand):
    help = 'Management tool to update leaderboards and plots'
    def handle(self, *args, **options):
        base_url = 'https://aoe2.net/api/leaderboard?game={code}&leaderboard_id={leaderboard_id}&start={start}&count={count}'
        self.stdout.write(f'\nScraping started at {datetime.datetime.now()}\n')
        for i in settings.TITLES.keys():
            result = utl.harvest_leaderboard(base_url, i)
            result.plot = utl.create_plot(result)
            result.save()

        self.stdout.write(f'\nScraping ended at {datetime.datetime.now()}\n')
