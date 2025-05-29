from django.urls import path
from project.api.views import CreateCategoryView,ProjectsByCategoryView  

urlpatterns = [
    path('api/createCategory/', CreateCategoryView.as_view(), name='create-category'),
    path('categories/<int:category_id>/projects/', ProjectsByCategoryView.as_view(), name='projects-by-category'),
]
