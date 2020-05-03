from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

# TODO: When API key changes, so do the IDs because they are all encrypted with the key
# TODO: Make a test to ensure all these points are good to go https://riot-api-libraries.readthedocs.io/en/latest/ids.html
#                                                             https://www.riotgames.com/en/DevRel/player-universally-unique-identifiers-and-a-new-security-layer

# Create your models here.

# TODO: Set primary, foreign and unique keys on all models so relationships can be made
# TODO: Set various fields to allow/default to null values
    

# ParticipantTimelineDto  + ParticipantStatsDto  + ParticipantDto
# TODO: Give all fields null=True to avoid any unforeseen issues
class ParticipantStats(models.Model):
    # TODO: Change summonerId to a better name
    summonerId = models.ForeignKey('core.Summoner', on_delete=models.PROTECT, null=True)
    gameId = models.ForeignKey('core.MatchReference', on_delete=models.PROTECT, null=True)
    # TODO: Make teamId a choice of 100 or 200
    teamId = models.IntegerField()
    spell1Id = models.IntegerField()
    spell2Id = models.IntegerField()
    # TODO: Maybe later add highestAchievedSeasonTier to Summoner model later
    item0 = models.IntegerField()
    item1 = models.IntegerField()
    item2 = models.IntegerField()
    item3 = models.IntegerField()
    item4 = models.IntegerField()
    item5 = models.IntegerField()
    item6 = models.IntegerField()
    totalUnitsHealed = models.IntegerField()
    largestMultiKill = models.IntegerField()
    goldEarned = models.IntegerField()
    firstInhibitorKill = models.BooleanField(null=True)
    physicalDamageTaken = models.BigIntegerField()
    nodeNeutralizeAssist = models.IntegerField(null=True)
    totalPlayerScore = models.IntegerField()
    champLevel = models.IntegerField()
    damageDealtToObjectives = models.BigIntegerField()
    totalDamageTaken = models.BigIntegerField()
    neutralMinionsKilled = models.IntegerField()
    deaths = models.IntegerField()
    tripleKills = models.IntegerField()
    magicDamageDealtToChampions = models.BigIntegerField()
    wardsKilled = models.IntegerField()
    pentaKills = models.IntegerField()
    damageSelfMitigated = models.BigIntegerField()
    largestCriticalStrike = models.IntegerField()
    nodeNeutralize = models.IntegerField(null=True)
    totalTimeCrowdControlDealt = models.IntegerField()
    firstTowerKill = models.BooleanField()
    magicDamageDealt = models.BigIntegerField()
    totalScoreRank = models.IntegerField()
    nodeCapture = models.IntegerField(null=True)
    wardsPlaced = models.IntegerField()
    totalDamageDealt = models.BigIntegerField()
    timeCCingOthers = models.BigIntegerField()
    magicalDamageTaken = models.BigIntegerField()
    largestKillingSpree = models.IntegerField()
    totalDamageDealtToChampions = models.BigIntegerField()
    physicalDamageDealtToChampions = models.BigIntegerField()
    neutralMinionsKilledTeamJungle = models.IntegerField()
    totalMinionsKilled = models.IntegerField()
    firstInhibitorAssist = models.BooleanField(null=True)
    firstTowerAssist = models.BooleanField()
    visionWardsBoughtInGame = models.IntegerField()
    objectivePlayerScore = models.IntegerField()
    kills = models.IntegerField()
    combatPlayerScore = models.IntegerField()
    inhibitorKills = models.IntegerField()
    turretKills = models.IntegerField()
    participantId = models.IntegerField()
    trueDamageTaken = models.BigIntegerField()
    firstBloodAssist = models.BooleanField()
    nodeCaptureAssist = models.IntegerField(null=True)
    assists = models.IntegerField()
    teamObjective = models.IntegerField(null=True)
    altarsNeutralized = models.IntegerField(null=True)
    goldSpent = models.IntegerField()
    damageDealtToTurrets = models.BigIntegerField()
    altarsCaptured = models.IntegerField(null=True)
    # TODO: Maybe move this to the team info/stats table?
    win = models.BooleanField()
    totalHeal = models.BigIntegerField()
    unrealKills = models.IntegerField()
    visionScore = models.BigIntegerField()
    physicalDamageDealt = models.BigIntegerField()
    firstBloodKill = models.BooleanField()
    longestTimeSpentLiving = models.IntegerField()
    killingSprees = models.IntegerField()
    sightWardsBoughtInGame = models.IntegerField()
    trueDamageDealtToChampions = models.BigIntegerField()
    neutralMinionsKilledEnemyJungle = models.IntegerField()
    doubleKills = models.IntegerField()
    trueDamageDealt = models.BigIntegerField()
    quadraKills = models.IntegerField()
    playerScore0 = models.IntegerField()
    playerScore1 = models.IntegerField()
    playerScore2 = models.IntegerField()
    playerScore3 = models.IntegerField()
    playerScore4 = models.IntegerField()
    playerScore5 = models.IntegerField()
    playerScore6 = models.IntegerField()
    playerScore7 = models.IntegerField()
    playerScore8 = models.IntegerField()
    playerScore9 = models.IntegerField() 			 																			
    perk0 = models.IntegerField() #	Primary path keystone rune.
    perk0Var1 = models.IntegerField() #	Post game rune stats.
    perk0Var2 = models.IntegerField() #	Post game rune stats.
    perk0Var3 = models.IntegerField() #	Post game rune stats.
    perk1 = models.IntegerField() #	Primary path rune.
    perk1Var1 = models.IntegerField() #	Post game rune stats.
    perk1Var2 = models.IntegerField() #	Post game rune stats.
    perk1Var3 = models.IntegerField() #	Post game rune stats.
    perk2 = models.IntegerField() #	Primary path rune.
    perk2Var1 = models.IntegerField() #	Post game rune stats.
    perk2Var2 = models.IntegerField() #	Post game rune stats.
    perk2Var3 = models.IntegerField() #	Post game rune stats.
    perk3 = models.IntegerField() #	Primary path rune.
    perk3Var1 = models.IntegerField() #	Post game rune stats.
    perk3Var2 = models.IntegerField() #	Post game rune stats.
    perk3Var3 = models.IntegerField() #	Post game rune stats.
    perk4 = models.IntegerField() #	Secondary path rune.
    perk4Var1 = models.IntegerField() #	Post game rune stats.
    perk4Var2 = models.IntegerField() #	Post game rune stats.
    perk4Var3 = models.IntegerField() #	Post game rune stats.
    perk5 = models.IntegerField() #	Secondary path rune.
    perk5Var1 = models.IntegerField() #	Post game rune stats.
    perk5Var2 = models.IntegerField() #	Post game rune stats.
    perk5Var3 = models.IntegerField() #	Post game rune stats.
    perkPrimaryStyle = models.IntegerField() #	Primary rune path
    perkSubStyle = models.IntegerField() #	Secondary rune path
    # Creep score difference versus the calculated lane opponent(s) for a specified period.
    csDiffPerMin0To10 = models.FloatField(null=True)
    csDiffPerMin10To20 = models.FloatField(null=True)
    csDiffPerMin20To30 = models.FloatField(null=True)
    csDiffPerMin30ToEnd = models.FloatField(null=True)
    # Damage taken for a specified period.
    damageTakenPerMin0To10 = models.FloatField(null=True)
    damageTakenPerMin10To20 = models.FloatField(null=True)
    damageTakenPerMin20To30 = models.FloatField(null=True)
    damageTakenPerMin30ToEnd = models.FloatField(null=True)
    # Damage taken difference versus the calculated lane opponent(s) for a specified period.
    damageTakenDiffPerMin0To10 = models.FloatField(null=True)
    damageTakenDiffPerMin10To20 = models.FloatField(null=True)
    damageTakenDiffPerMin20To30 = models.FloatField(null=True)
    damageTakenDiffPerMin30ToEnd = models.FloatField(null=True)
    # Experience change for a specified period.
    xpPerMin0To10 = models.FloatField(null=True)
    xpPerMin10To20 = models.FloatField(null=True)
    xpPerMin20To30 = models.FloatField(null=True)
    xpPerMin30ToEnd = models.FloatField(null=True)
    # Experience difference versus the calculated lane opponent(s) for a specified period.
    xpDiffPerMin0To10 = models.FloatField(null=True)
    xpDiffPerMin10To20 = models.FloatField(null=True)
    xpDiffPerMin20To30 = models.FloatField(null=True)
    xpDiffPerMin30ToEnd = models.FloatField(null=True)
    # Creeps for a specified period.
    creepsPerMin0To10 = models.FloatField(null=True)
    creepsPerMin10To20 = models.FloatField(null=True)
    creepsPerMin20To30 = models.FloatField(null=True)
    creepsPerMin30ToEnd = models.FloatField(null=True)
    # Gold for a specified period. 
    goldPerMin0To10 = models.FloatField(null=True)
    goldPerMin10To20 = models.FloatField(null=True)
    goldPerMin20To30 = models.FloatField(null=True)
    goldPerMin30ToEnd = models.FloatField(null=True)

    class Meta:
        unique_together = (('summonerId', 'gameId'))
 


