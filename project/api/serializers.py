from rest_framework import serializers 
from django.shortcuts import get_object_or_404
from ..models import *
from accounts.models import ProfileUser
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']

class ProjectSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source='categoryObject',
        queryset=Category.objects.all(),
    )
    user_id = serializers.PrimaryKeyRelatedField(
        source='userObject',
        queryset=ProfileUser.objects.all(),
    )
    current_donations = serializers.ReadOnlyField()
    rates = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'details', 'target', 'current_donations', 'rates',
            'start_date', 'end_date', 'status', 'featured',
            'create_date', 'category_id', 'user_id'
        ]
        read_only_fields = ['id', 'create_date', 'categoryObject', 'userObject']

    @classmethod
    def getAllProjects(cls):
        return cls(Project.objects.all(),many=True).data
    @classmethod
    def getProjectById(cls,id):
        return ProjectSerializer(Project.getProjById(id)).data

    def get_rates(self, obj):
        return obj.rates 
    
class ImageSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(
        source='projectObject',
        queryset=Project.objects.all(),
    )
    class Meta:
        model = Images
        fields = ['id','path','project_id']