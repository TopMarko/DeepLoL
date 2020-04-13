from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from django.shortcuts import render

from riotwatcher import LolWatcher, ApiError

from .models import Summoner

# TODO: Make this a db thing?
VALID_REGIONS = ['NA1', 'EUW1', 'KR']

# TODO: Should this be defined in whatever function it is needed? More processing there but can it take multiple requests at a time here?
watcher = LolWatcher(settings.RG_API_KEY)

# Create your views here.

def index(request):
    return render(request, 'core/test.html', {})

# TODO: Change function name to avoid confusion with model name
def summoner(request, region, summoner_name):
    region = region.upper()
    summoner_name = summoner_name.upper()

    # TODO: Verify that summoner name could potentially exist (follows riots naming rules)
    summoner_data = None
    summoner_object = None

    # TODO: See if we have any of their match history stored
    # TODO: Send whatever user match data we have with analytics, if we dont have any, send a page without any info and have them click a button that will send a 
    #       request to the backend to get the data and do analytics and everything (a refresh button)
    match_history = None

    if region in VALID_REGIONS:
        summoner_object = Summoner.objects.all().filter(name__iexact=summoner_name, region__iexact=region)[0]
        if not summoner_object:
            summoner_data = watcher.summoner.by_name(region, summoner_name)
            summoner_object = Summoner(name=summoner_data['name'],
                                       region=region,
                                       accountId=summoner_data['accountId'],
                                       profileIconId=summoner_data['profileIconId'],
                                       revisionDate=summoner_data['revisionDate'],
                                       summonerId=summoner_data['id'],
                                       summonerLevel=summoner_data['summonerLevel'],
                                       puuid=summoner_data['puuid']
                                       )
            summoner_object.save()
        

        template = loader.get_template('core/summoner.html')
        context = {
            'summoner_info': summoner_object,
            'match_history': match_history
        }
        print(context)
        return render(request, 'core/summoner.html', context)
        
    else:
        # TODO: Have a proper page for this
        return HttpResponse(f"Invalid Region.")

