from riotwatcher import LolWatcher, ApiError
from django.conf import settings

from .models import Summoner

# TODO: Make this a db thing?
VALID_REGIONS = ['NA1', 'EUW1', 'KR']

def get_summoner_info(region, summoner_name):
    watcher = LolWatcher(settings.RG_API_KEY)
    # region = region.upper() # Redundant
    summoner_name = summoner_name.upper()

    # TODO: Verify that summoner name could potentially exist (follows riots naming rules)
    summoner_data = None
    summoner_object = None

    # TODO: See if we have any of their match history stored
    # TODO: Send whatever user match data we have with analytics, if we dont have any, send a page without any info and have them click a button that will send a 
    #       request to the backend to get the data and do analytics and everything (a refresh button)
    match_history = None

    summoner_object = Summoner.objects.all().filter(name__iexact=summoner_name, region__iexact=region)
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
    else:
        summoner_object = summoner_object[0]

    ranked_info = watcher.league.by_summoner(region, summoner_object.summonerId)

    # print(ranked_info)

    return summoner_object