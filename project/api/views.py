from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import ProjectSerializer
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

