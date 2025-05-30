from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from donation.models import Donation
from project.models import Project
from donation.API.serializers import DonationSerializer 


class ProjectDonationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['project_id'] = project.id
        data['user_id'] = request.user.id

        serializer = DonationSerializer(data=data)

        if serializer.is_valid():
            donation = serializer.save()

            # # Optional: update the project's current donations
            # project.current_donations += donation.amount
            project.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
