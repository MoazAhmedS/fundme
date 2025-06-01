from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from interactions.models import *
from .serializers import *
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Get project ratings",
    description="Retrieve all ratings for a specific project.",
    responses={200: RateSerializer(many=True)}
)
class RateListAPIView(APIView):
    def get(self, request, project_id):
        queryset = Rate.objects.filter(project_id=project_id)
        serializer = RateSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(
    summary="Rate a project",
    description="Authenticated users can rate a project with a value between 1 and 5 and add an optional note.",
    request=RateSerializer,
    responses={201: RateSerializer}
)
class RateCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        data = request.data.copy()
        data['project'] = project_id 
        serializer = RateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Insert Tag name in Tags if not exist",
    description="Creates a new tag if it doesn't exist. If it exists, returns the existing one.",
    request=TagSerializer,
    responses={
        200: TagSerializer,
        201: TagSerializer
    }
)
class CreateTagView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = serializer.validated_data['name'].strip()

        if not name:
            return Response({"name": "Tag name cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        tag, created = Tag.objects.get_or_create(name=name)
        output = TagSerializer(tag).data
        return Response(output | {"created": created}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)