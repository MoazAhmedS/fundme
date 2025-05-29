from django.urls import path
from project.api.views import CreateCategoryView  

urlpatterns = [
    path('api/createCategory/', CreateCategoryView.as_view(), name='create-category'),
]
