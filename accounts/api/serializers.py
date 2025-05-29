from rest_framework import serializers
from ..models import ProfileUser
from django.contrib.auth import authenticate
from project.models import Project
from donation.models import Donation

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
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ProfileUser
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password.")

            if not user.email_active: 
                raise serializers.ValidationError("Account is not activated.")

            data['user'] = user
            return data

        raise serializers.ValidationError("Must include 'email' and 'password'.")


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ['email']

    def validate_email(self, value):
        if not ProfileUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = ProfileUser
        fields = ['password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def update(self, instance, validated_data):
        validated_data.pop('confirm_password')
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'image', 'birth_date', 'facebook', 'country', 'email_active', 'create_date']

class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'details', 'target', 'current_donations', 'start_date', 'end_date', 'create_date', 'status', 'featured', 'categoryObject']

class UserDonationSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project_id.title', read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'amount', 'donation_date', 'project_id', 'project_title']