# TeamStatsDto + TeamBansDto
class TeamStats(models.Model):
    gameReference = models.ForeignKey('core.MatchReference', on_delete=models.PROTECT)
    region = models.CharField(max_length=4)
    towerKills = models.IntegerField() #	Number of towers the team destroyed.
    riftHeraldKills = models.IntegerField() #	Number of times the team killed Rift Herald.
    inhibitorKills = models.IntegerField() #	Number of inhibitors the team destroyed.
    dominionVictoryScore = models.IntegerField() #	For Dominion matches, specifies the points the team had at game end.
    dragonKills = models.IntegerField() #	Number of times the team killed Dragon.
    baronKills = models.IntegerField() #	Number of times the team killed Baron.
    vilemawKills = models.IntegerField() #	Number of times the team killed Vilemaw.
    teamId = models.IntegerField() #	100 for blue side. 200 for red side.
    firstBlood = models.BooleanField() #	Flag indicating whether or not the team scored the first blood.
    firstBaron = models.BooleanField() #	Flag indicating whether or not the team scored the first Baron kill.
    firstDragon = models.BooleanField() #	Flag indicating whether or not the team scored the first Dragon kill.    
    firstInhibitor = models.BooleanField() #	Flag indicating whether or not the team destroyed the first inhibitor.
    firstTower = models.BooleanField() #	Flag indicating whether or not the team destroyed the first tower.
    firstRiftHerald = models.BooleanField() #	Flag indicating whether or not the team scored the first Rift Herald kill.
    win = models.BooleanField() #	string 	String indicating whether or not the team won. There are only two values visibile in public match history. (Legal values: Fail, Win) 
    
    # TODO: Allow these to be null
    ban0Turn = models.IntegerField()
    ban0Champion = models.IntegerField()
    ban1Turn = models.IntegerField()
    ban1Champion = models.IntegerField()
    ban2Turn = models.IntegerField()
    ban2Champion = models.IntegerField()
    ban3Turn = models.IntegerField()
    ban3Champion = models.IntegerField()
    ban4Turn = models.IntegerField()
    ban4Champion = models.IntegerField()

    class Meta:
        unique_together = (('region', 'gameReference', 'teamId'))


