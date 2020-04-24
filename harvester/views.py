from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils.utils import harvest_leaderboard, create_plot
from .models import Leaderboard
from django.conf import settings


# Create your views here.
def index(request):

    if request.method == 'POST' and 'run_script' in request.POST:
        return redirect('harvester:loading', leaderboard_id = int(request.POST['choice']))

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
    base_url = 'https://aoe2.net/api/leaderboard?game={code}&leaderboard_id={leaderboard_id}&start={start}&count={count}'
    leaderboard = harvest_leaderboard(base_url, leaderboard_id)
    #print(reverse('harvester:result'))
#    return redirect('harvester:result', db_id = leaderboard.id)
    # print('Plotting leaderboard {n}'.format(n=db_id))
    # leaderboard = get_object_or_404(Leaderboard, pk=db_id)
    leaderboard.plot = create_plot(leaderboard)
    leaderboard.save()
    context = {
                'leaderboard' : leaderboard
                }
    print(leaderboard.plot)
    return render(request, 'harvester/result.html', context = context)

#    return redirect('harvester:result', leaderboard = leaderboard)

def archive(request):
    context = {
        
    }
    return render(request, 'harvester/archive.html', context = context)
