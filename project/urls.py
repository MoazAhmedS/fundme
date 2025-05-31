from django.urls import path
from project.api.views import *

urlpatterns = [
    path('Create/',CreateProject.as_view()),
    path('<int:id>/',ProjectDetails.as_view()),
    path('<int:project_id>/comments/', ProjectCommentsView.as_view(), name='project-comments'),
    path('createCategory/', CreateCategoryView.as_view(), name='create-category'),
    path('cancel/<int:project_id>/', CancelProjectAPIView.as_view(), name='cancel_project'),
    path('<int:project_id>/similar/', SimilarProjectsView.as_view(), name='similar-projects'),
    path('Search/', SearchProjectsView.as_view(), name='project-search'),
    path('categories/<int:category_id>/projects/', ProjectsByCategoryView.as_view(), name='projects-by-category'),
    path('featured/latest/', LastFiveFeaturedProjects.as_view(), name='last-featured-projects'),
    path('list/categories/', CategoryListView.as_view(), name='category-list'),
    path('latest-projects/', LatestFiveProjectsView.as_view(), name='latest-projects'),
    path('projects/top/', TopRatedRunningProjectsView.as_view(), name='top-projects'),
    path('projects/<int:project_id>/toggle-featured/', ToggleFeaturedProjectView.as_view()),
]
