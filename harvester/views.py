from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils.utils import harvest_leaderboard, create_plot
from .models import Leaderboard

# Create your views here.
def index(request):
    if request.method == 'POST' and 'run_script' in request.POST:
        base_url = 'https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id={leaderboard_id}&start={start}&count={count}'
        # path = harvest_leaderboard(base_url, request.POST['leaderboard_id'])
        # return user to required page
        print(request.POST)
        return HttpResponseRedirect(reverse('harvester:result'))


    elif request.method == 'POST':
        print(request)
        # return HttpResponseRedirect(reverse('harvester:result'))
        return render(request, 'harvester/error.html')
    else:
        return render(request, 'harvester/index.html')


def result(request):
    print(request.GET)
    # path = 'not_versioned/data/{name}_{id}.txt'.format(id=request.POST['leaderboard_id'], name=datetime.now().strftime('%Y-%m-%d'))
    # if os.path.isfile(path):
    #     create_plot(path, request.POST['leaderboard_id'])
    #     return render(request, 'harvester/result.html', context = {'plot_div': fig})
    # else:
    #     return render(request, 'harvester/error.html')
    return render(request, 'harvester/result.html')
