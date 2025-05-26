from rest_framework import serializers
from ..models import ProfileUser

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProfileUser
        fields = '__all__'  
