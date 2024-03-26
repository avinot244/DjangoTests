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
    serializer = BehaviorADCSerializer(queryResult,  context={"request": request}, many=True)
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
def behaviorADC_stats_latest(request, summonnerName, limit, tournament):
    summonnerNameList : list = list()
    allObjects = BehaviorADC.objects.all()
    for res in allObjects:
        summonnerNameList.append(res.summonnerName)

    df = pd.DataFrame({"summonnerName": summonnerNameList})


    if not(summonnerName in df["summonnerName"].unique().tolist()) :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorADC.objects.filter(summonnerName__exact=summonnerName, tournament__exact=tournament).all()[:int(limit)]
    serializer = BehaviorADCSerializer(queryResult,  context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorADC_stats_patch(request, summonnerName, patch, tournament):
    #Getting all of the unique patches
    queryListPatch = BehaviorADC.objects.all()
    patchList : list = list()

    for res in queryListPatch:
        tempPatch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        patchList.append(tempPatch)
    dfPatch = pd.DataFrame({"patch": patchList})
    dfPatchUnique = dfPatch["patch"].unique()

    if not(patch in dfPatchUnique.tolist()):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorADC.objects.filter(summonnerName__exact=summonnerName, patch__contains=patch, tournament__exact=tournament)
    serializer = BehaviorADCSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)



