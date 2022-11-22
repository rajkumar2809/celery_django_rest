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
    data = cms_application.objects.using('secondary').all().count()
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
        count = cms_application.objects.using('secondary').filter(serviceId = i).count()
        test_lst.append(TestDat(srvce_nme ,srvce_id , departmentName  ,count ))

    print(data)
    return render(request , "index.html" , {"data":data , "test_lst":test_lst}) 


@csrf_exempt
def delete_all(request):
    
    if request.method == "POST" and (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        print("Delete button clicked")
        cms_application.objects.using('secondary').all().delete()
        data = cms_application.objects.using('secondary').all().count()
    return HttpResponse(data)

@api_view(['GET'])
def cms_get(request):
    cms_data = cms_application.objects.using('secondary').all().values()
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
            print(rtrn)
            # print(rtrn['status_code'] , type(rtrn['status_code']))
            # logger.info(responsess.id + " " + "-" +  " " + str(rtrn['status_code']) + " " + "-" +  " " + rtrn['msg'])
            return HttpResponse("{}".format(rtrn))
            
        except json.decoder.JSONDecodeError:
            msg = "Invalid request"
            response ={"status_code":434 , "msg":msg}
            logger = logging.getLogger('main')
            logger.info(str(service_Id) + " " + "-" +  " " +  " " + "-" + " " +  str(response)) 
            return HttpResponse("{}".format(response))


@api_view(['post'])
def enc_update(request , st):
    # print(st)
    srvc = st
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
            responses = update_application(decode_byte , service_Id)
            print(responses)
            return HttpResponse(responses)
            
        except json.decoder.JSONDecodeError:
            msg = "Invalid request"
            response ={"status_code":434 , "msg":msg}
            return HttpResponse("{}".format(response))


def update_application(token , sid):
    print("========update application called==========")
    crypted_token = token
    service_Id = sid
    decryption_key = ""
    print(service_Id)
    data = service.objects.using('secondary').all().filter(serviceId = service_Id)
    print(data[0].apiKey)
    decryption_key = data[0].apiKey
    

    if (decryption_key != ""):
        key = bytes(decryption_key, encoding="ascii")
        print("The key is ", key)
        try:
            # print("Inside try block and decryption key is {}".format(decryption_key))
            (ct, iv) = crypted_token.split("::", 1)
            # print("===========ct is=============",ct)
            # print("===========iv is=============",iv)
            ct = base64.b64decode(ct)
            iv = binascii.unhexlify(iv)
            cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            plain = decryptor.update(ct) + decryptor.finalize()
            print("===plain is =====")
            print(plain)
            # decode_byte = plain.decode()
            decode_byte = plain.decode('utf-8', 'ignore')
            print("======decode_data ==========")
            print(decode_byte)

            str_json = json.loads(decode_byte)
            print(str_json['appData']['apiKey'])
            status = 1
            eappeal_status = 0
            revision_status = 0
            if (decryption_key != str_json['appData']['apiKey'] ):
                # print("Api Key invalid or mismatched not matching")
                msg = " Data saving failed . Api Key invalid or not matching"
                response ={"status_code":421 , "msg":msg} 
                return HttpResponse("{}".format(response))
                
            else:
                
                try:
                    api_Key = str_json['appData']['apiKey']
                    application_Id = str_json['appData']['applicationId']
                    acknowledgement_Number = str_json['appData']['acknowledgementNumber']
                    department_Id = str_json['appData']['departmentId']
                    _service_Id = str_json['appData']['serviceId']
                    district_Id = str_json['appData']['districtId']
                    application_Status = str_json['appData']['applicationStatus']
                    delivery_Status = str_json['appData']['deliveryStatus']
                    delivery_Date = str_json['appData']['deliveryDate']
                    rejected_Reason = str_json['appData']['rejectedReason'] 

                    # Validation for application_Status , application_Status must be 1 digits 
                    # print("the application_Status is " ,application_Status )
                    # print("type of the application_Status is " ,type(application_Status ))
                    try:
                        if (application_Status == "" or int(application_Status) > 9 ):
                            msg = "Inavlid Application Status "
                            response = {"status_code":431,"msg":msg}             
                            return HttpResponse("{}".format(response))
                    except Exception as e:
                            msg = "Invalid Application Status  "
                            response = {"status_code":438,"msg":msg}             
                            return HttpResponse("{}".format(response))

                    try:
                        app_exist = cms_application.objects.using('secondary').all().filter( applicationId = application_Id , serviceId = service_Id , departmentId = int(department_Id) , 
                        acknowledgementNumber = acknowledgement_Number , apiKey = api_Key , districtId = district_Id  )
                        if app_exist:
                            print(app_exist)
                            upd = app_exist.update(applicationStatus = application_Status ,deliveryStatus = delivery_Status , deliveryDate = delivery_Date , rejectedReason = rejected_Reason )
                            print("Updated" , upd)
                            return HttpResponse("updated successfully")

                        else:
                            return HttpResponse("Data not Exists ")

                    except Exception as e:
                        print(e)
                        return HttpResponse("{}".format(e))

                except Exception as e:
                    msg = "Data received partially for Updation {}" . format(e)
                    response = {"status_code":447,"msg":msg}                   
                    return HttpResponse("{}".format(response))

        except json.decoder.JSONDecodeError:
                msg = "Something went wrong due to data mismatched "
                response = {"status_code":440,"msg":msg}
                return HttpResponse("{}".format(response))
                # return response
    else:
        msg = "Api key not found"
        response = {"status_code":411,"msg":msg}
        return HttpResponse("{}".format(response))
