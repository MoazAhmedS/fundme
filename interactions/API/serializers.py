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
        fields = ['id', 'user_id', 'project_id', 'rate_value', 'note']
        read_only_fields = ['id', 'user_id']

    def validate_rate_value(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rate must be between 1 and 5.")
        return value
    
class RateCreateAPIView(generics.CreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.profileuser)

class RateListAPIView(generics.ListAPIView):
    serializer_class = RateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Rate.objects.all()
        project_id = self.request.query_params.get('project_id')
        user_id = self.request.query_params.get('user_id')
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
