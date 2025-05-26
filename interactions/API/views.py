from rest_framework import generics, permissions
from rest_framework import generics
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


