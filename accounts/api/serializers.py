from rest_framework import serializers
from ..models import ProfileUser

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProfileUser
        fields = '__all__'  


class AccountRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = ProfileUser
        fields = [
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'phone',
            'image',
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return super().create(validated_data)
    

class AccountLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProfileUser
        fields = [
            'email',
            'password',
        ]