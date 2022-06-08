from celery import shared_task
import json
from django.http import HttpResponse
from middleapp.models import *
from rest_framework import status

@shared_task
def send_data_through_celery(data):
    data1 = json.loads(data)
    print("Data 1 from tasks",data1)
    try:
        # url = 'http://165.22.210.193:8005/mdl_post_string/'
        # request_type = "POST"
        # data2 =  {'uid':data1['uid'] , 'name': data1['name']}
        saveto_db = mdl_string (uid = data1['uid'] , name = data1['name'] )
        saveto_db.save()
        #x = mycol.insert_one(data2)
        # x = mycol.insert_many(data2)
        # _response = requests.request(request_type, url, data=data2)
        # return Response(request.data , status = status.HTTP_201_CREATED)
        return HttpResponse("status {} " .format(status.HTTP_201_CREATED))
    except Exception as e:
        return HttpResponse("Exception from tasks {} " .format(e))