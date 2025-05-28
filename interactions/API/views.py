from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from interactions.models import Rate
from .serializers import RateSerializer

class RateListAPIView(APIView):
    def get(self, request, project_id):
        queryset = Rate.objects.filter(project_id=project_id)
        serializer = RateSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RateCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        data = request.data.copy()
        data['project_id'] = project_id 
        serializer = RateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
