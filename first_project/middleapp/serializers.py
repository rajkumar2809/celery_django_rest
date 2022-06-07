from rest_framework import serializers
from .models import mdl_string

class MdlStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = mdl_string
        fields = '__all__'