from django.db import models

# Create your models here.

# Date
# Tournament
# MatchId
# SeriesId
# SummonnerName
# XPD@15
# GD@15
# CS/Min
# Kills
# Deaths
# Assists
# KP%
# Damage/Min
# JungleProximity
# botLanePresence
# riverBotPresence

class BehaviorADC(models.Model):
    date = models.CharField("Date", max_length=240)
    tournament = models.CharField("Tournament", max_length=240)
    matchId = models.CharField("MatchId", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    summonnerName = models.CharField("SummonnerName", max_length=240)
    xpd15 = models.IntegerField("XPD@15")
    gd15 = models.IntegerField("GD@15")
    csMin = models.FloatField("CS/Min")
    kills = models.IntegerField("Kills")
    deaths = models.IntegerField("Deaths")
    assists = models.IntegerField("Assists")
    kp = models.FloatField("KP%")
    dpm = models.FloatField("Damage/Min")
    jungleProximity = models.FloatField("JungleProximity")
    botLanePresence = models.FloatField("botLanePresence")
    riverBotPresence = models.FloatField("riverBotPresence")
    
    def __str__(self) -> str:
        return self.summonnerName