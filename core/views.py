from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from django.shortcuts import render

from riotwatcher import LolWatcher, ApiError

from .models import Summoner

# The API key is {settings.RG_API_KEY}
# TODO: Make this a db thing?
VALID_REGIONS = ['NA1', 'EUW1', 'KR']

# TODO: Should this be defined in whatever function it is needed? More processing there but can it take multiple requests at a time here?
watcher = LolWatcher(settings.RG_API_KEY)

# Create your views here.
# TODO: Change function name to avoid confusion with model name
def summoner(request, region, summoner_name):
    region = region.upper()
    summoner_name = summoner_name.upper()
    summoner_data = None
    summoner_object = None

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
        
        # return HttpResponse(f"Hello, world. You're at the Summoner page for {summoner_name} from {region}.<br/><br/><br/>{summoner_data}<br/><br/><br/>{test_qs}")
        template = loader.get_template('core/summoner.html')
        context = {
            'summoner_info': summoner_object
        }
        print(context)
        return render(request, 'core/summoner.html', context)

        # TODO: Send whatever user match data we have with analytics, if we dont have any, send a page without any info and have them click a button that will send a 
        #       request to the backend to get the data and do analytics and everything (a refresh button)
        
    else:
        # TODO: Have a proper page for this
        return HttpResponse(f"Invalid Region.")

