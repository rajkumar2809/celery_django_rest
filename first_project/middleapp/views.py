from pydoc import render_doc
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import json
from django.http import HttpResponse
from middleapp.models import mdl_string
from middleapp.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from middleapp.tasks import  send_data_through_celery , cms_application_celery123 , send_enc_data_to_celery
import logging
from django.views.decorators.csrf import csrf_exempt
import pymongo

# Create your views here.



def index(request):
    data = cms_application_2.objects.all().count()
    print(data)
    return render(request , "index.html" , {"data":data})

@csrf_exempt
def delete_all(request):
    
    if request.method == "POST" and (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        print("Delete button clicked")
        cms_application_2.objects.all().delete()
        data = cms_application_2.objects.all().count()
    return HttpResponse(data)
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
        return HttpResponse("{}".format(responsess)) 
        # return Response(request.data , status = status.HTTP_201_CREATED)

    return Response(request.data , status = status.HTTP_400_BAD_REQUEST)

# APi for CMS Application or for cms_application_2 modal

@api_view(['GET'])
def cms_get(request):
    cms_data = cms_application_2.objects.all().values()
    return Response( {"data": cms_data})


@api_view(['post'])
def cms_post(request):
    serializer = ApplicationCmsSerializer(data=request.data)
    csm_data = json.dumps(request.data)
    rqst_data = json.loads(csm_data)
    logger = logging.getLogger('main')
    ac_nm = rqst_data['acknowledgementNumber']
    print("Acnmber is ", ac_nm)
    srvc_id = rqst_data['serviceId']
    logger.info(str(ac_nm) + " " + "-" +  " " + str(srvc_id) + " " )
    # logger.info(_Service)
    if serializer.is_valid():
        # print("serializer is valid")
        responsess = cms_application_celery123.delay(json.dumps(request.data))
        return HttpResponse("{}".format(responsess))
    print(serializer.errors) 
    return Response(request.data , status = status.HTTP_400_BAD_REQUEST)

@api_view(['post'])
def enc_post(request , st):
    # print(st)

    service = st
    # print(service.split("=")[1])
    serviceId = int(service.split("=")[1])
    print(serviceId)
    # print(type(serviceId))
    # serviceId = id
    enc_d = request.body

    try:
        decode_byte = enc_d.decode()
        responsess = send_enc_data_to_celery.delay(decode_byte , serviceId)
        return HttpResponse("{}".format(responsess))
    except Exception as e:
        return HttpResponse(e)
