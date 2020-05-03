from django.contrib import admin

from .models import Summoner, MatchReference, TeamStats, ParticipantStats, FailedMatchGet

# Register your models here.
admin.site.register(Summoner)
admin.site.register(MatchReference)
admin.site.register(TeamStats)
admin.site.register(ParticipantStats)
admin.site.register(FailedMatchGet)
