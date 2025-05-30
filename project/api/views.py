from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
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
    
class LastFiveFeaturedProjects(APIView):
    def get(self, request):
        projects = Project.objects.filter(featured=True).order_by('-create_date')[:5]
        serialized_projects = ProjectSerializer(projects, many=True)
        return Response(serialized_projects.data, status=status.HTTP_200_OK)
    
class CategoryListView(APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching categories.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        