from riotwatcher import LolWatcher, ApiError
from django.conf import settings

from requests.exceptions import HTTPError

from .models import Summoner, MatchReference, TeamStats, ParticipantStats, FailedMatchGet

# TODO: Make this a db thing?
VALID_REGIONS = ['NA1', 'EUW1', 'KR']

rank_dict = {
    'IV':4,
    'III':3,
    'II':2,
    'I':1
}

def get_summoner_from_riot(region, summoner_name):
    summoner_object = None
    try:
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
        exists = True

    except HTTPError:
        exists = False
        
    return exists, summoner_object


def get_summoner_info(region, summoner_name):
    watcher = LolWatcher(settings.RG_API_KEY)

    summoner_object = None

    summoner_object = Summoner.objects.all().filter(name__iexact=summoner_name, region__iexact=region)
    if not summoner_object:
        # TODO: Deal with no summoner found response from Riot API
        exists, summoner_object = get_summoner_from_riot(region, summoner_name)
        if exists:
            summoner_object.save()
    else:
        summoner_object = summoner_object[0]
        exists = True

    return exists, summoner_object


def refresh_summoner_info(region, summoner_name):
    exists, summoner_object = get_summoner_from_riot(region, summoner_name)
    if exists:
        summoner_object.save()

    return exists, summoner_object


def get_match_history_from_riot(region, accountId):
    watcher = LolWatcher(settings.RG_API_KEY)

    match_history = watcher.match.matchlist_by_account(region, accountId)

    
    # for match in match_history['matches'][35:41]:
    #     print(match)
    #     match_response = watcher.match.by_id(region, match['gameId'])
    #     print(match_response['participants'][0]['timeline'].keys())
    #     # timeline sometimes only includes participantId, role, and lane
    #     print(match_response['participants'][0]['timeline']['goldPerMinDeltas'])


    return match_history

def store_match_reference(region, match, match_info):
    # TODO: Check if MatchReference already exists to avoid errors
    match_ref = MatchReference(
            gameId=match['gameId'],
            queue=match['queue'],
            gameType=match_info['gameType'],
            gameDuration=match_info['gameDuration'],
            region=region,
            gameCreation=match_info['gameCreation'],
            season=match['season'],
            gameVersion=match_info['gameVersion'],
            mapId=match_info['mapId'],
            gameMode=match_info['gameMode']
        )
    match_ref.save()
    return match_ref


def create_team_stats_object(region, team, match_ref):
    # TODO: Check if MatchReference already exists to avoid errors
    team_stats_object = TeamStats(
                                gameReference=match_ref,
                                region=region,
                                towerKills=team['towerKills'],
                                riftHeraldKills=team['riftHeraldKills'],
                                inhibitorKills=team['inhibitorKills'],
                                dominionVictoryScore=team['dominionVictoryScore'],
                                dragonKills=team['dragonKills'],
                                baronKills=team['baronKills'],
                                vilemawKills=team['vilemawKills'],
                                teamId=team['teamId'],
                                firstBlood=team['firstBlood'],
                                firstBaron=team['firstBaron'],
                                firstDragon=team['firstDragon'],
                                firstInhibitor=team['firstInhibitor'],
                                firstTower=team['firstTower'],
                                firstRiftHerald=team['firstRiftHerald'],
                                win=True if team['win'] != "Fail" else False,
                                # TODO: Are the banXTurns redundant?
                                ban0Turn=team['bans'][0]['pickTurn'],
                                ban0Champion=team['bans'][0]['championId'],
                                ban1Turn=team['bans'][1]['pickTurn'],
                                ban1Champion=team['bans'][1]['championId'],
                                ban2Turn=team['bans'][2]['pickTurn'],
                                ban2Champion=team['bans'][2]['championId'],
                                ban3Turn=team['bans'][3]['pickTurn'],
                                ban3Champion=team['bans'][3]['championId'],
                                ban4Turn=team['bans'][4]['pickTurn'],
                                ban4Champion=team['bans'][4]['championId'])
    team_stats_object.save()
    return team_stats_object


