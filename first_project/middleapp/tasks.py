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
        saveto_cms_db = cms_application ( acknowledgementNumber = cms_data['acknowledgementNumber'] , departmentId = cms_data['departmentId'] , 
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
                msg = " Data saving failed . Api Key invalid or not matching"
                response ={"status_code":421 , "msg":msg} 
                return response
                
            else:
                
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

                    # Apply validation for all the data before saving into the database
                    # Validation for department code , department code must be 2 digits 
                    # print("the district is " ,department_Id )
                    # print("type of the district is " ,type(department_Id ))
                    if (department_Id == "" or len(department_Id) > 2 ):
                            msg = "Department  Id is Invalid"
                            response = {"status_code":429,"msg":msg}
                            
                            return response

                    check_srv_dept = service.objects.using('secondary').all().filter(departmentId = department_Id)
                    if not check_srv_dept:
                        msg = "Service Id and Department Id mismatched"
                        response = {"status_code":435,"msg":msg}
                        
                        return response

                    check_ofc_id = office_middleware.objects.using('secondary').all().filter(officeId = int(office_Id) , departmentId = department_Id)
                    if not check_ofc_id:
                        msg = "Office Id Not exists with this department id"
                        response = {"status_code":436,"msg":msg}
                        
                        return response
                                      
                    # Validation for district id , district id must be 2 digits 
                    # print("the district is " ,district_Id )
                    # print("type of the district is " ,type(district_Id ))
                    if (district_Id == "" or len(district_Id) > 2 ):
                            msg = "District Id is Invalid"
                            response = {"status_code":429,"msg":msg}
                            
                            return response

                    # Validation for blockId starts here , if block_Id is empty then 0 will sent as block_Id
                    if (block_Id == "" ):
                        block_Id = 0

                    # Validation for tahasil_Id starts here , if tahasil_Id is empty then 0 will sent as block_Id
                    if (tahasil_Id == "" ):
                        tahasil_Id = 0

                    # Validation for grampanchayat_Id starts here , if grampanchayat_Id is empty then 0 will sent as block_Id
                    if (grampanchayat_Id == "" ):
                        grampanchayat_Id = 0

                    # Validation for office_Id , office_Id must be in between 4 digits 
                    # print("the office_Id is " ,office_Id )
                    # print("type of the office_Id is " ,type(office_Id ))
                    if (office_Id == "" or len(office_Id) > 5 ):
                        msg = "Office Id is Invalid"
                        response = {"status_code":430,"msg":msg}
                        
                        return response

                    # Validation for application_Status , application_Status must be 1 digits 
                    # print("the application_Status is " ,application_Status )
                    # print("type of the application_Status is " ,type(application_Status ))
                    try:
                        if (application_Status == "" or int(application_Status) > 9 ):
                            msg = "Inavlid Application Status "
                            response = {"status_code":431,"msg":msg}             
                            return response
                    except Exception as e:
                            msg = "Invalid Application Status  "
                            response = {"status_code":438,"msg":msg}             
                            return response

                    # Validation for applicant_Name , applicant_Name mustn't be empty.
                    print("the applicant_Name is " ,applicant_Name )
                    print("type of the applicant_Name is " ,type(applicant_Name ))
                    if (applicant_Name == "" ):
                            msg = "applicant_Name is Invalid "
                            response = {"status_code":431,"msg":msg}
                            
                            return response

                    # Validation for applicant_Address starts here , if applicant_Address is empty then N/A will be sent as applicant_Address
                    if (applicant_Address == "" ):
                        applicant_Address = "N/A"
                    
                    # Validation for applicant_PhoneNo , applicant_PhoneNo mustn't be empty.
                    # print("the applicant_PhoneNo is " ,applicant_PhoneNo )
                    # print("type of the applicant_PhoneNo is " ,type(applicant_PhoneNo ))
                    # print("length of mobile number is" ,  len(applicant_PhoneNo))
                    if (applicant_PhoneNo == "" or len(applicant_PhoneNo) != 10):
                            msg = "applicant_PhoneNo is Invalid "
                            response = {"status_code":432,"msg":msg}
                            
                            return response

                    # Validation for delivery_Status , delivery_Status mustn't be empty.
                    # print("the delivery_Status is " ,delivery_Status )
                    # print("type of the delivery_Status is " ,type(delivery_Status ))
                    if (delivery_Status == ""):
                        delivery_Status = "N/A"

                    # Validation for delivery_Date , delivery_Date mustn't be empty.
                    # print("the delivery_Date is " ,delivery_Date )
                    # print("type of the delivery_Date is " ,type(delivery_Date ))
                    if (delivery_Date == ""):
                        delivery_Date = "N/A"

                    
                    # Validation for rejected_Reason , rejected_Reason mustn't be empty.
                    # print("the rejected_Reason is " ,rejected_Reason )
                    # print("type of the rejected_Reason is " ,type(rejected_Reason ))
                    if (rejected_Reason == ""):
                        rejected_Reason = "N/A"
        
                    
                    # Validation for designated_OfficerName , designated_OfficerName mustn't be empty.
                    # print("the designated_OfficerName is " ,designated_OfficerName )
                    # print("type of the designated_OfficerName is " ,type(designated_OfficerName ))
                    if (designated_OfficerName == ""):
                        msg = "designated_OfficerName is Invalid "
                        response = {"status_code":433,"msg":msg}
                        
                        return response

                    # Validation for _description , _description mustn't be empty.
                    # print("the _description is " ,_description )
                    # print("type of the _description is " ,type(_description ))
                    if (_description == ""):
                        _description = "N/A"
                        msg = "_description is Invalid "
    
                    # Acknowledgement Number Validation

                    # print("the depart code is from api number is",department_Id)
                    # print("the service code  is from api " ,_service_Id)
                    offc_id = acknowledgement_Number[2:7] # 2 3 4 5 6 
                    dep_num = acknowledgement_Number[7:9] # 7,8
                    srv_id = acknowledgement_Number[9:12] # 9,10,11
                    # print("the depart code is from acknowledgement number is",dep_num)
                    # print("the service code  is from acknowledgement number is",dep_num)

                    if (_service_Id != srv_id or department_Id != dep_num ):
                        msg = " Invalid Acknowledgement Number " 
                        response = {"status_code":433,"msg":msg} 
                        
                        return response
                    try: 
                        check_ackn_ofc_id = office_middleware.objects.using('secondary').all().filter(officeId = int(offc_id) , departmentId = int(dep_num))
                        if not (check_ackn_ofc_id):
                            msg = "Office Id mismatched in acknowledgement number "
                            response = {"status_code":438,"msg":msg}
                            return response
                    except Exception as e:
                        msg = "Office Id not exist with this department id in acknowledgement number "
                        response = {"status_code":442,"msg":msg}
                        return response
                            


                    try:
                        flt_srv = service.objects.using('secondary').all().filter(serviceId = service_Id , departmentId = int(department_Id))

                        if flt_srv:
                            print("====department have the service====")
                            
                            saveto_cms_db = cms_application (apiKey = api_Key,applicationId = application_Id, acknowledgementNumber = acknowledgement_Number , departmentId = department_Id , serviceId = _service_Id , districtId = district_Id , blockId = block_Id , tahasilId = tahasil_Id ,
                                                            grampanchayatId = grampanchayat_Id , officeId = office_Id , applicationStatus = application_Status , 
                                                            applicantName = applicant_Name , applicantAddress = applicant_Address , applicantPhoneNo = applicant_PhoneNo , 
                                                            applicationReceivedDate = applicationReceived_Date , lastDate = last_Date , deliveryStatus = delivery_Status , appealStatus = eappeal_status , revisionStatus = revision_status ,
                                                            deliveryDate = delivery_Date , rejectedReason = rejected_Reason , applyMode = apply_Mode , 
                                                            designatedOfficerName = designated_OfficerName , designatedOfficerId = designated_OfficerId , description = _description , status = status  )
                            saved = saveto_cms_db.save(using="secondary")
                            msg = "Data saved successfully"
                            response = {"status_code":200,"msg":msg}
                            
                            return response
                        else:
                            msg = "acknowledgement number is invalid . Service code and department code  not matched "
                            response = {"status_code":420,"msg":msg}                         
                            return response

                    except Exception as e:
                        msg = "Failed to save the data in the database due to the following error ".format(e)
                        response = {"status_code":413,"msg":msg}
                        return response

                except Exception as e:
                    msg = "Data received partially from application ,Field Name is invalid for {}" . format(e)
                    response = {"status_code":419,"msg":msg}                   
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