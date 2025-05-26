from rest_framework import generics, permissions
from interactions.models import Tag
from interactions.serializers import TagSerializer

class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]  # الادمن بس اللي يضيف التاجات 
        return [permissions.AllowAny()]  # الكل يقدر يشوف التاجات
