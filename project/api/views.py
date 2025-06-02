from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.pagination import  PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from ..models import *
from comments.models import Comment
from comments.API.serializers import CommentSerializer
from interactions.models import Tag, ProjectTag
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

@extend_schema(
    summary="List all projects",
    description="Retrieve all projects with their images, tags, current donations, and average ratings.",
    responses={201: ProjectSerializer}
)
class AllProjectsAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Create a new project",
    description="This endpoint allows authenticated users to create a new project. The request must include project details, images, and tags. The user must be authenticated to access this endpoint.",
    request=ProjectSerializer,
    responses={201: ProjectSerializer}
)
class CreateProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_data = request.data.copy()
        images = request.FILES.getlist('images')

        if not images:
            return Response(
                data={'error': 'At least one image is required to create a project.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        tag_names = request.data.getlist('tags')

        projectSerialized = ProjectSerializer(data=project_data)
        if projectSerialized.is_valid():
            if(projectSerialized.validated_data['target'] <= 0):
                return Response(
                    {'error': 'Project Target must be greater than zero.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if(projectSerialized.validated_data['end_date'] < projectSerialized.validated_data['start_date']):
                return Response(
                    {'error': 'Project end date must be after the start date.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
            if(projectSerialized.validated_data['status'] == False):
                projectSerialized.validated_data['status'] = True

            projectSerialized.validated_data['userObject'] = request.user
            project = projectSerialized.save()

            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                ProjectTag.objects.get_or_create(project_id=project, tag_id=tag)

            for image in images:
                Images.objects.create(projectObject=project, path=image)

            return Response(data=ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors': projectSerialized.errors}, status=status.HTTP_400_BAD_REQUEST)

        
@extend_schema(
        summary="Retrieve a project's details",
        description="Fetch detailed information for a specific project using its ID. Returns 404 if the project is not found.",
        responses={200: ProjectSerializer}
    )
class ProjectDetails(APIView):
    def get(self, request, id):
        try:
            project_data = ProjectSerializer.getProjectById(id)
            if not project_data:
                return Response(
                    {"success": False, "message": "Project not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(data=project_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "message": "An error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(
        summary="Retrieve comments for a project",
        description="Retrieve all comments and replies for a specific project using its ID. Returns 404 if the project does not exist.",
        responses={200:CommentSerializer},
)
class ProjectCommentsView(APIView):
    def get(self, request, project_id):
        try:
            if not Project.objects.filter(id=project_id).exists():
                return Response(
                    {"success": False, "message": "Project not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            comments = Comment.objects.filter(project_id=project_id, parent_id=None).order_by('-created_date')
            serialized = CommentSerializer(comments, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "message": "Failed to load comments.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(
    summary="Create a new category",
    description="Allows superusers to create a new category. Only authenticated superusers are authorized to access this endpoint.",
    request=CategorySerializer,
    responses={201: CategorySerializer}
)
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


@extend_schema(
    summary="Cancel a project",
    description=(
        "Allows an authenticated user to cancel a project by its ID, if the project is eligible for cancellation. "
        "Returns 404 if the project does not exist, 400 if it's already cancelled or if donations have reached at least 25% of the target."
    )
)
class CancelProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        try:
            project = Project.getProjById(project_id)
        except:
            return Response(
                {"success": False, "message": "Project not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if project.status is False:
            return Response(
                {"success": False, "message": "Project is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if project.can_be_cancelled:
            project.status = False
            project.save()
            return Response(
                {"success": True, "message": "Project cancelled successfully."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"success": False, "message": "Project cannot be cancelled. Donations >= 25% of target."},
                status=status.HTTP_400_BAD_REQUEST
            )

        
@extend_schema(
    summary="Retrieve similar projects",
    description="Fetch projects that share common tags with the given project ID, excluding the project itself.",
    responses={200: ProjectSerializer}
   )
class SimilarProjectsView(APIView):
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        tag_ids = list(
            ProjectTag.objects.filter(project_id=project).values_list('tag_id', flat=True)
        )

        if not tag_ids:
            return Response({'similar_projects': []}, status=status.HTTP_200_OK)

        similar_projects = (
            Project.objects
            .filter(status=True)
            .exclude(id=project.id)
            .annotate(shared_tags=Count(
                'projecttag__tag_id',
                filter=Q(projecttag__tag_id__in=tag_ids)
            ))
            .filter(shared_tags__gt=0)
            .order_by('-shared_tags')
        )

        serialized_data = ProjectSerializer(similar_projects, many=True).data
        return Response({'similar_projects': serialized_data}, status=status.HTTP_200_OK)
    
@extend_schema(
    summary="Search projects",
    description="Search projects by title or tags matching the given query string.",
    parameters=[
        OpenApiParameter(
            name="search",
            description="Search query string to filter projects by title or tag names",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={200: ProjectSerializer}
)
class SearchProjectsView(APIView):
    def get(self, request):
        search_query = request.GET.get('search', '')

        if not search_query:
            return Response(
                {"success": False, "message": "Please provide a search query."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            title_matches = Project.objects.filter(title__icontains=search_query, status=True)
            tag_matches = Project.objects.filter(
                projecttag__tag_id__name__icontains=search_query,
                status=True
            )
            projects = (title_matches | tag_matches).distinct()

            if not projects.exists():
                return Response(
                    {"success": False, "message": "No projects found matching the search query."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serialized = ProjectSerializer(projects, many=True)
            return Response(
                {"success": True, "data": serialized.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "message": "An error occurred during search.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(
        summary="Retrieve projects by category",
        description="Fetch active projects belonging to a specific category by its ID.",
        responses={200: ProjectSerializer}
        )
    
class ProjectsByCategoryView(APIView):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)

    
        projects = Project.objects.filter(categoryObject=category,status=True)

        if not projects.exists():
            return Response(
                {"projects": [], "message": "No projects found for this category."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProjectSerializer(projects, many=True)
        return Response({"projects": serializer.data}, status=status.HTTP_200_OK)
    
@extend_schema(
        summary="Get last five featured projects",
        description="Retrieve the latest five active projects marked as featured.",
        responses={200: ProjectSerializer(many=True)}
)    
class LastFiveFeaturedProjects(APIView):
    def get(self, request):
        projects = Project.objects.filter(featured=True,status=True).order_by('-create_date')[:5]
        serialized_projects = ProjectSerializer(projects, many=True)
        return Response(serialized_projects.data, status=status.HTTP_200_OK)
    
@extend_schema(
        summary="List all categories",
        description="Retrieve a list of all available categories.",
        responses={200: ProjectSerializer}
    )    
class CategoryListView(APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching categories.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(
        summary="Retrieve latest five active projects",
        description="Fetch the five most recently created projects that are currently active.",
        responses={200: ProjectSerializer}
    )
class LatestFiveProjectsView(APIView):
    def get(self, request):
        try:
            latest_projects = Project.objects.filter(status=True).order_by('-create_date')[:5]
            serializer = ProjectSerializer(latest_projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching the latest projects.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        


@extend_schema(
        summary="Retrieve top 5 highest rated active projects",
        description="Fetch the top five active projects ranked by average rating value.",
        responses={200: ProjectSerializer}
    )
class TopRatedRunningProjectsView(APIView):
    def get(self, request):
        projects = Project.objects.filter(status=True)
        projects = sorted(
            projects,
            key=lambda p: p.rate_set.aggregate(avg=Avg('rate_value'))['avg'] or 0,
            reverse=True
        )[:5]
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
@extend_schema(
        summary="Toggle featured status of a project",
        description="Allow superusers to toggle the featured status of a specific project by its ID.",
        responses={
        200: {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer', 'description': 'The ID of the project'},
                'featured': {'type': 'boolean', 'description': 'Whether the project is featured'},
                'message': {'type': 'string', 'description': 'Confirmation message'}
            },
            'example': {
                'id': 42,
                'featured': True,
                'message': 'Project featured status updated successfully.'
            }
        },
        404: OpenApiTypes.STR 
    }
        )
class ToggleFeaturedProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        if not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            project = get_object_or_404(Project, id=project_id)
            project.featured = not project.featured
            project.save()

            return Response({
                "id": project.id,
                "featured": project.featured,
                "message": "Project featured status updated successfully."
            }, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {"detail": "Project not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"detail": "An unexpected error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )