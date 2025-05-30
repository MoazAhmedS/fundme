from django.urls import path
from project.api.views import *

urlpatterns = [
    path('API/Create/',CreateProject.as_view()),
    path('API/<int:id>/',ProjectDetails.as_view()),
    path('API/<int:project_id>/comments/', ProjectCommentsView.as_view(), name='project-comments'),
    path('API/createCategory/', CreateCategoryView.as_view(), name='create-category'),
    path('API/cancel/<int:project_id>/', CancelProjectAPIView.as_view(), name='cancel_project'),
    path('API/<int:project_id>/similar/', SimilarProjectsView.as_view(), name='similar-projects'),
    path('API/Search/', SearchProjectsView.as_view(), name='project-search'),
    path('API/categories/<int:category_id>/projects/', ProjectsByCategoryView.as_view(), name='projects-by-category'),
    path('API/featured/latest/', LastFiveFeaturedProjects.as_view(), name='last-featured-projects'),
    path('API/list/categories/', CategoryListView.as_view(), name='category-list'),
    path('API/latest-projects/', LatestFiveProjectsView.as_view(), name='latest-projects'),
    path('API/projects/top/', TopRatedRunningProjectsView.as_view(), name='top-projects'),
]
