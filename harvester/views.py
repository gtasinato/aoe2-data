from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils.utils import harvest_leaderboard
# Create your views here.
def index(request):
    if request.method == 'POST' and 'run_script' in request.POST:

        # impo
        # call function
        #open('touched..txt', 'a').close()
        base_url = 'https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=3&start={start}&count={count}'

        harvest_leaderboard(base_url)
        # return user to required page
        return HttpResponseRedirect(reverse('harvester:result'))

    return render(request, 'harvester/index.html')


def result(request):
    return render(request, 'harvester/result.html')
