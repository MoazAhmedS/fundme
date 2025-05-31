from rest_framework import serializers
from interactions.models import Tag, ProjectTag, Rate



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProjectTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTag
        fields = ['id', 'project_id', 'tag_id']
        read_only_fields = ['id']


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'user', 'project', 'rate_value', 'note']
        read_only_fields = ['id', 'user']

    def validate_rate_value(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rate must be between 1 and 5.")
        return value


