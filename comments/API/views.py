from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from comments.models import Comment
from ..models import Project
from .serializers import (
    ProjectCommentSerializer,
    CommentReplySerializer,
)

class ProjectCommentView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Add a comment to a project",
        description="Authenticated users can post a comment on the specified project. Provide the comment text in the body.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'comment': {
                        'type': 'string',
                        'description': 'The content of the comment'
                    }
                },
                'required': ['text']
            }
        },
        responses={
            201: OpenApiResponse(description="Comment created successfully."),
            400: OpenApiResponse(description="Validation error — bad input"),
            404: OpenApiResponse(description="Project not found"),
            401: OpenApiResponse(description="Authentication required"),
        },
        tags=["Comments"],
    )
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

    @extend_schema(
        summary="Reply to a comment",
        description="Allows an authenticated user to reply to an existing comment. The project ID is inherited from the parent comment.",
        request=CommentReplySerializer,
        responses={
            201: CommentReplySerializer,
            400: OpenApiResponse(description="Validation error — bad input"),
            404: OpenApiResponse(description="Parent comment not found"),
            401: OpenApiResponse(description="Authentication required"),
        },
        tags=["Comments"]
    )
    def post(self, request, comment_id):
        try:
            parent_comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Parent comment not found.'}, status=status.HTTP_404_NOT_FOUND)

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
