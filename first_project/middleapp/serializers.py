from rest_framework import serializers
from .models import *

class MdlStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = mdl_string
        fields = '__all__'

class ApplicationCmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = application_cms
        fields = '__all__'

class EncyptedCmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = encrypted_cms
        fields = '__all__'