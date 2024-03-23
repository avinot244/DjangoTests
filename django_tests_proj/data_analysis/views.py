from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import BehaviorADC
from .serializers import *

@api_view(['GET'])
def behaviorADC_list(request) :
    
    data = BehaviorADC.objects.all()
    serializer = BehaviorADCSerializer(data, context={"request": request}, many=True)

    return Response(serializer.data)


