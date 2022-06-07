from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import json
from django.http import HttpResponse
from middleapp.models import mdl_string
from middleapp.serializers import MdlStringSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from middleapp.tasks import  send_data_through_celery

# Create your views here.

def home(request):
    ud = 10
    name = "dj"
    try:
        data = mdl_string(uid = ud , name = name)
        data.save()
        return HttpResponse("Data saved on first application successfully")
    except Exception as e:
        return HttpResponse("Data saving faailed on first application , due to {}".format(e))

@api_view(['GET'])
def get(request):
    data = mdl_string.objects.all().values()
    return Response( {"data": data})

@api_view(['post'])
def post(request):
    serializer = MdlStringSerializer(data=request.data)
    if serializer.is_valid():
        # serializer.save()
        # print("serializer is valid")
        responsess = send_data_through_celery.delay(json.dumps(request.data))
        return HttpResponse("{}".format(responsess)) # Response(request.data , status = status.HTTP_201_CREATED)  # 
    return Response(request.data , status = status.HTTP_400_BAD_REQUEST)                                