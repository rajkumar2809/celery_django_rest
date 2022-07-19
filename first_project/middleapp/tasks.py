from urllib import response
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
from time import sleep

@shared_task
def cms_application_celery123(data):
    # print("========data received=========")
    cms_data = json.loads(data)
    # print("Data  from cms_application_celery",cms_data)
    try:
        saveto_cms_db = cms_application_2 ( acknowledgementNumber = cms_data['acknowledgementNumber'] , departmentId = cms_data['departmentId'] , 
                                        serviceId = cms_data['serviceId'] , districtId = cms_data['districtId'] , blockId = cms_data['blockId'] , tahasilId = cms_data['tahasilId'] ,
                                        grampanchayatId = cms_data['grampanchayatId'] , officeId = cms_data['officeId'] , applicationStatus = cms_data['applicationStatus'] , 
                                        applicantName = cms_data['applicantName'] , applicantAddress = cms_data['applicantAddress'] , applicantPhoneNo = cms_data['applicantPhoneNo'] , 
                                        applicationReceivedDate = cms_data['applicationReceivedDate'] , lastDate = cms_data['lastDate'] , deliveryStatus = cms_data['deliveryStatus'] ,
                                        deliveryDate = cms_data['deliveryDate'] , rejectedReason = cms_data['rejectedReason'] , applyMode = cms_data['applyMode'] , 
                                        designatedOfficerName = cms_data['designatedOfficerName'] , designatedOfficerId = cms_data['designatedOfficerId'] , description = cms_data['description']  )
        saveto_cms_db.save(using="secondary")
        return HttpResponse(status.HTTP_201_CREATED)
    except Exception as e:
        return HttpResponse(e)


@shared_task()
def send_enc_data_to_celery(token  , sid):

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
                msg = " Data saving failed . Api Key invalid or mismatched not matching"
                response ={"status_code":421 , "msg":msg} 
                return response
                
            else:
                # sleep(2)
                try:

                    api_Key = str_json['appData']['apiKey']
                    application_Id = str_json['appData']['applicationId']
                    acknowledgement_Number = str_json['appData']['acknowledgementNumber']
                    department_Id = str_json['appData']['departmentId']
                    _service_Id = str_json['appData']['serviceId']
                    district_Id = str_json['appData']['districtId']
                    block_Id = str_json['appData']['blockId']
                    tahasil_Id = str_json['appData']['tahasilId'] 
                    grampanchayat_Id = str_json['appData']['grampanchayatId']
                    office_Id = str_json['appData']['officeId'] 
                    application_Status = str_json['appData']['applicationStatus']
                    applicant_Name = str_json['appData']['applicantName']
                    applicant_Address = str_json['appData']['applicantAddress']
                    applicant_PhoneNo = str_json['appData']['applicantPhoneNo']
                    applicationReceived_Date = str_json['appData']['applicationReceivedDate'] 
                    last_Date = str_json['appData']['lastDate']
                    delivery_Status = str_json['appData']['deliveryStatus']
                    delivery_Date = str_json['appData']['deliveryDate']
                    rejected_Reason = str_json['appData']['rejectedReason'] 
                    apply_Mode = str_json['appData']['applyMode']
                    designated_OfficerName = str_json['appData']['designatedOfficerName']
                    designated_OfficerId = str_json['appData']['designatedOfficerId'] 
                    _description = str_json['appData']['description']



                    saveto_cms_db = cms_application_2 (apiKey = api_Key,applicationId = application_Id, acknowledgementNumber = acknowledgement_Number , departmentId = department_Id , serviceId = _service_Id , districtId = district_Id , blockId = block_Id , tahasilId = tahasil_Id ,
                                                    grampanchayatId = grampanchayat_Id , officeId = office_Id , applicationStatus = application_Status , 
                                                    applicantName = applicant_Name , applicantAddress = applicant_Address , applicantPhoneNo = applicant_PhoneNo , 
                                                    applicationReceivedDate = applicationReceived_Date , lastDate = last_Date , deliveryStatus = delivery_Status , appealStatus = eappeal_status , revisionStatus = revision_status ,
                                                    deliveryDate = delivery_Date , rejectedReason = rejected_Reason , applyMode = apply_Mode , 
                                                    designatedOfficerName = designated_OfficerName , designatedOfficerId = designated_OfficerId , description = _description , status = status  )
                    saved = saveto_cms_db.save(using="secondary")
                    msg = "Data saved successfully"
                    response = {"status_code":200,"msg":msg}
                    # sleep(2)
                    return response
                except Exception as e:
                    msg = "Field Name is invalid for {}" . format(e)
                    response = {"status_code":419,"msg":msg}
                    # sleep(2)
                    return response

        except json.decoder.JSONDecodeError:
                print("There was a  in input")
                msg = "Something went wrong due to data mismatched"
                response = {"status_code":413,"msg":msg}
                return response
    else:
        msg = "Api key not found"
        response = {"status_code":411,"msg":msg}
        return response