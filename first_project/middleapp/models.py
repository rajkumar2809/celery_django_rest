from django.db import models

# Create your models here.
class mdl_string(models.Model):
    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=150 )


class cms_application_2(models.Model):

    acknowledgementNumber = models.CharField(max_length = 50)
    departmentId = models.IntegerField()
    serviceId = models.IntegerField()
    districtId = models.IntegerField()
    blockId = models.IntegerField()
    tahasilId = models.IntegerField()
    grampanchayatId = models.IntegerField()
    officeId = models.IntegerField()
    applicationStatus = models.IntegerField()
    applicantName = models.CharField(max_length = 40 )
    applicantAddress = models.CharField(max_length = 100)
    applicantPhoneNo = models.BigIntegerField()
    applicationReceivedDate = models.DateField()
    lastDate = models.DateField()
    deliveryStatus = models.CharField(max_length = 10)
    deliveryDate = models.DateField()
    rejectedReason = models.CharField(max_length = 20)
    applyMode = models.CharField(max_length = 20)
    designatedOfficerName = models.CharField(max_length = 40)
    designatedOfficerId = models.IntegerField()
    description = models.CharField(max_length = 100)


class encrypted_cms(models.Model):
    enc_data = models.CharField(max_length=1000)



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
