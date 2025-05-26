from rest_framework import serializers
from ..models import ProfileUser

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProfileUser
        fields = '__all__'  
        
class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProfileUser
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
            'image',
        ]  

class AccountLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProfileUser
        fields = [
            'email',
            'password',
        ]