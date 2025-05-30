from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.pagination import  PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from ..models import *
from comments.models import Comment
from comments.API.serializers import CommentSerializer

class CreateProject(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        project_data = request.data.copy()
        images = request.FILES.getlist('images') 

        projectSerialized = ProjectSerializer(data=project_data)
        if projectSerialized.is_valid():
            project = projectSerialized.save()
            for image in images:
                Images.objects.create(projectObject=project, path=image)

            return Response(data=ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors': projectSerialized.errors}, status=status.HTTP_400_BAD_REQUEST)

class ReadUpdateDeleteProjectByID(APIView):
    def get(self,request,id):
        return Response(
            data=ProjectSerializer.getProjectById(id),
            status=status.HTTP_200_OK
        )

class ProjectCommentsView(APIView):
    def get(self, request, project_id):
        comments = Comment.objects.filter(project_id=project_id, parent_id=None).order_by('-created_date')
        serialized = CommentSerializer(comments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can create categories.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response({
                'message': 'Category created successfully.',
                'category': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
