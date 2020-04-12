from django.db import models

# TODO: When API key changes, so do the IDs because they are all encrypted with the key
# TODO: Make a test to ensure all these points are good to go https://riot-api-libraries.readthedocs.io/en/latest/ids.html

# Create your models here.
# TODO: make these fields mandatory
class Summoner(models.Model):
    region = models.CharField(max_length=4)
    accountId = models.CharField(max_length=56)
    profileIconId = models.IntegerField()
    revisionDate = models.BigIntegerField()
    name = models.CharField(max_length=16)
    summonerId = models.CharField(max_length=63)
    puuid = models.CharField(max_length=78, primary_key=True)
    summonerLevel = models.BigIntegerField()