# MatchDto 
class MatchReference(models.Model):
    gameId = models.BigIntegerField()
    queue = models.PositiveIntegerField()
    # TODO: Proper length for gameType max_length
    gameType = models.CharField(max_length=20)
    gameDuration = models.BigIntegerField()
    region = models.CharField(max_length=4)
    gameCreation = models.BigIntegerField()
    season = models.PositiveIntegerField()
    # TODO: Proper length for gameVersion max_length
    gameVersion = models.CharField(max_length=20)
    mapId = models.PositiveIntegerField()
    # TODO: Proper length for gameMode max_length
    gameMode = models.CharField(max_length=12)
    teamStats = models.ManyToManyField('core.TeamStats')
    participantStats = models.ManyToManyField('core.ParticipantStats')

    class Meta:
        unique_together = (('region', 'gameId'))


# TODO: maybe make region a choice field?
# TODO: Add a field for last time updated/refreshed
class Summoner(models.Model):
    class Tiers(models.TextChoices):
        IRON = 'IRON', _('IRON')
        BRONZE = 'BRONZE', _('BRONZE')
        GOLD = 'GOLD', _('GOLD')
        PLATINUM = 'PLATINUM', _('PLATINUM')
        DIAMOND = 'DIAMOND', _('DIAMOND')
        MASTER = 'MASTER', _('MASTER')
        GRANDMASTER = 'GRANDMASTER', _('GRANDMASTER')
        CHALLENGER = 'CHALLENGER', _('CHALLENGER')

    class Ranks(models.IntegerChoices):
        IV = 4
        III = 3
        II = 2
        I = 1

    region = models.CharField(max_length=4)
    accountId = models.CharField(max_length=56)
    profileIconId = models.IntegerField()
    revisionDate = models.BigIntegerField()
    name = models.CharField(max_length=16)
    summonerId = models.CharField(max_length=63)
    puuid = models.CharField(max_length=78, primary_key=True)
    summonerLevel = models.BigIntegerField()

    soloTier = models.CharField(
        max_length=12,
        choices=Tiers.choices,
        default=None,
        blank=True,
        null=True
    )
    soloRank = models.IntegerField(choices=Ranks.choices, default=None, blank=True, null=True)
    soloLP = models.IntegerField(default=0, blank=True, validators=[MaxValueValidator(100)])
    soloWins = models.PositiveIntegerField(default=None, blank=True, null=True)
    soloLosses = models.PositiveIntegerField(default=None, blank=True, null=True)
    soloVeteran = models.BooleanField(default=False)
    soloInactive = models.BooleanField(default=False)
    soloFreshBlood = models.BooleanField(default=False)
    soloHotStreak = models.BooleanField(default=False)
    soloLeagueId = models.CharField(max_length=255, blank=True, default='')

    soloMiniSeriesTarget = models.PositiveIntegerField(default=None, blank=True, null=True, validators=[MaxValueValidator(5)])
    soloMiniSeriesWins = models.PositiveIntegerField(default=None, blank=True, null=True, validators=[MaxValueValidator(3)])
    soloMiniSeriesLosses = models.PositiveIntegerField(default=None, blank=True, null=True, validators=[MaxValueValidator(3)])
    soloMiniSeriesProgress = models.CharField(blank=True, default='', max_length=5)


    flexTier = models.CharField(
        max_length=12,
        choices=Tiers.choices,
        default=None,
        blank=True,
        null=True
    )
    flexRank = models.IntegerField(choices=Ranks.choices, default=None, blank=True, null=True)
    flexLP = models.IntegerField(default=0, blank=True, validators=[MaxValueValidator(100)])
    flexWins = models.PositiveIntegerField(default=None, blank=True, null=True)
    flexLosses = models.PositiveIntegerField(default=None, blank=True, null=True)
    flexVeteran = models.BooleanField(default=False)
    flexInactive = models.BooleanField(default=False)
    flexFreshBlood = models.BooleanField(default=False)
    flexHotStreak = models.BooleanField(default=False)
    flexLeagueId = models.CharField(max_length=255, blank=True, default='')

    flexMiniSeriesTarget = models.PositiveIntegerField(default=None, blank=True, null=True, validators=[MaxValueValidator(5)])
    flexMiniSeriesWins = models.PositiveIntegerField(default=None, blank=True, null=True, validators=[MaxValueValidator(3)])
    flexMiniSeriesLosses = models.PositiveIntegerField(default=None, blank=True, null=True, validators=[MaxValueValidator(3)])
    flexMiniSeriesProgress = models.CharField(blank=True, default='', max_length=5)

    matches = models.ManyToManyField('core.MatchReference')
    individualPerformances = models.ManyToManyField('core.ParticipantStats')
    teamPerformances = models.ManyToManyField('core.TeamStats')

    class Meta:
        unique_together = (('region', 'summonerId'),
                           ('region', 'accountId'),
                           ('region', 'name'))


class FailedMatchGet(models.Model):
    gameId = models.BigIntegerField()
    region = models.CharField(max_length=4)

    class Meta:
        unique_together = (('gameId', 'region'))
