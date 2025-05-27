from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from comments.models import Comment
from ..models import Project
from .serializers import (
    ProjectCommentSerializer,
    CommentReplySerializer,
)

class ProjectCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['project_id'] = project_id
        data['user_id'] = request.user.id

        serializer = ProjectCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class CommentReplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,  comment_id):
        # try:
        #     project = Project.objects.get(pk=projectry:
        #     project = Project.objects.get(pk=project_id)
        # except Project.DoesNotExist:
        #     return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)t_id)
        # except Project.DoesNotExist:
        #     return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            parent_comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Parent comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # if parent_comment.project_id.id != project.id:
        #     return Response({'error': 'Comment does not belong to this project.'}, status=status.HTTP_400_BAD_REQUEST)
        project = parent_comment.project_id 
        data = request.data.copy()
        data['project_id'] = project.id
        data['parent_id'] = parent_comment.id
        data['user_id'] = request.user.id

        serializer = CommentReplySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        