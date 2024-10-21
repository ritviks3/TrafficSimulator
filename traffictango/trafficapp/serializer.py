from rest_framework import serializers
from .models import *

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['x','y','speed','acceleration','id','lane']