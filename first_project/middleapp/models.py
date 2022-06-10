from django.db import models

# Create your models here.
class mdl_string(models.Model):
    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=150 )


class application_cms(models.Model):

    action = models.CharField(max_length = 50)
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

