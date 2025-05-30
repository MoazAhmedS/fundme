from django.urls import path  
from .API.views import ProjectCommentView, CommentReplyView

urlpatterns = [
    path('projects/<int:project_id>/comments/', ProjectCommentView.as_view(), name='project-comments'),
    path('comments/<int:comment_id>/reply/', CommentReplyView.as_view(), name='comment-reply'),
]