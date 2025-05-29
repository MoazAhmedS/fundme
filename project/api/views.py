from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from project.models import Category
from project.api.serializers import CategorySerializer

class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can create categories.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response({
                'message': 'Category created successfully.',
                'category': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)