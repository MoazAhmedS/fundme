from rest_framework import serializers 

from ..models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id','create_date', 'current_donations']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'
        read_only_fields = ['id']