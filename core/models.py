from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

# TODO: When API key changes, so do the IDs because they are all encrypted with the key
# TODO: Make a test to ensure all these points are good to go https://riot-api-libraries.readthedocs.io/en/latest/ids.html
#                                                             https://www.riotgames.com/en/DevRel/player-universally-unique-identifiers-and-a-new-security-layer

# Create your models here.
# TODO: maybe make region a choice field?
# TODO: Add a field for last time updated/refreshed
class Summoner(models.Model):
    class Tiers(models.TextChoices):
        IRON = 'IN', _('Iron')
        BRONZE = 'BE', _('Bronze')
        GOLD = 'GD', _('Gold')
        PLATINUM = 'PN', _('Platinum')
        DIAMOND = 'DD', _('Diamond')
        MASTER = 'MR', _('Master')
        GRANDMASTER = 'GR', _('Grandmaster')
        CHALLENGER = 'CR', _('Challenger')

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

    class Meta:
        unique_together = (('region', 'summonerId'),
                           ('region', 'accountId'),
                           ('region', 'name'))