from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.conf import settings
from django.template import loader
from django.shortcuts import render
from django.core import serializers

from riotwatcher import LolWatcher, ApiError

from .models import Summoner, MatchReference
from .helpers import get_summoner_info, refresh_summoner_info, get_match_history_from_riot, store_match_history

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
        exists, summoner_object = get_summoner_info(region, summoner_name)

        if not exists:
            # TODO: Return an error page
            return HttpResponse(f"Summoner not found.")
        else:
            match_history = get_match_history_from_riot(region, summoner_object.accountId)
            store_match_history(region, summoner_object, match_history)

            # match_ref_test_var = summoner_object.matches.all()[0].gameId
            # print(match_ref_test_var)
           
            pass

        context = {
            'summoner_info': summoner_object,
            'match_history': match_history
        }

        return render(request, 'core/summoner.html', context)
        
    else:
        # TODO: Return an error page
        return HttpResponse(f"Invalid Region.")


def update_summoner(request, region, summoner_name):
    # TODO: Remove unnecessary information from being returned
    # TODO: Check when Summoner was last refreshed and only refresh it once every 3 minutes   
    summoner_object = refresh_summoner_info(region, summoner_name)
    data = serializers.serialize('json', [summoner_object,])
    
    return JsonResponse(data, safe=False)

