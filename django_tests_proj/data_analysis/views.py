from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import BehaviorADC
from .serializers import *
from .globals import BEHAVIOR_ADC_HEADER

import os
import pandas as pd

@api_view(['GET'])
def behaviorADC_list(request, limit: int) :
    data = BehaviorADC.objects.all()[:int(limit)]
    serializer = BehaviorADCSerializer(data, context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorADC_patch(request, patch1, patch2):
    
    # use Entry.objects.get(patch__contains=patch1 + "." + patch2)
    queryResult = BehaviorADC.objects.filter(patch__contains=patch1 + "." + patch2)
    queryResult.order_by("-seriesId")
    print(queryResult)

    serializer = BehaviorADCSerializer(queryResult, context={"request": request}, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_listPatch(request):
    queryResult = BehaviorADC.objects.all()
    patchList : list = list()

    for res in queryResult:
        patch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        patchList.append(patch)
    df = pd.DataFrame({"patch": patchList})

    return Response(df["patch"].unique())

@api_view(['GET'])
def behaviorADC_latest(request, limit : str):
    data = BehaviorADC.objects.order_by("-seriesId")[:int(limit)]
        
    
    serializer = BehaviorADCSerializer(data, context={"request": request}, many=True)

    return Response(serializer.data)


@api_view(['PATCH'])
def behaviorADC_updatePatch(request):
    csv_file_path = "./data_analysis/data/behavior_ADC.csv"
    df = pd.read_csv(csv_file_path, sep=";")

    for _, row in df.iterrows():
        queryResult = BehaviorADC.objects.filter(seriesId__exact=row["SeriesId"], summonnerName__exact=row["SummonnerName"], matchId__exact=row["MatchId"])
        print(queryResult)

        data = BehaviorADC.objects.get(seriesId=row["SeriesId"], summonnerName=row["SummonnerName"], matchId=row["MatchId"])
        data.delete()
        data.patch = row["Patch"]
        data.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def behaviorADC_stats(request, summonnerName):
    print(summonnerName)

    summonnerNameList : list = list()
    allObjects = BehaviorADC.objects.all()
    for res in allObjects:
        summonnerNameList.append(res.summonnerName)

    df = pd.DataFrame({"summonnerName": summonnerNameList})


    if not(summonnerName in df["summonnerName"].unique().tolist()) :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorADC.objects.filter(summonnerName__exact=summonnerName)
    
    data : list = list()
    for res in queryResult:
        data.append([res.date, res.tournament, res.matchId, res.seriesId, res.patch, res.summonnerName, res.xpd15, res.gd15, res.csMin, res.kills, res.deaths, res.assists, res.kp, res.dpm, res.jungleProximity, res.botLanePresence, res.riverBotPresence])

    df = pd.DataFrame(data=data, columns=BEHAVIOR_ADC_HEADER)
    print(df)

    return Response(df)