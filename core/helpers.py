from riotwatcher import LolWatcher, ApiError
from django.conf import settings

from .models import Summoner

# TODO: Make this a db thing?
VALID_REGIONS = ['NA1', 'EUW1', 'KR']

rank_dict = {
    'IV':4,
    'III':3,
    'II':2,
    'I':1
}

def get_summoner_info(region, summoner_name):
    watcher = LolWatcher(settings.RG_API_KEY)

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

        ranked_info = watcher.league.by_summoner(region, summoner_object.summonerId)

        for info in ranked_info:
            if info['queueType'] == 'RANKED_SOLO_5x5':
                summoner_object.soloTier = info['tier']
                summoner_object.soloRank = rank_dict[info['rank']]
                summoner_object.soloLP = info['leaguePoints']
                summoner_object.soloWins = info['wins']
                summoner_object.soloLosses = info['losses']
                summoner_object.soloVeteran = info['veteran']
                summoner_object.soloInactive = info['inactive']
                summoner_object.soloFreshBlood = info['freshBlood']
                summoner_object.soloHotStreak = info['hotStreak']
                summoner_object.soloLeagueId = info['leagueId']
                # TODO: Add Miniseries stuff

            elif info['queueType'] == 'RANKED_FLEX_SR':
                summoner_object.flexTier = info['tier']
                summoner_object.flexRank = rank_dict[info['rank']]
                summoner_object.flexLP = info['leaguePoints']
                summoner_object.flexWins = info['wins']
                summoner_object.flexLosses = info['losses']
                summoner_object.flexVeteran = info['veteran']
                summoner_object.flexInactive = info['inactive']
                summoner_object.flexFreshBlood = info['freshBlood']
                summoner_object.flexHotStreak = info['hotStreak']
                summoner_object.flexLeagueId = info['leagueId']
                # TODO: Add Miniseries stuff

        summoner_object.save()
    else:
        summoner_object = summoner_object[0]

    return summoner_object