from rest_framework import serializers 

from ..models import *
from ...accounts.models import ProfileUser

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
        source = 'userObject',
        queryset = ProfileUser.objects.all(),
    )

    class Meta:
        model = Project
        fields = ['id','title','details','target','current_donations','start_date',
                  'end_date','status','featured','create_date','category_id','user_id']
        read_only_fields = ['id','create_date', 'current_donations','categoryObject','userObject']

class ImageSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(
        source='projectObject',
        queryset=Project.objects.all(),
    )
    class Meta:
        model = Images
        fields = ['id','path','project_id']
        read_only_fields = ['id','projectObject']