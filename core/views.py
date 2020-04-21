from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from django.shortcuts import render

from riotwatcher import LolWatcher, ApiError

from .models import Summoner
from .helpers import get_summoner_info

# TODO: Make this a db thing?
VALID_REGIONS = ['NA1', 'EUW1', 'KR']

# TODO: Should this be defined in whatever function it is needed? More processing there but can it take multiple requests at a time here?
watcher = LolWatcher(settings.RG_API_KEY)

# Create your views here.

def index(request):
    return render(request, 'core/test.html', {})

# TODO: Change function name to avoid confusion with model name
def summoner(request, region, summoner_name):
    match_history = None
    region = region.upper()

    if region in VALID_REGIONS:
        summoner_object = get_summoner_info(region, summoner_name)

        context = {
            'summoner_info': summoner_object,
            'match_history': match_history
        }

        return render(request, 'core/summoner.html', context)
        
    else:
        # TODO: Have a proper page for this
        return HttpResponse(f"Invalid Region.")

