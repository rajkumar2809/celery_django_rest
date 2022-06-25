from celery import shared_task
import json
from django.http import HttpResponse
from middleapp.models import *
from rest_framework import status
from rest_framework.response import Response
import base64
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import pymongo

@shared_task
def send_data_through_celery(data):
    data1 = json.loads(data)
    # print("Data 1 from tasks",data1)
    try:
        saveto_db = mdl_string (uid = data1['uid'] , name = data1['name'] )
        saveto_db.save()
        return HttpResponse("status {} " .format(status.HTTP_201_CREATED))
    except Exception as e:
        return HttpResponse("Exception from tasks {} " .format(e))


@shared_task
def cms_application_celery123(data):
    # print("========data received=========")
    cms_data = json.loads(data)
    # print("Data  from cms_application_celery",cms_data)
    try:
        saveto_cms_db = application_cms (action = cms_data['action'] , acknowledgementNumber = cms_data['acknowledgementNumber'] , departmentId = cms_data['departmentId'] , 
                                        serviceId = cms_data['serviceId'] , districtId = cms_data['districtId'] , blockId = cms_data['blockId'] , tahasilId = cms_data['tahasilId'] ,
                                        grampanchayatId = cms_data['grampanchayatId'] , officeId = cms_data['officeId'] , applicationStatus = cms_data['applicationStatus'] , 
                                        applicantName = cms_data['applicantName'] , applicantAddress = cms_data['applicantAddress'] , applicantPhoneNo = cms_data['applicantPhoneNo'] , 
                                        applicationReceivedDate = cms_data['applicationReceivedDate'] , lastDate = cms_data['lastDate'] , deliveryStatus = cms_data['deliveryStatus'] ,
                                        deliveryDate = cms_data['deliveryDate'] , rejectedReason = cms_data['rejectedReason'] , applyMode = cms_data['applyMode'] , 
                                        designatedOfficerName = cms_data['designatedOfficerName'] , designatedOfficerId = cms_data['designatedOfficerId'] , description = cms_data['description']  )
        saveto_cms_db.save()
        return HttpResponse(status.HTTP_201_CREATED)
    except Exception as e:
        return HttpResponse(e)


@shared_task
def send_enc_data_to_celery(token  , sid):

    crypted_token = token
    serviceId = sid
    decryption_key = ""
    print(serviceId)
    try:    
        myclient = pymongo.MongoClient("mongodb://staging.secuodsoft.com:27666/")
        if myclient:
            print("connected succesfully")
            mydb = myclient["eappeal_bse"]
            mycol = mydb["service"] 
            eappeal_data = mycol.find() 
            # eappeal_data_count = mycol.count_documents({}) #count() 
    except Exception as e:
        print(e)

    if (eappeal_data):
        for data in eappeal_data:
            # print(data)
            if (data["serviceId"] == serviceId):
                decryption_key = data["apiKey"]
                print("data api key is {}" .format(data["apiKey"]))
    else:
        # print("======No data found==========")
        return HttpResponse("No service found in the selected database ")

    if (decryption_key != ""):
        key = bytes(decryption_key, encoding="ascii")
        try:
            # print("Inside try block and decryption key is {}".format(decryption_key))
            (ct, iv) = crypted_token.split("::", 1)
            ct = base64.b64decode(ct)
            iv = binascii.unhexlify(iv)
            cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            plain = decryptor.update(ct) + decryptor.finalize()
            decode_byte = plain.decode()
            # print("======decode_data ==========")
            print(decode_byte)

            str_json = json.loads(decode_byte)
            saveto_cms_db = application_cms (action = "post" , acknowledgementNumber = str_json['appData']['acknowledgementNumber'] , departmentId = str_json['appData']['departmentId'] , 
                                            serviceId = str_json['appData']['serviceId'] , districtId = str_json['appData']['districtId'] , blockId = str_json['appData']['blockId'] , tahasilId = str_json['appData']['tahasilId'] ,
                                            grampanchayatId = str_json['appData']['grampanchayatId'] , officeId = str_json['appData']['officeId'] , applicationStatus = str_json['appData']['applicationStatus'] , 
                                            applicantName = str_json['appData']['applicantName'] , applicantAddress = str_json['appData']['applicantAddress'] , applicantPhoneNo = str_json['appData']['applicantPhoneNo'] , 
                                            applicationReceivedDate = str_json['appData']['applicationReceivedDate'] , lastDate = str_json['appData']['lastDate'] , deliveryStatus = str_json['appData']['deliveryStatus'] ,
                                            deliveryDate = str_json['appData']['deliveryDate'] , rejectedReason = str_json['appData']['rejectedReason'] , applyMode = str_json['appData']['applyMode'] , 
                                            designatedOfficerName = str_json['appData']['designatedOfficerName'] , designatedOfficerId = str_json['appData']['designatedOfficerId'] , description = str_json['appData']['description']  )
            saved = saveto_cms_db.save()
            return Response(saved , status.HTTP_201_CREATED)


        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Key not found")