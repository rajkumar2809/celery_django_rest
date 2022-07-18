from pydoc import classname
from statistics import mode
from django.db import models
from datetime import datetime
from datetime import date

def get_current_date():
    dt = date.today()
    return dt

def get_current_time():
    tm = datetime.now().strftime('%H:%M:%S')
    return tm


class cms_application_2(models.Model):

    apiKey = models.CharField(max_length=100)
    applicationId  = models.CharField(max_length=200)
    acknowledgementNumber = models.CharField(max_length = 300)
    departmentId = models.IntegerField()
    serviceId = models.IntegerField()
    districtId = models.IntegerField()
    blockId = models.IntegerField()
    tahasilId = models.IntegerField()
    grampanchayatId = models.IntegerField()
    officeId = models.IntegerField()
    applicationStatus = models.IntegerField()
    appealStatus = models.IntegerField()
    revisionStatus = models.IntegerField()
    applicantName = models.CharField(max_length = 200 )
    applicantAddress = models.CharField(max_length = 1000)
    applicantPhoneNo = models.CharField(max_length = 50)
    applicationReceivedDate = models.DateField()
    lastDate = models.DateField()
    deliveryStatus = models.CharField(max_length = 50)
    deliveryDate = models.DateField()
    rejectedReason = models.CharField(max_length = 500)
    applyMode = models.CharField(max_length = 20)
    designatedOfficerName = models.CharField(max_length = 50)
    designatedOfficerId = models.IntegerField()
    description = models.CharField(max_length = 1000)
    status = models.IntegerField()
    creatd_date = models.CharField(max_length=50 ,  default=get_current_date())
    created_time = models.CharField( max_length=50 , default= get_current_time())
    updated_date = models.CharField(max_length=50 , default=get_current_date())
    updated_time = models.CharField(max_length=50 , default= get_current_time())

    class Meta:
        db_table = "cms_application_2"

class service(models.Model):
    
    serviceId = models.IntegerField()
    serviceName = models.CharField(max_length= 200)
    departmentId = models.IntegerField()
    departmentName = models.CharField(max_length= 200)
    designatedOfficer = models.IntegerField()
    appellateAuthority = models.IntegerField()
    revisionalAuthority = models.IntegerField()
    timeLimit = models.CharField(max_length=100)
    apiKey = models.CharField(max_length= 30)
    url = models.CharField(max_length = 300)
    ipAddress = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    createdDate = models.CharField(max_length=50)
    createdTime = models.CharField(max_length=50)
    updatedDate = models.CharField(max_length=50)
    updatedTime = models.CharField(max_length=50)

    class Meta:
        db_table = "service"