def create_participant_stats_object(summoner_object, match_ref, participant_data):
    participant_stats_obj = ParticipantStats(
                                            summonerId=summoner_object,
                                            gameId=match_ref,
                                            teamId=participant_data['teamId'],
                                            spell1Id=participant_data['spell1Id'],
                                            spell2Id=participant_data['spell2Id'],
                                            item0=participant_data['stats']['item0'],
                                            item1=participant_data['stats']['item1'],
                                            item2=participant_data['stats']['item2'],
                                            item3=participant_data['stats']['item3'],
                                            item4=participant_data['stats']['item4'],
                                            item5=participant_data['stats']['item5'],
                                            item6=participant_data['stats']['item6'],
                                            totalUnitsHealed=participant_data['stats']['totalUnitsHealed'],
                                            largestMultiKill=participant_data['stats']['largestMultiKill'],
                                            goldEarned=participant_data['stats']['goldEarned'],
                                        #  firstInhibitorKill=participant_data['stats']['firstInhibitorKill'],
                                            physicalDamageTaken=participant_data['stats']['physicalDamageTaken'],
                                        #  nodeNeutralizeAssist=participant_data['stats']['nodeNeutralizeAssist'],
                                            totalPlayerScore=participant_data['stats']['totalPlayerScore'],
                                            champLevel=participant_data['stats']['champLevel'],
                                            damageDealtToObjectives=participant_data['stats']['damageDealtToObjectives'],
                                            totalDamageTaken=participant_data['stats']['totalDamageTaken'],
                                            neutralMinionsKilled=participant_data['stats']['neutralMinionsKilled'],
                                            deaths=participant_data['stats']['deaths'],
                                            tripleKills=participant_data['stats']['tripleKills'],
                                            magicDamageDealtToChampions=participant_data['stats']['magicDamageDealtToChampions'],
                                            wardsKilled=participant_data['stats']['wardsKilled'],
                                            pentaKills=participant_data['stats']['pentaKills'],
                                            damageSelfMitigated=participant_data['stats']['damageSelfMitigated'],
                                            largestCriticalStrike=participant_data['stats']['largestCriticalStrike'],
                                        #  nodeNeutralize=participant_data['stats']['nodeNeutralize'],
                                            totalTimeCrowdControlDealt=participant_data['stats']['totalTimeCrowdControlDealt'],
                                            firstTowerKill=participant_data['stats']['firstTowerKill'],
                                            magicDamageDealt=participant_data['stats']['magicDamageDealt'],
                                            totalScoreRank=participant_data['stats']['totalScoreRank'],
                                        #  nodeCapture=participant_data['stats']['nodeCapture'],
                                            wardsPlaced=participant_data['stats']['wardsPlaced'],
                                            totalDamageDealt=participant_data['stats']['totalDamageDealt'],
                                            timeCCingOthers=participant_data['stats']['timeCCingOthers'],
                                            magicalDamageTaken=participant_data['stats']['magicalDamageTaken'],
                                            largestKillingSpree=participant_data['stats']['largestKillingSpree'],
                                            totalDamageDealtToChampions=participant_data['stats']['totalDamageDealtToChampions'],
                                            physicalDamageDealtToChampions=participant_data['stats']['physicalDamageDealtToChampions'],
                                            neutralMinionsKilledTeamJungle=participant_data['stats']['neutralMinionsKilledTeamJungle'],
                                            totalMinionsKilled=participant_data['stats']['totalMinionsKilled'],
                                        #  firstInhibitorAssist=participant_data['stats']['firstInhibitorAssist'],
                                            firstTowerAssist=participant_data['stats']['firstTowerAssist'],
                                            visionWardsBoughtInGame=participant_data['stats']['visionWardsBoughtInGame'],
                                            objectivePlayerScore=participant_data['stats']['objectivePlayerScore'],
                                            kills=participant_data['stats']['kills'],
                                            combatPlayerScore=participant_data['stats']['combatPlayerScore'],
                                            inhibitorKills=participant_data['stats']['inhibitorKills'],
                                            turretKills=participant_data['stats']['turretKills'],
                                            participantId=participant_data['stats']['participantId'],
                                            trueDamageTaken=participant_data['stats']['trueDamageTaken'],
                                            firstBloodAssist=participant_data['stats']['firstBloodAssist'],
                                        #  nodeCaptureAssist=participant_data['stats']['nodeCaptureAssist'],
                                            assists=participant_data['stats']['assists'],
                                        #  teamObjective=participant_data['stats']['teamObjective'],
                                        #  altarsNeutralized=participant_data['stats']['altarsNeutralized'],
                                            goldSpent=participant_data['stats']['goldSpent'],
                                            damageDealtToTurrets=participant_data['stats']['damageDealtToTurrets'],
                                        #  altarsCaptured=participant_data['stats']['altarsCaptured'],
                                            win=participant_data['stats']['win'],
                                            totalHeal=participant_data['stats']['totalHeal'],
                                            unrealKills=participant_data['stats']['unrealKills'],
                                            visionScore=participant_data['stats']['visionScore'],
                                            physicalDamageDealt=participant_data['stats']['physicalDamageDealt'],
                                            firstBloodKill=participant_data['stats']['firstBloodKill'],
                                            longestTimeSpentLiving=participant_data['stats']['longestTimeSpentLiving'],
                                            killingSprees=participant_data['stats']['killingSprees'],
                                            sightWardsBoughtInGame=participant_data['stats']['sightWardsBoughtInGame'],
                                            trueDamageDealtToChampions=participant_data['stats']['trueDamageDealtToChampions'],
                                            neutralMinionsKilledEnemyJungle=participant_data['stats']['neutralMinionsKilledEnemyJungle'],
                                            doubleKills=participant_data['stats']['doubleKills'],
                                            trueDamageDealt=participant_data['stats']['trueDamageDealt'],
                                            quadraKills=participant_data['stats']['quadraKills'],
                                            playerScore0=participant_data['stats']['playerScore0'],
                                            playerScore1=participant_data['stats']['playerScore1'],
                                            playerScore2=participant_data['stats']['playerScore2'],
                                            playerScore3=participant_data['stats']['playerScore3'],
                                            playerScore4=participant_data['stats']['playerScore4'],
                                            playerScore5=participant_data['stats']['playerScore5'],
                                            playerScore6=participant_data['stats']['playerScore6'],
                                            playerScore7=participant_data['stats']['playerScore7'],
                                            playerScore8=participant_data['stats']['playerScore8'],
                                            playerScore9=participant_data['stats']['playerScore9'],
                                            perk0=participant_data['stats']['perk0'],
                                            perk0Var1=participant_data['stats']['perk0Var1'],
                                            perk0Var2=participant_data['stats']['perk0Var2'],
                                            perk0Var3=participant_data['stats']['perk0Var3'],
                                            perk1=participant_data['stats']['perk1'],
                                            perk1Var1=participant_data['stats']['perk1Var1'],
                                            perk1Var2=participant_data['stats']['perk1Var2'],
                                            perk1Var3=participant_data['stats']['perk1Var3'],
                                            perk2=participant_data['stats']['perk2'],
                                            perk2Var1=participant_data['stats']['perk2Var1'],
                                            perk2Var2=participant_data['stats']['perk2Var2'],
                                            perk2Var3=participant_data['stats']['perk2Var3'],
                                            perk3=participant_data['stats']['perk3'],
                                            perk3Var1=participant_data['stats']['perk3Var1'],
                                            perk3Var2=participant_data['stats']['perk3Var2'],
                                            perk3Var3=participant_data['stats']['perk3Var3'],
                                            perk4=participant_data['stats']['perk4'],
                                            perk4Var1=participant_data['stats']['perk4Var1'],
                                            perk4Var2=participant_data['stats']['perk4Var2'],
                                            perk4Var3=participant_data['stats']['perk4Var3'],
                                            perk5=participant_data['stats']['perk5'],
                                            perk5Var1=participant_data['stats']['perk5Var1'],
                                            perk5Var2=participant_data['stats']['perk5Var2'],
                                            perk5Var3=participant_data['stats']['perk5Var3'],
                                            perkPrimaryStyle=participant_data['stats']['perkPrimaryStyle'],
                                            perkSubStyle=participant_data['stats']['perkSubStyle'],
                                        #  csDiffPerMin0To10=participant_data['stats']['csDiffPerMin0To10'],
                                            csDiffPerMin0To10=participant_data['timeline']['csDiffPerMinDeltas']['0-10'] if len(participant_data['timeline']['csDiffPerMinDeltas'])>0 else None,
                                            csDiffPerMin10To20=participant_data['timeline']['csDiffPerMinDeltas']['10-20'] if len(participant_data['timeline']['csDiffPerMinDeltas'])>1 else None,
                                            csDiffPerMin20To30=participant_data['timeline']['csDiffPerMinDeltas']['20-30'] if len(participant_data['timeline']['csDiffPerMinDeltas'])>2 else None,
                                            csDiffPerMin30ToEnd=participant_data['timeline']['csDiffPerMinDeltas']['30-end'] if len(participant_data['timeline']['csDiffPerMinDeltas'])>3 else None,
                                            damageTakenPerMin0To10=participant_data['timeline']['damageTakenPerMinDeltas']['0-10'] if len(participant_data['timeline']['damageTakenPerMinDeltas'])>0 else None,
                                            damageTakenPerMin10To20=participant_data['timeline']['damageTakenPerMinDeltas']['10-20'] if len(participant_data['timeline']['damageTakenPerMinDeltas'])>1 else None,
                                            damageTakenPerMin20To30=participant_data['timeline']['damageTakenPerMinDeltas']['20-30'] if len(participant_data['timeline']['damageTakenPerMinDeltas'])>2 else None,
                                            damageTakenPerMin30ToEnd=participant_data['timeline']['damageTakenPerMinDeltas']['30-end'] if len(participant_data['timeline']['damageTakenPerMinDeltas'])>3 else None,
                                            damageTakenDiffPerMin0To10=participant_data['timeline']['damageTakenDiffPerMinDeltas']['0-10'] if len(participant_data['timeline']['damageTakenDiffPerMinDeltas'])>0 else None,
                                            damageTakenDiffPerMin10To20=participant_data['timeline']['damageTakenDiffPerMinDeltas']['10-20'] if len(participant_data['timeline']['damageTakenDiffPerMinDeltas'])>1 else None,
                                            damageTakenDiffPerMin20To30=participant_data['timeline']['damageTakenDiffPerMinDeltas']['20-30'] if len(participant_data['timeline']['damageTakenDiffPerMinDeltas'])>2 else None,
                                            damageTakenDiffPerMin30ToEnd=participant_data['timeline']['damageTakenDiffPerMinDeltas']['30-end'] if len(participant_data['timeline']['damageTakenDiffPerMinDeltas'])>3 else None,
                                            xpPerMin0To10=participant_data['timeline']['xpPerMinDeltas']['0-10'] if len(participant_data['timeline']['xpPerMinDeltas'])>0 else None,
                                            xpPerMin10To20=participant_data['timeline']['xpPerMinDeltas']['10-20'] if len(participant_data['timeline']['xpPerMinDeltas'])>1 else None,
                                            xpPerMin20To30=participant_data['timeline']['xpPerMinDeltas']['20-30'] if len(participant_data['timeline']['xpPerMinDeltas'])>2 else None,
                                            xpPerMin30ToEnd=participant_data['timeline']['xpPerMinDeltas']['30-end'] if len(participant_data['timeline']['xpPerMinDeltas'])>3 else None,
                                            xpDiffPerMin0To10=participant_data['timeline']['xpDiffPerMinDeltas']['0-10'] if len(participant_data['timeline']['xpDiffPerMinDeltas'])>0 else None,
                                            xpDiffPerMin10To20=participant_data['timeline']['xpDiffPerMinDeltas']['10-20'] if len(participant_data['timeline']['xpDiffPerMinDeltas'])>1 else None,
                                            xpDiffPerMin20To30=participant_data['timeline']['xpDiffPerMinDeltas']['20-30'] if len(participant_data['timeline']['xpDiffPerMinDeltas'])>2 else None,
                                            xpDiffPerMin30ToEnd=participant_data['timeline']['xpDiffPerMinDeltas']['30-end'] if len(participant_data['timeline']['xpDiffPerMinDeltas'])>3 else None,
                                            creepsPerMin0To10=participant_data['timeline']['creepsPerMinDeltas']['0-10'] if len(participant_data['timeline']['creepsPerMinDeltas'])>0 else None,
                                            creepsPerMin10To20=participant_data['timeline']['creepsPerMinDeltas']['10-20'] if len(participant_data['timeline']['creepsPerMinDeltas'])>1 else None,
                                            creepsPerMin20To30=participant_data['timeline']['creepsPerMinDeltas']['20-30'] if len(participant_data['timeline']['creepsPerMinDeltas'])>2 else None,
                                            creepsPerMin30ToEnd=participant_data['timeline']['creepsPerMinDeltas']['30-end'] if len(participant_data['timeline']['creepsPerMinDeltas'])>3 else None,
                                            goldPerMin0To10=participant_data['timeline']['goldPerMinDeltas']['0-10'] if len(participant_data['timeline']['goldPerMinDeltas'])>0 else None,
                                            goldPerMin10To20=participant_data['timeline']['goldPerMinDeltas']['10-20'] if len(participant_data['timeline']['goldPerMinDeltas'])>1 else None,
                                            goldPerMin20To30=participant_data['timeline']['goldPerMinDeltas']['20-30'] if len(participant_data['timeline']['goldPerMinDeltas'])>2 else None,
                                            goldPerMin30ToEnd=participant_data['timeline']['goldPerMinDeltas']['30-end'] if len(participant_data['timeline']['goldPerMinDeltas'])>3 else None
                                        )
    participant_stats_obj.save()
    return participant_stats_obj

