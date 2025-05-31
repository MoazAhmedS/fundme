from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from interactions.models import Rate
from .serializers import *

class RateListAPIView(APIView):
    def get(self, request, project_id):
        queryset = Rate.objects.filter(project_id=project_id)
        serializer = RateSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RateCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        data = request.data.copy()
        data['project'] = project_id 
        serializer = RateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateTagView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = serializer.validated_data['name'].strip()

        if not name:
            return Response({"name": "Tag name cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        tag, created = Tag.objects.get_or_create(name=name)
        output = TagSerializer(tag).data
        return Response(output | {"created": created}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)