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
from interactions.models import Tag, ProjectTag


class CreateProject(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        project_data = request.data.copy()
        images = request.FILES.getlist('images')

        tag_names = request.data.getlist('tags')

        projectSerialized = ProjectSerializer(data=project_data)
        if projectSerialized.is_valid():
            project = projectSerialized.save()

            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                ProjectTag.objects.get_or_create(project_id=project, tag_id=tag)

            for image in images:
                Images.objects.create(projectObject=project, path=image)

            return Response(data=ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors': projectSerialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class ProjectDetails(APIView):
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


class CancelProjectAPIView(APIView):

    def post(self, request, project_id):
        try:
            project = Project.getProjById(project_id)
        except:
            return Response(
                {"success": False, "message": "Project not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if project.can_be_cancelled:
            project.status = False
            project.save()
            return Response(
                {"success": True, "message": "Project cancelled successfully."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"success": False, "message": "Project cannot be cancelled. Donations >= 25% of target."},
                status=status.HTTP_400_BAD_REQUEST
            )
class SimilarProjectsView(APIView):
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        tag_ids = ProjectTag.objects.filter(project_id=project).values_list('tag_id', flat=True)

        if not tag_ids:
            return Response({'similar_projects': []}, status=status.HTTP_200_OK)

        similar_project_ids = ProjectTag.objects.filter(
            tag_id__in=tag_ids
        ).exclude(
            project_id=project
        ).values_list('project_id', flat=True).distinct()

        similar_projects = Project.objects.filter(id__in=similar_project_ids)

        serialized_data = ProjectSerializer(similar_projects, many=True).data
        return Response({'similar_projects': serialized_data}, status=status.HTTP_200_OK)
    

class SearchProjectsView(APIView):
    def get(self, request):
        search_query = request.GET.get('search', '')

        if not search_query:
            return Response({"detail": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

        title_matches = Project.objects.filter(title__icontains=search_query)

        tag_matches = Project.objects.filter(
            projecttag__tag_id__name__icontains=search_query
        )

        projects = (title_matches | tag_matches).distinct()

        serialized = ProjectSerializer(projects, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
 

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
