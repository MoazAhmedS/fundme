from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Report, ReportProject, ReportComment
from project.models import Project
from comments.models import Comment

class ReportCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        reason = request.data.get('reason')
        if not reason:
            return Response({'success': False, 'message': 'Reason is required.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, id=comment_id)
        report = Report.objects.create(
            user_id=request.user.id ,
            report_details=reason
        )

        ReportComment.objects.create(
            report_id=report,
            comment_id= comment
        )

        return Response({'success': True, 'message': 'comment has been reported successfully.'}, status=status.HTTP_201_CREATED)

class ReportProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        reason = request.data.get('reason')
        if not reason:
            return Response({'success': False, 'message': 'Reason is required.'}, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(Project, id= project_id)
        report = Report.objects.create(
            user_id= request.user.id ,
            report_details=reason
        )

        ReportProject.objects.create(
            report_id=report,
            project_id= project
        )

        return Response({'success': True, 'message': 'project has been reported successfully.'}, status=status.HTTP_201_CREATED)
