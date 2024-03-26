from rest_framework import serializers
from .models import BehaviorADC

class BehaviorADCSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BehaviorADC
        fields = ("pk", "date", "tournament", "matchId", "seriesId", "patch", "summonnerName", "xpd15", "gd15", "csMin", "kills", "deaths", "assists", "kp", "dpm", "jungleProximity", "botLanePresence", "riverBotPresence")