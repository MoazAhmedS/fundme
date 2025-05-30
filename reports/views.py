from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from project.models import Project
from .models import Report, ReportProject
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_project(request, project_id):
    user = request.user
    reason = request.data.get('reason')

    if not reason:
        return Response({'success': False, 'message': 'Reason is required.'}, status=status.HTTP_400_BAD_REQUEST)

    project = get_object_or_404(Project, id=project_id)

    report = Report.objects.create(
        user_id=user.profileuser,
        report_details=reason,
    )

    ReportProject.objects.create(
        report_id=report,
        project_id=project
    )

    return Response({'success': True, 'message': 'Project has been reported successfully.'}, status=status.HTTP_201_CREATED)
