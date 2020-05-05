from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from utils.utils import harvest_leaderboard, create_plot
from .models import Leaderboard
from django.conf import settings
import datetime

# Create your views here.
def index(request):

    if request.method == 'POST' and 'run_script' in request.POST:
        req = int(request.POST['choice'])
        game = 'aoe2de'
        name = '{date}_{code}_{leaderboard_id}.txt'.format(date=datetime.datetime.now().strftime('%Y-%m-%d'),
                                        leaderboard_id=req, code=game)

        query =  Leaderboard.objects.filter(csv_table__contains=name)

        leaderboard = get_object_or_404(query).id
        return redirect('harvester:loading', leaderboard_id = leaderboard)

    else:
        print('First landing')
        return render(request, 'harvester/index.html', context={'titles': settings.TITLES})
#
# def result(request, db_id):
#     print('Plotting leaderboard {n}'.format(n=db_id))
#     leaderboard = get_object_or_404(Leaderboard, pk=db_id)
#     fig = create_plot(leaderboard)
#     context = {
#                'plot_div' : fig,
#                'leaderboard' : leaderboard
#                 }
#     return render(request, 'harvester/result.html', context = context)

def loading(request, leaderboard_id):

    leaderboard = get_object_or_404(Leaderboard, pk=leaderboard_id)

    context = {
                'leaderboard' : leaderboard,
                'title' : settings.TITLES[leaderboard.leaderboard_id]
                }
    return render(request, 'harvester/result.html', context = context)


def archive(request):
    context = {

    }
    return render(request, 'harvester/archive.html', context = context)
