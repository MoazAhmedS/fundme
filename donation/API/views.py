from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from donation.models import Donation
from project.models import Project
from donation.API.serializers import DonationSerializer 
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(
    summary="Create a new donation",
    description="This endpoint allows authenticated users to donate to a project. The request must include the donation amount. The user must be authenticated to access this endpoint.",
    request=DonationSerializer,
    responses={
        201: DonationSerializer,
        400: OpenApiResponse(description="Bad Request (Invalid data)"),
        404: OpenApiResponse(description="Project not found")
    }
)
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
            if(serializer.validated_data['amount'] <= 0):
                return Response(
                    {'error': 'Donation amount must be greater than zero.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            donation_amount = serializer.validated_data['amount']
            remaining_amount = project.target - project.current_donations
            if remaining_amount == 0:
                return Response(
                    {'error': 'Project has already reached its target.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if donation_amount > remaining_amount:
                return Response(
                    {'error': f'Donation exceeds remaining target. Only {remaining_amount} left.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            donation = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
