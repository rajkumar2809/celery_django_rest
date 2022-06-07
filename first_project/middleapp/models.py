from django.db import models

# Create your models here.
class mdl_string(models.Model):
    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=150 )