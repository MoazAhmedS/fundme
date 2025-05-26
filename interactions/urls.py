from django.urls import path
from interactions.api.views import TagListCreateView

urlpatterns = [
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
]