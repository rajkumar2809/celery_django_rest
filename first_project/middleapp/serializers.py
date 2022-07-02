from rest_framework import serializers
from .models import *

class ApplicationCmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = cms_application_2
        fields = '__all__'
