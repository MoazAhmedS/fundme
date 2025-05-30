from rest_framework import serializers 
from django.shortcuts import get_object_or_404
from ..models import *
from accounts.models import ProfileUser
from interactions.models import Tag, ProjectTag
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']

class ImageSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(
        source='projectObject',
        queryset=Project.objects.all(),
    )
    class Meta:
        model = Images
        fields = ['id','path','project_id']

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

    images = ImageSerializer(source='images_set', many=True, read_only=True)

    tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    tag_names = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'details', 'target', 'current_donations', 'rates',
            'start_date', 'end_date', 'status', 'featured',
            'create_date', 'category_id', 'user_id','images','tags', 'tag_names'
        ]
        read_only_fields = ['id', 'create_date', 'categoryObject', 'userObject']

    @classmethod
    def getAllProjects(cls):
        return cls(Project.objects.all(),many=True).data
    @classmethod
    def getProjectById(cls,id):
        return ProjectSerializer(Project.getProjById(id)).data


    def create(self, validated_data):
        tag_names = validated_data.pop('tags', [])
        project = Project.objects.create(**validated_data)

        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            ProjectTag.objects.get_or_create(project_id=project, tag_id=tag)

        return project
    
    def get_rates(self, obj):
        return obj.rates 
    
    def get_tag_names(self, obj):
            return list(
                Tag.objects.filter(projecttag__project_id=obj.id).values_list('name', flat=True)
            )