def store_failed_match(region, gameId):
    if not FailedMatchGet.objects.filter(region__iexact=region, gameId=gameId).exists():
        fmg = FailedMatchGet(region=region, gameId=gameId)
        fmg.save()


# TODO: Maybe make this a class function on the Summoner object or something?
def store_match_history(region, summoner_object, match_history):
    watcher = LolWatcher(settings.RG_API_KEY)
    match_info = None
     # TODO: Remove this logic from here
    for match in match_history['matches'][:20]:
        # TODO: Skip match if it is already in the db
        try:
            match_check = MatchReference.objects.filter(region__iexact=region, gameId=match['gameId'])
            if not match_check.exists():
                print("Match info not found in database...")
                match_info = watcher.match.by_id(region, match['gameId'])
                match_ref = store_match_reference(region, match, match_info)
            else:
                print('Match Info found in database :)')
                match_ref = match_check[0]

            team100_stats_check = TeamStats.objects.filter(region__iexact=region, gameReference=match_ref, teamId=100)
            team200_stats_check = TeamStats.objects.filter(region__iexact=region, gameReference=match_ref, teamId=200)
            
            if not team100_stats_check.exists():
                if match_info is None:
                    match_info = watcher.match.by_id(region, match['gameId'])
                    team100_stats_raw = [x for x in match_info['teams'] if x['teamId']==100][0]
                    team100_stats_obj = create_team_stats_object(region, team100_stats_raw, match_ref)
                else:
                    team100_stats_raw = [x for x in match_info['teams'] if x['teamId']==100][0]
                    team100_stats_obj = create_team_stats_object(region, team100_stats_raw, match_ref)
                    pass
            else:
                team100_stats_obj = team100_stats_check[0]

            if not team200_stats_check.exists():
                if match_info is None:
                    match_info = watcher.match.by_id(region, match['gameId'])
                    team200_stats_raw = [x for x in match_info['teams'] if x['teamId']==200][0]
                    team200_stats_obj = create_team_stats_object(region, team200_stats_raw, match_ref)
                else:
                    team200_stats_raw = [x for x in match_info['teams'] if x['teamId']==200][0]
                    team200_stats_obj = create_team_stats_object(region, team200_stats_raw, match_ref)
                    pass
            else:
                team200_stats_obj = team200_stats_check[0]
            # if not match_check.exists():

            team_stats_objs = list()

            if team100_stats_obj not in match_ref.teamStats.all():
                match_ref.teamStats.add(team100_stats_obj)
            if team200_stats_obj not in match_ref.teamStats.all():
                match_ref.teamStats.add(team200_stats_obj)
            # match_ref.save()

            # TODO: Should this be accountIds instead?
            summ_ids = list()
            # Get all the summoner id's for the participants
            if match_info == None:
                match_info = watcher.match.by_id(region, match['gameId'])
            for participant in match_info['participantIdentities']:
                summ_ids.append(participant['player']['summonerId'])

            # Determine which Summoners are already in the db
            summoners_in_game = Summoner.objects.filter(region=region, summonerId__in=summ_ids)
            summoners_found = [x.summonerId for x in summoners_in_game]        

            for participant in match_info['participantIdentities']:
                if participant['player']['summonerId'] not in summoners_found:
                    exists, summoner_object = get_summoner_from_riot(region, participant['player']['summonerName'])
                    # TODO: Should I be saving here? Do I need to?
                    summoner_object.save() # ?
                else:
                    summoner_object = summoners_in_game.filter(summonerId=participant['player']['summonerId'])[0]

                participant_stats_check = ParticipantStats.objects.filter(summonerId=summoner_object, gameId=match_ref)
                if participant_stats_check.exists():
                    participant_stats_obj = participant_stats_check[0]
                else:
                    participant_data = match_info['participants'][participant['participantId']-1]
                    participant_stats_obj = create_participant_stats_object(summoner_object, match_ref, participant_data)

                if participant_stats_obj.teamId == 100:
                    tso = team100_stats_obj
                else:
                    tso = team200_stats_obj

                if tso not in summoner_object.teamPerformances.all():
                    summoner_object.teamPerformances.add(tso)
                if match_ref not in summoner_object.matches.all():
                    summoner_object.matches.add(match_ref)
                if participant_stats_obj not in summoner_object.individualPerformances.all():
                    summoner_object.individualPerformances.add(participant_stats_obj)

        except Exception:
            store_failed_match(region, match['gameId'])
            


    return None