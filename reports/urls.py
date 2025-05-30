from django.urls import path
from .views import ReportCommentAPIView, ReportProjectAPIView

urlpatterns = [
    path('comments/<int:comment_id>/', ReportCommentAPIView.as_view(), name='report-comment'),
    path('projects/<int:project_id>/', ReportProjectAPIView.as_view(), name='report-project'),
]
