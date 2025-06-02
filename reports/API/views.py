from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Report, ReportProject, ReportComment
from project.models import Project
from comments.models import Comment
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Report a comment",
    description="This endpoint allows authenticated users to report inappropriate comments.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'reason': {
                        'type': 'string',
                        'description': 'The content of the reason for reporting the comment',
                    }
                },
                'required': ['text']
            }
        },
    responses={
        201: {
            'type': 'object',
            'properties': {
                'success': {
                    'type': 'boolean',
                    'example': True,
                    'description': 'Indicates if the report was successful'
                },
                'message': {
                    'type': 'string',
                    'example': 'Comment has been reported successfully.',
                    'description': 'Success message'
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean', 'example': False},
                'message': {'type': 'string', 'example': 'Reason is required.'}
            }
        },
        404: {
            'description': 'Not Found',
            'type': 'object',
            'properties': {
                'detail': {'type': 'string', 'example': 'Not found.'}
            }
        }
    },
    tags=['Reports']
)
class ReportCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        reason = request.data.get('reason')
        if not reason:
            return Response({'success': False, 'message': 'Reason is required.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, id=comment_id)
        report = Report.objects.create(
            user_id=request.user,
            report_details=reason
        )

        ReportComment.objects.create(
            report_id=report,
            comment_id= comment
        )

        return Response({'success': True, 'message': 'comment has been reported successfully.'}, status=status.HTTP_201_CREATED)

@extend_schema(
    summary="Report a project",
    description="This endpoint allows authenticated users to report projects that violate guidelines.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'reason': {
                        'type': 'string',
                        'description': 'The content of the reason for reporting the project',
                    }
                },
                'required': ['text']
            }
        },
    responses={
        201: {
            'type': 'object',
            'properties': {
                'success': {
                    'type': 'boolean',
                    'example': True,
                    'description': 'Indicates if the report was successful'
                },
                'message': {
                    'type': 'string',
                    'example': 'Project has been reported successfully.',
                    'description': 'Success message'
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean', 'example': False},
                'message': {'type': 'string', 'example': 'Reason is required.'}
            }
        },
        404: {
            'description': 'Not Found',
            'type': 'object',
            'properties': {
                'detail': {'type': 'string', 'example': 'Not found.'}
            }
        }
    },
    tags=['Reports']
)
class ReportProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        reason = request.data.get('reason')
        if not reason:
            return Response({'success': False, 'message': 'Reason is required.'}, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(Project, id= project_id)
        report = Report.objects.create(
            user_id= request.user,
            report_details=reason
        )

        ReportProject.objects.create(
            report_id=report,
            project_id= project
        )

        return Response({'success': True, 'message': 'project has been reported successfully.'}, status=status.HTTP_201_CREATED)
