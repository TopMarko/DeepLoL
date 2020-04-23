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

def get_summoner_from_riot(region, summoner_name):
    watcher = LolWatcher(settings.RG_API_KEY)
    # TODO: Verify that summoner name could potentially exist (follows riots naming rules)

    summoner_object = Summoner.objects.all().filter(name__iexact=summoner_name, region__iexact=region)
    if not summoner_object:
        summoner_object = Summoner()
    else:
        summoner_object = summoner_object[0]

    summoner_data = watcher.summoner.by_name(region, summoner_name)
    summoner_object = Summoner(name=summoner_data['name'],
                                region=region.upper(),
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
            try:
                summoner_object.soloMiniSeriesTarget = info['miniSeries']['target']
                summoner_object.soloMiniSeriesWins = info['miniSeries']['wins']
                summoner_object.soloMiniSeriesLosses = info['miniSeries']['losses']
                summoner_object.soloMiniSeriesProgress = info['miniSeries']['progress']
            except Exception:
                summoner_object.soloMiniSeriesTarget = None
                summoner_object.soloMiniSeriesWins = None
                summoner_object.soloMiniSeriesLosses = None
                summoner_object.soloMiniSeriesProgress = ""


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
            try:
                summoner_object.flexMiniSeriesTarget = info['miniSeries']['target']
                summoner_object.flexMiniSeriesWins = info['miniSeries']['wins']
                summoner_object.flexMiniSeriesLosses = info['miniSeries']['losses']
                summoner_object.flexMiniSeriesProgress = info['miniSeries']['progress']
            except Exception:
                summoner_object.flexMiniSeriesTarget = None
                summoner_object.flexMiniSeriesWins = None
                summoner_object.flexMiniSeriesLosses = None
                summoner_object.flexMiniSeriesProgress = ""
        
    return summoner_object


def get_summoner_info(region, summoner_name):
    watcher = LolWatcher(settings.RG_API_KEY)

    summoner_object = None

    summoner_object = Summoner.objects.all().filter(name__iexact=summoner_name, region__iexact=region)
    if not summoner_object:
        # TODO: Deal with no summoner found
        get_summoner_from_riot(region, summoner_name)
        summoner_object.save()
    else:
        summoner_object = summoner_object[0]

    return summoner_object


def refresh_summoner_info(region, summoner_name):
    summoner_object = get_summoner_from_riot(region, summoner_name)
    summoner_object.save()

    return summoner_object