from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from interactions.models import *
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiParameter ,OpenApiResponse ,OpenApiExample


@extend_schema(
    summary="List project ratings",
    description=(
        "Returns all ratings for a specific project, including user, value (1–5), and optional note. "
        "The project ID is passed in the URL."
    ),
    parameters=[
        OpenApiParameter(
            name='project_id',
            description='The ID of the project to retrieve ratings for.',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        )
    ],
    responses={200: RateSerializer(many=True)}
)
class RateListAPIView(APIView):
    def get(self, request, project_id):
        queryset = Rate.objects.filter(project_id=project_id)
        serializer = RateSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(
    summary="Rate a project",
    description="Allows authenticated users to rate a project with a value between 1 and 5 and add an optional note.",
    parameters=[
        OpenApiParameter(
            name='project_id',
            description='ID of the project to rate',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        )
    ],
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
    summary="Create a tag if not exists",
    description="Inserts a tag name in Tags if it does not already exist.",
    request=TagSerializer,
    responses={
        200: OpenApiResponse(response=TagSerializer, description="Tag already exists"),
        201: OpenApiResponse(response=TagSerializer, description="Tag created successfully")
    },
    examples=[
        OpenApiExample(
            name="Create Tag Example",
            value={"name": "education"},
            request_only=True
        )
    ]
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