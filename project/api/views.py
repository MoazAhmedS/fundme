from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from project.models import Category
from project.api.serializers import *
from django.shortcuts import get_object_or_404
from project.models import Project


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
    
 

class ProjectsByCategoryView(APIView):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)

    
        projects = Project.objects.filter(categoryObject=category)

        if not projects.exists():
            return Response(
                {"projects": [], "message": "No projects found for this category."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProjectSerializer(projects, many=True)
        return Response({"projects": serializer.data}, status=status.HTTP_200_OK)
