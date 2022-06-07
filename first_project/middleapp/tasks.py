from celery import shared_task
import json
import requests
from django.http import HttpResponse
import pymongo

@shared_task
def send_data_through_celery(data):
    data1 = json.loads(data)
    print("Data 1 from tasks",data1)
    try:
        #myclient = pymongo.MongoClient("mongodb://165.22.210.193:27017/")
        #mydb = myclient["MIDDLE_APPLICATION"]
        #mycol = mydb["middleapp_mdl_string"]

        url = 'http://165.22.210.193:8005/mdl_post_string/'
        request_type = "POST"
        data2 =  {'uid':data1['uid'] , 'name': data1['name']}
        #x = mycol.insert_one(data2)
        # x = mycol.insert_many(data2)
        _response = requests.request(request_type, url, data=data2)
        return HttpResponse("Response after saved on database {} " .format(_response))
    except Exception as e:
        return HttpResponse("Exception from tasks {} " .format(e))