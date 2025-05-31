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


class CreateProject(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        project_data = request.data.copy()
        images = request.FILES.getlist('images')

        tag_names = request.data.getlist('tags')

        projectSerialized = ProjectSerializer(data=project_data)
        if projectSerialized.is_valid():
            project = projectSerialized.save()

            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                ProjectTag.objects.get_or_create(project_id=project, tag_id=tag)

            for image in images:
                Images.objects.create(projectObject=project, path=image)

            return Response(data=ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors': projectSerialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class ProjectDetails(APIView):
    def get(self,request,id):
        return Response(
            data=ProjectSerializer.getProjectById(id),
            status=status.HTTP_200_OK
        )

class ProjectCommentsView(APIView):
    def get(self, request, project_id):
        comments = Comment.objects.filter(project_id=project_id, parent_id=None).order_by('-created_date')
        serialized = CommentSerializer(comments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


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


class CancelProjectAPIView(APIView):

    def post(self, request, project_id):
        try:
            project = Project.getProjById(project_id)
        except:
            return Response(
                {"success": False, "message": "Project not found."},
                status=status.HTTP_404_NOT_FOUND
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
    

class SearchProjectsView(APIView):
    def get(self, request):
        search_query = request.GET.get('search', '')

        if not search_query:
            return Response({"detail": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

        title_matches = Project.objects.filter(title__icontains=search_query)

        tag_matches = Project.objects.filter(
            projecttag__tag_id__name__icontains=search_query
        )

        projects = (title_matches | tag_matches).distinct()

        serialized = ProjectSerializer(projects, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
 

class ProjectsByCategoryView(APIView):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)

    
        projects = Project.objects.filter(categoryObject=category)

        if not projects.exists():
            return Response(
                {"projects": [], "message": "No projects found for this category."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProjectSerializer(projects, many=True)
        return Response({"projects": serializer.data}, status=status.HTTP_200_OK)
    
class LastFiveFeaturedProjects(APIView):
    def get(self, request):
        projects = Project.objects.filter(featured=True).order_by('-create_date')[:5]
        serialized_projects = ProjectSerializer(projects, many=True)
        return Response(serialized_projects.data, status=status.HTTP_200_OK)
    
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

class LatestFiveProjectsView(APIView):
    def get(self, request):
        try:
            latest_projects = Project.objects.order_by('-create_date')[:5]
            serializer = ProjectSerializer(latest_projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching the latest projects.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        


class TopRatedRunningProjectsView(APIView):
    def get(self, request):
        running_projects = Project.objects.filter(status=True)
        rated_projects = running_projects.annotate(avg_rating=Avg('rate__rate_value'))
        top_rated_projects = rated_projects.order_by('-avg_rating')[:5]
        serializer = ProjectSerializer(top_rated_projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        

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