from django.urls import path
from project.api.views import *
urlpatterns = [
    path('Create/',CreateProject.as_view()),
    path('<int:id>/',ProjectDetails.as_view()),
    path('<int:project_id>/Comments/', ProjectCommentsView.as_view(), name='project-comments'),
    path('<int:project_id>/Similar/', SimilarProjectsView.as_view(), name='similar-projects'),
    path('Search/', SearchProjectsView.as_view(), name='project-search'),
    path('featured/latest/', LastFiveFeaturedProjects.as_view(), name='last-featured-projects'),
    path('list/categories/', CategoryListView.as_view(), name='category-list'),
]