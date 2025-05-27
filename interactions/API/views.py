from rest_framework import generics, permissions
from interactions.models import *
from interactions.API.serializers import *
from rest_framework.permissions import IsAuthenticated


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]  
        return [permissions.AllowAny()] 


class ProjectTagCreateAPIView(generics.CreateAPIView):
    queryset = ProjectTag.objects.all()
    serializer_class = ProjectTagSerializer


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
