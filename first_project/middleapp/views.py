from http.client import responses
from pydoc import render_doc
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import json
from django.http import HttpResponse
from middleapp.models import *
from middleapp.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from middleapp.tasks import  *
import logging
from django.views.decorators.csrf import csrf_exempt
import pymongo
from celery.result import AsyncResult
from celery import app
# Create your views here.


class TestDat:
    def __init__(self , srvce_nme , srvce_id , departmentName , count):
        self.s_name = srvce_nme
        self.s_id = srvce_id
        self.d_name = departmentName
        self.s_count = count


def index(request):
    data = cms_application_2.objects.using('secondary').all().count()
    service_obj = service.objects.using('secondary').all()
    service_count = service.objects.using('secondary').all().count()
    no_of_application = []
    test_lst= []
    test_obj= {"srvce_nme":None}
    # print("service_count = ",service_count )
    test_lst = [] #empty array

    for i in range(1, service_count+1):
        service_ob = service.objects.using('secondary').filter(serviceId = i)
    #     # print(service_ob[0].serviceName)
        # print(i)
        srvce_nme = service_ob[0].serviceName
        srvce_id = service_ob[0].serviceId
        departmentName = service_ob[0].departmentName
        count = cms_application_2.objects.using('secondary').filter(serviceId = i).count()
        test_lst.append(TestDat(srvce_nme ,srvce_id , departmentName  ,count ))

    print(data)
    return render(request , "index.html" , {"data":data , "test_lst":test_lst}) 


@csrf_exempt
def delete_all(request):
    
    if request.method == "POST" and (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        print("Delete button clicked")
        cms_application_2.objects.using('secondary').all().delete()
        data = cms_application_2.objects.using('secondary').all().count()
    return HttpResponse(data)

@api_view(['GET'])
def cms_get(request):
    cms_data = cms_application_2.objects.using('secondary').all().values()
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

    srvc = st
    # print(service.split("=")[1])
    service_Id = int(srvc.split("=")[1])
    enc_d = request.body
    # test if service exists according to id or not
    data = service.objects.using('secondary').filter(serviceId = service_Id).exists()

    if data == False:
        print(data)
        msg = "Service Id not found"
        response = {"status_code":409 , "msg":msg}
        return HttpResponse("{}".format(response))

    else:
        try:
            decode_byte = enc_d.decode()
            responsess = send_enc_data_to_celery.delay(decode_byte , service_Id)
            msg = "Data Received"
            response = {"status_code":444 , "msg":msg}
            logger = logging.getLogger('main')
            logger.info(str(service_Id) + " " + "-" +  " " + responsess.id + " " + "-" + " " +  str(response['status_code']) + " " + "-" + " " + response['msg']) 


            result = AsyncResult(responsess.id)
            rtrn = result.get()
            print(rtrn['status_code'] , type(rtrn['status_code']))
            logger.info(responsess.id + " " + "-" +  " " + str(rtrn['status_code']) + " " + "-" +  " " + rtrn['msg'])
            return HttpResponse("{}".format(rtrn))
            
        except json.decoder.JSONDecodeError:
            msg = "Invalid request"
            response ={"status_code":434 , "msg":msg}
            logger = logging.getLogger('main')
            logger.info(str(service_Id) + " " + "-" +  " " +  " " + "-" + " " +  str(response)) 
            return HttpResponse("{}".format(response))
